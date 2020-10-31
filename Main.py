from Order import Order
from Postcode import Postcode
from Truck import Truck
import csv
import schedule
import pandas as pd
import time
import math
import mysql.connector
from random import randint


# Group 14 - Logistical optimisation problem

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpass",
    database="project"
)
cursor = db.cursor()
#Reset system state tables
cursor.execute("DROP TABLE IF EXISTS system_state")
cursor.execute("CREATE TABLE system_state (src VARCHAR(4), des VARCHAR(4), order_ID INT)")
cursor.execute("DROP TABLE IF EXISTS src_des_matrix")
cursor.execute("CREATE TABLE src_des_matrix (src VARCHAR(5))")
cursor.execute("DROP TABLE IF EXISTS batched")
cursor.execute("CREATE TABLE batched (orderID INT, truckID INT, pickupIndex INT, origin INT, destination INT, created DATETIME)")
cursor.execute("DROP TABLE IF EXISTS processed")
cursor.execute("CREATE TABLE processed (orderID INT, origin INT, destination INT, weight FLOAT, volume FLOAT, qty INT, status VARCHAR(20), truckID INT, created DATETIME)")
db.commit()
# Step 1. Import delivery order list from CSV into an array
orders = []
postcodes = []
trucks = []

with open('datafile.csv', newline='') as csvfile:
    orderlist = csv.reader(csvfile, delimiter=',')
    for row in orderlist:
        order = Order(row[0], row[1], row[5], row[6], row[7], row[2], row[3], row[4], row[8], row[9], row[10])
        orders.append(order)

# Import ALL Australian postcodes and create objects for each containing GPS coords
with open('australian_postcodes.csv', newline='') as csvfile:
    postcodeList = csv.reader(csvfile, delimiter=',')
    for row in postcodeList:
        postcode = Postcode(row[0], row[1], row[2])
        postcodes.append(postcode)

# Get order object from orderID
def get_order(orderid=""):
    for o in orders:
        if str(o.order_num) == str(orderid):
            return o

#Get postcode object from postcode ID
def get_postcode(postcode=""):
    for pc in postcodes:
        if str(pc.postcode) == str(postcode):
            return pc

# This function returns the furthest origin from a destination. This is used to calculate a trucks starting location
def get_starting_loc(origins = [], destination = ""):
    d_pc = get_postcode(destination)
    furthest = 0
    furthest_pc = ""
    for o in origins:
        o_pc = get_postcode(o)
        dist = math.sqrt((float(d_pc.lat) - float(o_pc.lat))**2 + (float(d_pc.long) - float(o_pc.long))**2)
        if (dist > furthest) :
            furthest_pc = o
            furthest = dist
    return furthest_pc

# This function returns the next closest source based on the last source postcode
def get_closest(origins = [], last = "", destination = ""):
    last_pc = get_postcode(last)
    d_pc = get_postcode(destination)
    closest = math.sqrt((float(last_pc.lat) - float(d_pc.lat))**2 + (float(last_pc.long) - float(d_pc.long))**2)
    closest_pc = destination
    for o in origins:
        o_pc = get_postcode(o)
        dist = math.sqrt((float(last_pc.lat) - float(o_pc.lat))**2 + (float(last_pc.long) - float(o_pc.long))**2)
        if (dist < closest) :
            closest_pc = o
            closest = dist
    return closest_pc

def get_pickup_order(tuple = [], postcode = ""):
    for pc in tuple:
        if pc[1] == postcode:
            return pc[0]

#Set current time to the time of the first record in our sample data
current_time = pd.to_datetime("03/05/2020 08:00", dayfirst=True)

#Initialise lists
origins = [] #List to store origin postcodes
destinations = [] #List to store destination postcodes
processed_orders = [] #List to store queued orders


cycles = 1
total_orders = len(orders)  # total number of orders

#Set capacity thresholds based on a standard B-Double truck
w_cap = 20000 #Max truck volume set to 20 tonnes
v_cap = 69.08 #Max truck volume set to 69m^3

