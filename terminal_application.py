#!/usr/bin/python3

import os
import time
import pymysql

printedFiles = '/home/jonas/EQ/Printed'
printFiles = '/home/jonas/EQ/Print'

def find_batch(batch):
    batch = str(batch)
    whole_batch = []
    for printfile in os.listdir(printedFiles):
        file_frag = printfile.split('_')
        if batch in file_frag[0]:
            if printfile.endswith('.prn'):
                whole_batch.append(printfile)
            elif printfile.endswith('.ini'):
                print("ini file found:", printfile)
    batch_count = len(whole_batch) - 2
    try:

        data_file = whole_batch[1]
        print(data_file)
    except IndexError:
        print("batch : {} is not in the Printed files folder.\n\n".format(batch))
        
    else:
        stationary, postage, umi, inserts, date, time = process_file(data_file)

        date_split = date.split('/')
        date = "-".join(date_split)
        datetime = date + " " + time
        sql = "INSERT INTO BVS_VERIFIED(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
        print(sql)
        cursor.execute(sql)
        db.commit()
        print("batch number: {}".format(batch))
        print("batch date: {}".format(date))
        print("stationary: {}".format(stationary))
        print("postage: {}".format(postage))
        print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
        print("items: {}".format(batch_count))


def find_work_id(filename, rootpath=printFiles):
    """return work id"""
    file_path = os.path.join(rootpath, filename)
    with open(file_path, 'r') as f:
            contents = f.readlines(1024)
    for line in contents:
        if "Microsoft Word" in line:
            junk, id = line.split(' - ')
            id = id.replace('.xml"', '')
            id = id.replace('\n', '')
            return id

def process_file(filename, rootpath=printedFiles):
    data_file = os.path.join(rootpath, filename)
    with open(data_file, 'rb') as f:
        first = f.readlines(1024)

    for line in first:
        head = line.decode('UTF-8')
        head = head.replace('\r', '')
        head = head.replace('\n', '')
        head = head.replace("\"", '')
        # print(head)
        if "Microsoft" == head:
            jname = head.split(" = ")
            print(jname)

        elif "DATE" in head:
            date = head.split(' = ')
            date = date[1].split('/')
            date = "/".join(date)

        elif "TIME" in head:
            time = head.split(' = ')
            time = time[1]
            break

    file_frag = filename.split('_')
    stationary = file_frag[2].capitalize()

    umi = file_frag[3]
    if umi == '1':
        umi = "YES"
    elif umi == '0':
        umi = "NO"
    else:
        umi = 'UNDEFINED'

    inserts = file_frag[4]
    if inserts == '1':
        inserts = "YES"
    elif inserts == '0':
        inserts = "NO"
    else:
        inserts = 'UNDEFINED'

    postage = file_frag[5].replace('.prn', '')
    if postage == '0':
        postage = 'None'
    elif postage == '1':
        postage = 'First Class'
    elif postage == '2':
        postage = 'Airmail'
    elif postage == '3':
        postage = 'Second Class'
    elif postage == '6':
        postage = 'TNT'
    else:
        postage = 'UNDEFINED'

    try:
        return stationary, postage, umi, inserts, date, time
    except NameError:
        date = 'UNDEFINED'
        time = 'UNDEFINED'
        return stationary, postage, umi, inserts, date, time


def verify_number(number):
    try:
        number = int(number)
    except ValueError:
        print("{} is not a number.".format(number))
    else:
        if len(str(number)) <= 5:
            number = '{:05}'.format(number)
            find_batch(number)
        else:
            
            print("batch number: {0} too long.".format(number))


def input_batches(numbers):
    try:
        if ', ' in numbers:
            multiple_batches = numbers.split(', ')
            for number in multiple_batches:
                verify_number(number)
        else:
            verify_number(numbers)
    except TypeError:
        verify_number(numbers)


# printedFiles = 'D:/Dropbox/Printed'
# printedFiles = '/home/jonas/Dropbox/src/Printed'


version = 1.3
# build_date = '28/07/2017'
# build_date = '17/08/2017'
build_date = '30/08/2017'




def connect():
    """returns a cursor and its database if successful connection established to mysql server"""
    try:
        db = pymysql.connect("localhost", "BVS", "3Qu1n1t1", "bvs_db")
        cursor = db.cursor()
    except pymysql.err.OperationalError as e:
        print('Connection error... {}'.format(e))
    else:
        print("Connected to database")
        return cursor, db


