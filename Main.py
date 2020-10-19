import numpy as np
from Order import Order
from Postcodes import Postcodes
import random
import csv
import googlemaps as maps
import schedule
import pandas as pd
import time
import datetime

# Group 14 - Logistical optimisation problem


# Step 1. Import delivery order list from CSV into an array
orders = []

with open('datafile.csv', newline='') as csvfile:
    orderlist = csv.reader(csvfile, delimiter=',')
    for row in orderlist:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        orders.append(order)

total_orders = len(orders)  # total number of order
num_trucks = total_orders // 30  # total number of trucks

next_time = ""

# Import Postcode data into an array
postcodes = []

with open('australian_postcodes.csv', newline='') as csvfile:
    postcodesList = csv.reader(csvfile, delimiter=',')
    for row in postcodesList:
        postcodes = Postcodes(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        postcodes.append(postcodes)


# Get order object from orderID
def get_order(orderid=""):
    for o in orders:
        if o.order_num == orderid:
            return o



current_time = pd.to_datetime("03/05/2020 08:00", dayfirst=True)

origins = []
destinations = []

def optimise():
    global current_time
    for o in orders:
        order_datetime = pd.to_datetime(o.ordered_date, dayfirst=True)
        if (order_datetime - current_time).seconds < 600 and (order_datetime - current_time).days == 0:
            print(o.order_num)
    current_time = current_time + pd.Timedelta(seconds=600)

#optimise is running at every 10 seconds for troubleshooting purposes
schedule.every(10).seconds.do(optimise)

while 1:
    schedule.run_pending()
    time.sleep(1)