#This function provides the optimisation. It is executed every 10 minutes.
def optimise():
    global current_time
    new_orders = [] #List to store new orders from the last 10 minutes
    print(current_time)

    for o in orders:
        order_datetime = pd.to_datetime(o.ordered_date, dayfirst=True)
        #Get all orders from the last 10 minutes / 600 secs
        if (order_datetime - current_time).seconds < 600 and (order_datetime - current_time).days == 0:
            new_orders.append(o)
            processed_orders.append(o)
            # Add new orders to MySQL database
            sql = "INSERT INTO processed (orderID, origin, destination, weight, volume, qty, status, created) VALUES (%s, %s, %s, %s, %s, %s, 'NEW', '%s')" % (o.order_num, o.from_pcode, o.to_pcode, o.weight, o.volume, o.item_qty, current_time)
            cursor.execute(sql)
            db.commit()

            print(o.order_num + " - Source: " + str(o.from_pcode) + ". Destination: " + str(o.to_pcode))

            #Update the system state table
            sql = "INSERT INTO system_state (src, des, order_ID) VALUES (%s, %s, %s)"
            val = (o.from_pcode,o.to_pcode,o.order_num)
            cursor.execute(sql, val)
            db.commit()

            #add records to origins and destinations list if not already
            if o.to_pcode not in destinations:
                destinations.append(o.to_pcode)
                new_col = "d" + o.to_pcode
                sql = "ALTER TABLE src_des_matrix ADD %s BOOLEAN" % new_col
                cursor.execute(sql)
                db.commit()

            if o.from_pcode not in origins:
                origins.append(o.from_pcode)

    combos = [] #List to store origin/destination combos.

    #Fill matrix and delivery tables
    cursor.execute("TRUNCATE TABLE src_des_matrix") #reset matrix table
    for src in origins:
        #Store sources/origin postcodes in tables rows
        row = "o" + src
        sql = "INSERT INTO src_des_matrix (src) VALUES ('%s')" % row
        cursor.execute(sql)
        db.commit()
        for des in destinations:
            count = 0
            shared = []
            for o in processed_orders:
                if o.from_pcode == src:
                    if o.to_pcode == des:
                        #Store destination postcodes in table columns
                        shared.append(o)
                        count = count + 1
                        col = "d" + des
                        sql = "UPDATE src_des_matrix SET {}=%s WHERE src=%s".format(col)
                        val = (1, row)
                        cursor.execute(sql, val)
                        combo = row + col
                        db.commit()
                        if o in new_orders:
                            if combo not in combos:
                                combos.append(combo)
                            sql = "SHOW TABLE STATUS LIKE {}".format("'"+combo+"'")
                            cursor.execute(sql)
                            #create new table for each combo if it doesnt already exist
                            if not cursor.fetchall():
                                sql = "CREATE TABLE {} (order_id INT, weight FLOAT, volume FLOAT, qty INT)".format(combo)
                                print("Added table: "+combo)
                                cursor.execute(sql)
                                db.commit()
                            else:
                                if count == 1 :
                                    #Clear table if it already exists
                                    sql = "TRUNCATE TABLE {}".format(combo)
                                    cursor.execute(sql)

                            sql = "INSERT INTO {} (order_id, weight, volume, qty) VALUES (%s, %s, %s, %s)".format(combo)
                            val = (o.order_num, o.weight, o.volume, o.item_qty)
                            cursor.execute(sql, val)

    #For each destination get
    for d in destinations:
        #Get a list of sources for each destination
        sql = "SELECT %s FROM src_des_matrix" % ("d" + d)
        cursor.execute(sql)

        print("===== " + d)

        combos = []
        weight = 0
        volume = 0
        sources = []

        candidate_orders = [] #list of possible orders for each truck
        i = 0

        #Check destination/origin matrix table to see if each source delivers to the destination
        for o in cursor.fetchall():
            if (str(o) != "(None,)"):
                sources.append(origins[i]) #add to sources list if record not null
                print(origins[i])
            i = i + 1

        for s in sources:
            combo = "o" + s + "d" + d
            combos.append(combo)
        for combo in combos:
            sql = "SELECT * FROM %s" % combo
            cursor.execute(sql)

            for o in cursor.fetchall():

                weight = weight + (o[1] * o[3])
                volume = volume + (o[2] * o[3])
                w_cap_pct = (weight / w_cap) * 100
                v_cap_pct = (volume / v_cap) * 100
                ord = get_order(o[0])
                candidate_orders.append(ord.order_num)

                if (w_cap_pct > 90) or (v_cap_pct > 90):
                    pickup_order = []
                    stops = []

                    for i in range(0, len(sources)):
                        last = ""
                        if i == 0:
                            start = get_starting_loc(sources, d)
                            print("STARTING LOC: " + start)
                            sources.remove(start)
                            pickup_order.append((i + 1, start))
                            stops.append(start)
                            last = start
                        else:
                            next = get_closest(sources, start, d)
                            print("Stop " + str(i) + ": " + next)
                            if (next == d):
                                break
                            sources.remove(next)
                            stops.append(next)
                            pickup_order.append((i + 1, next))

                    for co in candidate_orders:
                        print("Order " + co)
                        cand = get_order(co)
                        if cand.from_pcode not in stops:
                            candidate_orders.remove(co)


                    truck = Truck(randint(100000, 999999), candidate_orders, ord.from_pcode, [], ord.to_pcode)
                    trucks.append(truck)
                    print("Truck generated for destination: " + d + ". ID: " + str(truck.id))
                    db.commit()
                    for o in truck.orders:
                        print("Order added to truck : " + o)
                        to_remove = get_order(o)
                        processed_orders.remove(to_remove)
                        sql = "DELETE FROM system_state where order_ID = %s " % o
                        cursor.execute(sql)

                        index = get_pickup_order(pickup_order, to_remove.from_pcode)
                        sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (o, truck.id, index, to_remove.from_pcode, d, current_time)
                        cursor.execute(sql)

                        sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                        cursor.execute(sql)

                        sql = "UPDATE processed SET status='BATCHED', truckID = %s WHERE orderID = %s" % (truck.id, o)
                        cursor.execute(sql)
                        db.commit()
                    volume = 0
                    weight = 0
                    sources = []

    current_time = current_time + pd.Timedelta(seconds=600)
    new_orders.clear()

#optimise is running at every 10 seconds for troubleshooting purposes
schedule.every(5).seconds.do(optimise)
cycles = cycles + 1

while 1:
    schedule.run_pending()
    time.sleep(1)



