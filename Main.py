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
cursor.execute("CREATE TABLE processed (orderID INT, origin INT, destination INT, status VARCHAR(20), truckID INT, created DATETIME)")
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

with open('australian_postcodes.csv', newline='') as csvfile:
    postcodeList = csv.reader(csvfile, delimiter=',')
    for row in postcodeList:
        postcode = Postcode(row[0], row[1], row[2])
        postcodes.append(postcode)


total_orders = len(orders)  # total number of order

# Get order object from orderID
def get_order(orderid=""):
    for o in orders:
        if str(o.order_num) == str(orderid):
            return o

def get_postcode(postcode=""):
    for pc in postcodes:
        if str(pc.postcode) == str(postcode):
            return pc


def get_starting_loc(origins = [], destination = ""):
    #get furthest origin from destination
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

def get_closest(origins = [], last = ""):
    #get furthest origin from destination
    last_pc = get_postcode(last)
    closest = 99999999999999999999999999999999999999999999999999999999999999
    closest_pc = ""
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

current_time = pd.to_datetime("03/05/2020 08:00", dayfirst=True)
origins = []
destinations = []
processed_orders = []
new_orders = []
cycles = 1

w_cap = 20000
v_cap = 69.08

def optimise():
    global current_time
    new_orders = []
    print(current_time)
    for o in orders:
        order_datetime = pd.to_datetime(o.ordered_date, dayfirst=True)
        #Get all orders from the last 10 minutes / 600 secs
        if (order_datetime - current_time).seconds < 600 and (order_datetime - current_time).days == 0:
            new_orders.append(o)
            processed_orders.append(o)
            sql = "INSERT INTO processed (orderID, origin, destination, status, created) VALUES (%s, %s, %s, 'NEW', '%s')" % (o.order_num, o.from_pcode, o.to_pcode, current_time)
            cursor.execute(sql)
            db.commit()
            print(o.order_num + " - Source: " + str(o.from_pcode) + ". Destination: " + str(o.to_pcode))
            #Add records to DB
            sql = "INSERT INTO system_state (src, des, order_ID) VALUES (%s, %s, %s)"
            val = (o.from_pcode,o.to_pcode,o.order_num)
            cursor.execute(sql, val)
            db.commit()
            #add records to origins and destinations list if not already
            if o.to_pcode not in destinations:
                destinations.append(o.to_pcode)
                new_col = "d" + o.to_pcode
                sql = "ALTER TABLE src_des_matrix ADD {} BOOLEAN".format(new_col)
                cursor.execute(sql)
                db.commit()
            if o.from_pcode not in origins:
                origins.append(o.from_pcode)
    combos = []
    #Fill matrix and delivery tables
    cursor.execute("TRUNCATE TABLE src_des_matrix") #reset matrix table
    for src in origins:
        row = "o" + src
        sql = "INSERT INTO src_des_matrix (src) VALUES ('{}')".format(row)
        cursor.execute(sql)
        db.commit()
        for des in destinations:
            count = 0
            shared = []
            for o in processed_orders:
                if o.from_pcode == src:
                    if o.to_pcode == des:
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


    for d in destinations:
        sql = "SELECT %s FROM src_des_matrix" % ("d" + d)
        cursor.execute(sql)
        print("===== " + d)
        i = 0
        sources = []
        combos = []
        v_w = 0 #vic
        v_v = 0
        v_sources = []
        na_w = 0 #nsw/act
        na_v = 0
        na_sources = []
        q_v = 0
        q_w = 0
        q_sources = []
        s_w = 0
        s_v = 0
        s_sources = []
        w_w = 0
        w_v =0
        w_sources = []
        t_w = 0
        t_v = 0
        t_sources = []
        n_v = 0
        n_w = 0
        n_sources = []

        batched_orders_na = []
        batched_orders_v = []
        batched_orders_q = []
        batched_orders_s = []
        batched_orders_w = []
        batched_orders_t = []
        batched_orders_n = []
        for o in cursor.fetchall():
            if (str(o) != "(None,)"):
                sources.append(origins[i])
                print(origins[i])
            i = i + 1
        for s in sources:
            combo = "o" + s + "d" + d
            combos.append(combo)
        for combo in combos:
            sql = "SELECT * FROM %s" % combo
            cursor.execute(sql)
            batched_orders = []
            for o in cursor.fetchall():
                if (combo[1] == "2"):
                    na_w = na_w + (o[1] * o[3])
                    na_v = na_v + (o[2] * o[3])
                    w_cap_pct = (na_w / w_cap) * 100
                    v_cap_pct = (na_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_na.append(ord.order_num)
                    na_sources.append(ord.from_pcode)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_na, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(na_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(na_sources, d)
                                print("STARTING LOC: " + get_starting_loc(na_sources, d))
                                na_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(na_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                na_sources.remove(next)
                                pickup_order.append((i + 1, next))

                        print("Truck generated for destination: " + d + ". From NSW/ACT. ID: " + str(truck.id))
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

                if (combo[1] == "3"):
                    v_w = v_w + (o[1] * o[3])
                    v_v = v_v + (o[2] * o[3])
                    w_cap_pct = (v_w / w_cap) * 100
                    v_cap_pct = (v_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_v.append(ord.order_num)
                    v_sources.append(ord.from_pcode)

                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_v, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(v_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(v_sources, d)
                                print("STARTING LOC: " + get_starting_loc(v_sources, d))
                                v_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(v_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                v_sources.remove(next)
                                pickup_order.append((i + 1, next))

                        print("Truck generated for destination: " + d + ". From VIC. ID: " + str(truck.id))
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            index = get_pickup_order(pickup_order, to_remove.from_pcode)
                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (o, truck.id, index, to_remove.from_pcode, d, current_time)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)

                            sql = "UPDATE processed SET status='BATCHED', truckID = %s WHERE orderID = %s" % (truck.id, o)
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "4"):
                    q_w = q_w + (o[1] * o[3])
                    q_v = q_v + (o[2] * o[3])
                    w_cap_pct = (q_w / w_cap) * 100
                    v_cap_pct = (q_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_q.append(ord.order_num)
                    q_sources.append(ord.from_pcode)

                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_q, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(q_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(q_sources, d)
                                print("STARTING LOC: " + get_starting_loc(q_sources, d))
                                q_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(q_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                q_sources.remove(next)
                                pickup_order.append((i+1, next))

                        for o in pickup_order:
                            print("ORDER : " + str(o))

                        print("Truck generated for destination: " + d + ". From QLD. ID: " + str(truck.id))
                        for o in truck.orders:

                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            index = get_pickup_order(pickup_order, to_remove.from_pcode)
                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (o, truck.id, index, to_remove.from_pcode, d, current_time)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)

                            sql = "UPDATE processed SET status='BATCHED', truckID = %s WHERE orderID = %s" % (truck.id, o)
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "5"):
                    s_w = s_w + (o[1] * o[3])
                    s_v = s_v + (o[2] * o[3])
                    w_cap_pct = (s_w / w_cap) * 100
                    v_cap_pct = (s_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_s.append(ord.order_num)
                    s_sources.append(ord.from_pcode)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_s, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(s_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(s_sources, d)
                                print("STARTING LOC: " + get_starting_loc(s_sources, d))
                                s_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(s_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                s_sources.remove(next)
                                pickup_order.append((i + 1, next))


                        print("Truck generated for destination: " + d + ". From SA. ID: " + str(truck.id))
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            index = get_pickup_order(pickup_order, to_remove.from_pcode)
                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (
                            o, truck.id, index, to_remove.from_pcode, d, current_time)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "6"):
                    w_w = w_w + (o[1] * o[3])
                    w_v = w_v + (o[2] * o[3])
                    w_cap_pct = (w_w / w_cap) * 100
                    v_cap_pct = (w_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_w.append(ord.order_num)
                    w_sources.append(ord.from_pcode)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_w, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(w_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(w_sources, d)
                                print("STARTING LOC: " + get_starting_loc(w_sources, d))
                                w_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(w_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                w_sources.remove(next)
                                pickup_order.append((i + 1, next))


                        print("Truck generated for destination: " + d + ". From WA.  ID: " + str(truck.id))
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            index = get_pickup_order(pickup_order, to_remove.from_pcode)
                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (
                            o, truck.id, to_remove.from_pcode, d, current_time)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "7"):
                    t_w = t_w + (o[1] * o[3])
                    t_v = t_v + (o[2] * o[3])
                    w_cap_pct = (t_w / w_cap) * 100
                    v_cap_pct = (t_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_t.append(ord.order_num)
                    t_sources.append(ord.from_pcode)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 999999) , batched_orders_t, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(t_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(t_sources, d)
                                print("STARTING LOC: " + get_starting_loc(t_sources, d))
                                t_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(t_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                t_sources.remove(next)
                                pickup_order.append((i + 1, next))

                        print("Truck generated for destination: " + d + ". From TAS.  ID: " + str(truck.id))
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (
                            o, truck.id, index, to_remove.from_pcode, d, current_time)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "0") and (combo[2] == "8"):
                    n_w = n_w + (o[1] * o[3])
                    n_v = n_v + (o[2] * o[3])
                    w_cap_pct = (n_w / w_cap) * 100
                    v_cap_pct = (n_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_n.append(ord.order_num)
                    n_sources.append(ord.from_pcode)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(randint(100000, 9999999) , batched_orders_n, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)

                        pickup_order = []

                        for i in range(0, len(n_sources)):
                            last = ""
                            if i == 0:
                                start = get_starting_loc(n_sources, d)
                                print("STARTING LOC: " + get_starting_loc(n_sources, d))
                                n_sources.remove(start)
                                pickup_order.append((i + 1, start))
                                last = start
                            else:
                                next = get_closest(n_sources, start)
                                print("Stop " + str(i) + ": " + next)
                                n_sources.remove(next)
                                pickup_order.append((i + 1, next))

                        print("Truck generated for destination: " + d + ". From NT. ID: " + str(truck.id))
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()

                            index = get_pickup_order(pickup_order, to_remove.from_pcode)
                            sql = "INSERT INTO batched (orderID, truckID, pickupIndex, origin, destination, created) VALUES (%s, %s, %s, %s, %s, '%s')" % (o, truck.id, index, to_remove.from_pcode, d, current_time)
                            print(sql)
                            cursor.execute(sql)

                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()

            # if (origins[i][0] == d[0]) and (origins[i] in sources):
            # print("same state")
            # sql = "SELECT distance from distlocal where postcode1=%s and postcode2=%s" % (origins[i], d)
            # cursor.execute(sql)
            # print("DISTANCE: " + str(cursor.fetchall()))


    current_time = current_time + pd.Timedelta(seconds=600)
    new_orders.clear()

#optimise is running at every 10 seconds for troubleshooting purposes
schedule.every(5).seconds.do(optimise)
cycles = cycles + 1




while 1:
    schedule.run_pending()
    time.sleep(1)



