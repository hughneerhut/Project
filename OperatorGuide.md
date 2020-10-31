# 14 - Data-driven Operation Research for Cleaner Logistics

**Author: Hugh Neerhut**


This document is designed to assist operators in using the Cleaner Logistics route planner. It will contain an overview of how the system works, troubleshooting steps and reference material. 


# Database

The software relies heavily upon a MySQL Database running in the backend. The database structure is relatively straight-forward and will require a 1-time setup before use.  

## Setup:
- Download MySQL Server v8.0 from the MySQL website. ***Important:** *version 8.0 must be used. If you are experiencing errors when running our software, please check that you are running a compatible version of MySQL.*
- Optional: Download the MySQL Workbench tool for a graphical interface to the MySQL server. Available from MySQL
- Set up a new MySQL database. By default our software uses the following configuration:
	- Localhost
	- User= root
	- Password = rootpass
	- Database= project
***Note: It is good practice to change these settings for additional security. The database connection is set up statically in Python. To update the connection configuration you will need to manually change it in Python. These settings can be found in 'Main.py' at line 15.***

- Your database should now be set up successfully. **The tables will populate automatically when you start the software.** 


##  Tables:
The software will automatically set up the following tables:

**system_state :** src (varchar4), des(varchar4), order_ID(int)
This table is used for storing each individual order's source postcode and destination postcode for each order ID. Once orders have been batched for dispatch, they are removed from this table. 

**src_des_matrix** dynamic
This table is used to store the order destination and origins combinations. The rows contain each unique source postcode and the columns contain each unique destination postcode. If an order exists for the source/destination combo, a binary 1 will added to the aligning cell on the matrix. If the combo doesn't exist, the cell will contain 'null'. 

**processed** orderID(INT), origin(INT), destination(INT), weight(FLOAT), volume(FLOAT), qty(INT), status(VARCHAR), truckID(INT), created(DATETIME)
This table contains a list of orders in the queue. It is the master list of every order that has entered the system. The status field will either be 'NEW' or 'BATCHED'

**batched**orderID(INT), truckID(INT), pickupIndex(INT), origin(INT), destination(INT), created(DATETIME)
This table contains a list of all orders that have been successfully batched for dispatch.  The pickupIndex field is used to determine the order in which the truck will be picking up the orders from the different origins. 

**o----d----** orderID(INT), weight(FLOAT), volume(FLOAT), qty(INT)
These tables are created dynamically based on the different order origin/destination combos. Eg, for an order with origin 3000 and destination 4000 the table name would be o3000d4000 and the table would contain a list of orders from 3000 bound to 4000. 

## Troubleshooting 

- Ensure your MySQL server is running v8.0.
- Ensure you have configured your server according to the static connection in Python. (eg the host name, user name, password and database name match what is hard-coded in main.py line 15). 
- Restart the server
- Delete all tables or recreate your database. 

# Input

Currently the only way to input data into our system is via CSV. The CSV file must be formatted as per below.

|OrderID|Datetime|DestinationSuburb|DestinationState|DestinationPostcode|OriginSurburb|OriginState|OriginPostcode| Quantity|Weight|Volume|

**The CSV file must be named 'datafile.csv'** and placed in the root directory. 

A list of every Australian postcode with latitude and longitude is also contained in the root directory named 'postcodes.csv'. This list is currently valid, however it may need to be updated in the future due to new suburbs existing. 


# Optimisation

Optimisation occurs every 10 minutes. During this process all the new orders from the last 10 minutes are added to the system for processing. Once the orders have been processed, the system optimises trucking routes by using the src_des_matrix table to find orders bound to a particular destination. If the accumulated weight or volume of all orders bound to this postcode is over 90% of the trucks capacity (**default weight 20tonnes, volume 69m^3)** a batch will be created. The order of the pickup for each batch is calculated using GPS coordinates and an altered version of Pythagoras' theorem. The origin destination furthest from the destination will always be the first pickup location. It will then iterate through all other origins and find the next closest one for the next pickup. This ensures trucks travel minimal distance between each pickup. 