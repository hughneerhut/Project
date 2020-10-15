import numpy as np
from pyswarm import pso
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
no_trucks = total_orders//30 #total number of trucks

#initialise random value
max_rand = 0
for o in orders:
    o.rand_init = (round(random.uniform(0,1) * no_trucks) + 1)
    if o.rand_init > max_rand:
        max_rand =o.rand_init
        print("Max random: " ,max_rand)

batches = []
#Create random batches and initialise particles
for i in range(max_rand):
    batch = []
    for o in orders:
        if i == o.rand_init:
            batch.append(o.order_num)
    particles.append(batch)

#Print batches (for troubleshooting only)
batchnum = 1
for b in particles:
    print("batch number: ", batchnum)
    for i in range(len(b)):
        print(b[i])
    batchnum = batchnum + 1
print('Total orders: ', total_orders)
print("Total particles: ", len(particles));

# Step 2: Define the objective function
# We will use distance as the main factor for lowering emission output

def weight(x, *args):
    H, d, t = x
    B, rho, E, P = args
    return rho*2*np.pi*d*t*np.sqrt((B/2)**2 + H**2)

# Step 3: Define contraints
# For our project the constraint functions will be volume of orders and weight of orders per truck
def yield_stress(x, *args):
    H, d, t = x
    B, rho, E, P = args
    return (P*np.sqrt((B/2)**2 + H**2))/(2*t*np.pi*d*H)

def buckling_stress(x, *args):
    H, d, t = x
    B, rho, E, P = args
    return (np.pi**2*E*(d**2 + t**2))/(8*((B/2)**2 + H**2))

def deflection(x, *args):
    H, d, t = x
    B, rho, E, P = args
    return (P*np.sqrt((B/2)**2 + H**2)**3)/(2*t*np.pi*d*H**2*E)

def constraints(x, *args):
    strs = yield_stress(x, *args)
    buck = buckling_stress(x, *args)
    defl = deflection(x, *args)
    return [100 - strs, buck - strs, 0.25 - defl]

# Define the other parameters
B = 60  # inches
rho = 0.3  # lb/in^3
E = 30000  # kpsi (1000-psi)
P = 66  # kip (1000-lbs, force)
args = (B, rho, E, P)

# Define the lower and upper bounds for H, d, t, respectively
lb = [10, 1, 0.01]
ub = [30, 3, 0.25]

xopt, fopt = pso(weight, lb, ub, f_ieqcons=constraints, args=args)
print(xopt)
print(fopt)