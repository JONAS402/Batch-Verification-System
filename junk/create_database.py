#!/usr/bin/python3

#sudo apt-get install python3-pymysql
import pymysql

# Open database connection
db = pymysql.connect("localhost", "jonas", "dennis", "bvs_db")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS BVS")
print("dropping table")
#db.query("""INSERT INTO BVS (batch, stationary, postage, umi, inserts, day, month, year) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (batch, stationary, postage, umi, inserts, day, month, year))


# Create table as per requirement
sql = """CREATE TABLE BVS (
   BATCH  CHAR(20),
   STATIONARY  CHAR(20),
   POSTAGE CHAR(20),  
   UMI CHAR(20),
   INSERTS CHAR(20),
   ITEMS INT, 
   DAY INT,
   `MONTH` CHAR(20),
   YEAR INT)"""

cursor.execute(sql)

print('created DB')
# disconnect from server
db.close()