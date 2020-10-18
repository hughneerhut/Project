from Order import Order
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
cursor.execute("TRUNCATE TABLE system_state")
cursor.execute("DROP TABLE src_des_matrix")
cursor.execute("CREATE TABLE src_des_matrix (src VARCHAR(5))")
db.commit()
# Step 1. Import delivery order list from CSV into an array
orders = []

with open('datafile.csv', newline='') as csvfile:
    orderlist = csv.reader(csvfile, delimiter=',')
    for row in orderlist:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        orders.append(order)

total_orders = len(orders)  # total number of order

# Get order object from orderID
def get_order(orderid=""):
    for o in orders:
        if o.order_num == orderid:
            return o

current_time = pd.to_datetime("03/05/2020 08:00", dayfirst=True)
origins = []
destinations = []
processed_orders = []

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
            print(o.order_num)
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

    #Fill matrix table
    cursor.execute("TRUNCATE TABLE src_des_matrix")
    for src in origins:
        row = "o" + src
        sql = "INSERT INTO src_des_matrix (src) VALUES ('{}')".format(row)
        cursor.execute(sql)
        db.commit()
        for des in destinations:
            count = 0
            shared = []
            for o in processed_orders:
                combos = []
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
                        sql = "SHOW TABLE STATUS LIKE {}".format("'"+combo+"'")
                        cursor.execute(sql)
                        #create new table for each combo if it doesnt already exist
                        if not cursor.fetchall():
                            combos.append(combo)
                            sql = "CREATE TABLE {} (order_id VARCHAR(10), weight FLOAT, volume FLOAT, qty INT)".format(combo)
                            print("Added table: "+combo)
                            cursor.execute(sql)
                            db.commit()
                        # clear table on first iteration
                        if count == 1:
                            sql = "TRUNCATE TABLE {}".format(combo)
                            print("Cleared table: " + combo)
                            cursor.execute(sql)
                        sql = "INSERT INTO {} (order_id, weight, volume, qty) VALUES (%s, %s, %s, %s)".format(combo)
                        val = ("'"+ o.order_num + "'", o.weight, o.volume, o.item_qty)
                        cursor.execute(sql, val)
    current_time = current_time + pd.Timedelta(seconds=600)

#optimise is running at every 10 seconds for troubleshooting purposes
schedule.every(10).seconds.do(optimise)

while 1:
    schedule.run_pending()
    time.sleep(1)
