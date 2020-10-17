import numpy as np
from Order import Order
import random
import csv
import googlemaps as maps


# Group 14 - Logistical optimisation problem


# Step 1. Import delivery order list from CSV into an array
orders = []
particles = []

with open('datafile.csv', newline='') as csvfile:
    orderlist = csv.reader(csvfile, delimiter=',')
    orderNum = 0
    for row in orderlist:
        order = Order(orderNum,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9])
        orders.append(order)
        orderNum = orderNum + 1

total_orders = len(orders) #total number of order
num_trucks = total_orders//30 #total number of trucks




#Get order object from orderID
def get_order(orderid =""):
    for o in orders:
        if o.order_num == orderid:
            return o

