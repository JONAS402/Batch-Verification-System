#!/usr/bin/python3

import pymysql

# Open database connection

db = pymysql.connect("localhost", "BVS", "BVS")
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS bvs_db")
db.close()
db = pymysql.connect("localhost", "BVS", "BVS", "bvs_db")

# prepare a cursor object using cursor() method
cursor = db.cursor()
cursor.execute("USE bvs_db")
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS BVS_VERIFIED, BVS_WORKID, BVS_CLOSED, BVS_OPEN")
print("dropped tables")

workid_table = """CREATE TABLE BVS_WORKID(BATCH CHAR(20), STATIONARY CHAR(20), POSTAGE CHAR(20),  
   UMI CHAR(20),
   INSERTS CHAR(20),
   WORK_ID INT, 
   CREATION_DATE DATETIME)
   """

closed_table = """CREATE TABLE BVS_CLOSED(
   BATCH  CHAR(20),
   STATIONARY  CHAR(20),
   POSTAGE CHAR(20),  
   UMI CHAR(20),
   INSERTS CHAR(20),
   ITEMS INT, 
   CREATION_DATE DATETIME)"""

open_table = """CREATE TABLE BVS_OPEN(
   BATCH  CHAR(20),
   STATIONARY  CHAR(20),
   POSTAGE CHAR(20),  
   UMI CHAR(20),
   INSERTS CHAR(20),
   ITEMS INT, 
   CREATION_DATE DATETIME)"""

verified_table = """CREATE TABLE BVS_VERIFIED(
   BATCH  CHAR(20),
   STATIONARY  CHAR(20),
   POSTAGE CHAR(20),  
   UMI CHAR(20),
   INSERTS CHAR(20),
   ITEMS INT, 
   CREATION_DATE DATETIME,
   VERIFICATION_DATE DATETIME NOT NULL DEFAULT NOW())"""

tables = [verified_table, open_table, closed_table, workid_table]

print("creating tables...")
for table in tables:
    print(table)
    res = cursor.execute(table)

print('created DB')
# disconnect from server
db.close()