def monitor():
    """monitors the print folder for open/closed batches and appends to corresponding mysql db"""
    monitor = True
    while monitor:
        unique_batches = set()
        batches = {}
        whole_folder = os.listdir(printFiles)
        cursor, db = connect()
        for print_file in whole_folder:
            file_frag = print_file.split('_')
            batch = file_frag[0]
            unique_batches.add(batch)
            if 'ini' not in print_file:
                stationary, postage, umi, inserts, date, time = process_file(print_file, printFiles)
                workid = find_work_id(print_file)
                id_query = "SELECT * FROM BVS_WORKID WHERE work_id='%s'" % workid
                cursor.execute(id_query)
                id_results = cursor.fetchall()
                if len(id_results) == 0:
                    datetime = date + " " + time
                    datetime = datetime.replace('/', '-')
                    sql = "INSERT INTO BVS_WORKID(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, WORK_ID, CREATION_DATE) \
                                                                                       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch, stationary, postage, umi, inserts, workid, "'" + datetime + "'")
                    cursor.execute(sql)
                    print("[sql_query]: {}".format(sql))
                    db.commit()
                else:
                    print("{} is already in ITEMS table".format(workid))

        for batch in unique_batches:
            for file_name in whole_folder:
                splitname = file_name.split('_')
                if splitname[0] == batch:
                    try:
                        if batches[batch]:
                            batches[batch].append(file_name)
                    except KeyError:
                        batches[batch] = [file_name]

        for batch_number, items in batches.items():
            batch_count = len(items) - 3
            sample_file = items[0]
            stationary, postage, umi, inserts, date, time = process_file(sample_file, printFiles)
            datetime = date + " " + time
            datetime = datetime.replace('/', '-')
            if any("_99999_" in item for item in items):
                open_query = "SELECT * FROM BVS_OPEN WHERE batch='%s'" % (batch_number)
                closed_query = "SELECT * FROM BVS_CLOSED WHERE batch='%s'" % (batch_number)
                cursor.execute(open_query)
                open_query_results = cursor.fetchall()
                if len(open_query_results) == 0:
                    cursor.execute(closed_query)
                    db.commit()
                    closed_query_results = cursor.fetchall()
                    if len(closed_query_results) == 0:
                        sql = "INSERT INTO BVS_CLOSED(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
                                                               VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
                        cursor.execute(sql)
                        #print("{0} has been put in CLOSED batch table".format(batch_number))
                        print("[sql_query]: {}".format(sql))
                        db.commit()

                    else:
                        print("{} is already in CLOSED table".format(batch_number))
                else:
                    #print("{} is in open table, delete from open and move to closed table".format(batch_number))
                    #print(open_query_results)
                    sql = "DELETE FROM BVS_OPEN WHERE batch='%s'" % batch_number
                    cursor.execute(sql)
                    print("[sql_query]: {}".format(sql))
                    sql = "INSERT INTO BVS_CLOSED(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
                                                                                       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
                    cursor.execute(sql)
                    print("[sql_query]: {}".format(sql))
                    db.commit()
            else:
                print("{} is OPEN".format(batch_number))
                open_query = "SELECT * FROM BVS_OPEN WHERE batch='%s'" % (batch_number)
                cursor.execute(open_query)
                db.commit()
                open_query_result = cursor.fetchall()
                if len(open_query_result) == 0:
                    sql = "INSERT INTO BVS_OPEN(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
                                                                                   VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
                    cursor.execute(sql)
                    #print("batch {0} has been put in OPEN batch table".format(batch_number))
                    print("[sql_query]: {}".format(sql))
                    db.commit()
                else:
                    print("{} is already in OPEN table".format(batch_number))
        monitor = False
        print("monitor has finished trawl...")
            



try:
    db = pymysql.connect("localhost", "BVS", "3Qu1n1t1", "bvs_db")
    cursor = db.cursor()
except pymysql.err.OperationalError as e:
    print("unable to connect:\n{} \n".format(e))
else:
    print("Connected to database.\n")


day = time.strftime("%d")
month = time.strftime("%B")
year = time.strftime("%Y")

hour = time.strftime("%H")
minutes = time.strftime("%M")
#print("{0}/{1}/{2} {3}:{4}".format(year, month, day, hour, minutes))


#batch_label = input("Enter batch to verify:")
#input_batches(batch_label)
for i in range(1, 31):
    input_batches(i)
monitor()