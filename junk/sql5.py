#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("localhost", "jonas", "dennis", "bvs_db")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO BVS(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, DAY, `MONTH`, YEAR) \
   VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s, %s )" % ('3828', 'Banco', 'Airmail', 'NO', 'YES', '4', '2',  1987)
try:
    print("excuting")
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    print('commiting changes')
    db.commit()
    sql = "SELECT * FROM BVS"
    print('d')
    cursor.execute(sql)
    print('e')
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    print(results)
    for row in results:
        print(row)
    print("finished")
except:
    # Rollback in case there is any error
    print('errors')
    db.rollback()

# disconnect from server
db.close()