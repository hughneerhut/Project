from Order import Order
from Postcode import Postcode
from Truck import Truck
import csv
import schedule
import pandas as pd
import time
import mysql.connector


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
        na_w = 0 #nsw/act
        na_v = 0
        q_v = 0
        q_w = 0
        s_w = 0
        s_v = 0
        w_w = 0
        w_v =0
        t_w = 0
        t_v = 0
        n_v = 0
        n_w = 0

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
                    print(na_w)
                    na_v = na_v + (o[2] * o[3])
                    w_cap_pct = (na_w / w_cap) * 100
                    v_cap_pct = (na_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_na.append(ord.order_num)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_na, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From NSW/ACT")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()

                if (combo[1] == "3"):
                    v_w = v_w + (o[1] * o[3])
                    v_v = v_v + (o[2] * o[3])
                    w_cap_pct = (v_w / w_cap) * 100
                    v_cap_pct = (v_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_v.append(ord.order_num)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_v, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From VIC")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "4"):
                    q_w = q_w + (o[1] * o[3])
                    q_v = q_v + (o[2] * o[3])
                    w_cap_pct = (q_w / w_cap) * 100
                    v_cap_pct = (q_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_q.append(ord.order_num)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_q, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From QLD")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
                            sql = "DELETE FROM {} where order_id = {}".format(combo, str(o))
                            cursor.execute(sql)
                            db.commit()
                if (combo[1] == "5"):
                    s_w = s_w + (o[1] * o[3])
                    s_v = s_v + (o[2] * o[3])
                    w_cap_pct = (s_w / w_cap) * 100
                    v_cap_pct = (s_v / v_cap) * 100
                    ord = get_order(o[0])
                    batched_orders_s.append(ord.order_num)
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_s, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From SA")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
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
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_w, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From WA")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
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
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_t, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From TAS")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
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
                    if (w_cap_pct > 90) or (v_cap_pct > 90):
                        truck = Truck(batched_orders_n, ord.from_pcode, [], ord.to_pcode)
                        trucks.append(truck)
                        print("Truck generated for destination: " + d + ". From NT")
                        for o in truck.orders:
                            print("Order added to truck : " + o)
                            to_remove = get_order(o)
                            processed_orders.remove(to_remove)
                            sql = "DELETE FROM system_state where order_ID = %s " % o
                            cursor.execute(sql)
                            db.commit()
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
