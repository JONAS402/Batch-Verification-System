#!/usr/bin/python3
# batch verification system application

import os
import pymysql
from tkinter import *
from tkinter import messagebox
import threading
from time import sleep


class BatchVerificationSystem:
    version = 2.0
    build_date = '17/09/2017'
    printedFiles = '/home/jonas/EQ/Printed'
    printFiles = '/home/jonas/EQ/Print'
    
    def __init__(self):
        self.root = Tk()
        self.root.wm_title('Batch Verification System')
        top_frame = Frame(self.root)
        top_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.textbox = Text(master=top_frame)
        menubar = Menu(self.root)
        infomenu = Menu(menubar, tearoff=0)
        filemenu = Menu(menubar, tearoff=0)

        bottom_frame = Frame(self.root)
        bottom_frame.grid(column=0, row=1, sticky=(W, E))

        menubar.add_cascade(label='Menu', menu=infomenu)
        infomenu.add_command(label="About...", command=self.about_callback)
        infomenu.add_command(label="Quit", command=self.root.quit)

        batch_label = Label(top_frame, text="Enter batch to verify:")
        self.batch_field = Entry(top_frame)
        verify_button = Button(top_frame, text="Verify", fg='black', bg='green', command=self.verify_callback)

        self.textbox.grid(row=2, column=0, columnspan=3)
        batch_label.grid(row=0, column=0)
        self.batch_field.grid(row=0, column=1)
        self.batch_field.bind("<Return>", self.verify_return)
        verify_button.grid(row=0, column=2)

        self.root.config(menu=menubar)

        w = 563  # width for the Tk root
        h = 371  # height for the Tk root

        # get display screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for positioning the Tk root window
        # centered
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        if not os.path.exists(self.printedFiles):
            os.makedirs(self.printedFiles)

    def about_callback(self):
        message = "Written by David Hayler.\nEmail: S1lv3r_h4z3@protonmail.com.\nBuild Date: {0}.\nVersion: {1}".format(self.build_date, self.version)
        messagebox.showinfo("About...", message)
    
    def find_work_id(self, filename, rootpath=printFiles):
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

    def connect(self):
        """returns a cursor and its database if successful connection established to mysql server"""
        try:
            db = pymysql.connect("localhost", "BVS", "3Qu1n1t1", "bvs_db")
            cursor = db.cursor()
        except pymysql.err.OperationalError as e:
            print('Connection error... {}'.format(e))
            self.textbox.insert(END, "unable to connect:\n{} \n".format(e))
        else:
            print("Connected to database")
            self.textbox.insert(END, "Connected to database.\n")
            return cursor, db

    def monitor(self, sleeptime=10):
        """monitors the print folder for open/closed batches and appends to corresponding mysql db"""

        self.textbox.insert(END, "Starting the monitoring service, this service will sleep for {} seconds between runs.\n".format(sleeptime))
        while True:
            unique_batches = set()
            batches = {}
            whole_folder = os.listdir(self.printFiles)
            cursor, db = self.connect()
            for print_file in whole_folder:
                file_frag = print_file.split('_')
                batch = file_frag[0]
                unique_batches.add(batch)
                if 'ini' not in print_file:
                    stationary, postage, umi, inserts, date, time = self.process_file(print_file, self.printFiles)
                    workid = self.find_work_id(print_file)
                    id_query = "SELECT * FROM BVS_WORKID WHERE work_id='%s'" % workid
                    cursor.execute(id_query)
                    id_results = cursor.fetchall()
                    if len(id_results) == 0:
                        datetime = date + " " + time
                        datetime = datetime.replace('/', '-')
                        sql = "INSERT INTO BVS_WORKID(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, WORK_ID, CREATION_DATE) \
                                                                                       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (
                            batch, stationary, postage, umi, inserts, workid, "'" + datetime + "'")
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
                stationary, postage, umi, inserts, date, time = self.process_file(sample_file, self.printFiles)
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
                                                               VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (
                            batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
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
                                                                                       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (
                            batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
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
                                                                                   VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (
                        batch_number, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
                        cursor.execute(sql)
                        #print("batch {0} has been put in OPEN batch table".format(batch_number))
                        print("[sql_query]: {}".format(sql))
                        db.commit()
                    else:
                        print("{} is already in OPEN table".format(batch_number))
            print("Sleeping for {} seconds...".format(sleeptime))
            self.textbox.insert(END, "Sleeping for {} seconds...\n".format(sleeptime))
            sleep(sleeptime)

    def find_batch(self, batch):
        batch = str(batch)
        whole_batch = []
        for printfile in os.listdir(self.printedFiles):
            file_frag = printfile.split('_')
            if batch in file_frag[0]:
                if printfile.endswith('.prn'):
                    whole_batch.append(printfile)
                elif printfile.endswith('.ini'):
                    print("ini file found:", printfile)
        batch_count = len(whole_batch) - 2
        try:

            data_file = whole_batch[1]
            #print(data_file)
        except IndexError:
            self.textbox.insert(END, "batch : {} is not in the Printed files folder.\n\n".format(batch))
            self.textbox.see(END)
        else:
            stationary, postage, umi, inserts, date, time = self.process_file(data_file)

            date_split = date.split('/')
            date = "-".join(date_split)
            datetime = date + " " + time
            sql = "INSERT INTO BVS_VERIFIED(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
           VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (
            batch, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
            print("[sql_query]: {}".format(sql))
            cursor, db = self.connect()
            cursor.execute(sql)
            db.commit()

            self.textbox.insert(END, "batch number:{}\n".format(batch))
            self.textbox.insert(END, "batch date:{}\n".format(date))
            self.textbox.insert(END, "Stationary type:{}\n".format(stationary))
            self.textbox.insert(END, "postage: {}\n".format(postage))
            self.textbox.insert(END, "UMI/INSERTS: {0}/{1}\n".format(umi, inserts))
            self.textbox.insert(END, "items: {}\n".format(batch_count))
            self.textbox.insert(END, 'Batch added.\n\n')
            self.textbox.see(END)
            print("batch number: {}".format(batch))
            print("batch date: {}".format(date))
            print("stationary: {}".format(stationary))
            print("postage: {}".format(postage))
            print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
            print("items: {}".format(batch_count))

    def process_file(self, filename, rootpath=printedFiles):
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

    def verify_number(self, number):
        # print("verify_number: ", number)
        try:
            
            if '[' in number and ']' in number:
                print("list expansion") ## broken
                for n in number:
                    try:
                        n = int(n)
                        if len(str(n)) <= 5:
                            n = '{:05}'.format(n)
                            self.find_batch(n)
                    except ValueError as e:
                        print("error in list expansion: {}".format(e))
                        self.textbox.insert(END, "{} is not a number.".format(number))
                        self.textbox.see()
                return
            else:
                number = int(number)
        except ValueError:
            print("{} is not a number.".format(number))
            self.textbox.insert(END, "{} is not a number.".format(number))
            self.textbox.see()
        else:
            if len(str(number)) <= 5:
                number = '{:05}'.format(number)
                self.find_batch(number)
            else:
                self.textbox.insert(END, "batch number: {0} too long.".format(number))
                self.textbox.see()
                print("batch number: {0} too long.".format(number))

    def input_batches(self, numbers):
        # print("input_batches: ", numbers)
        try:
            if ', ' in numbers:
                multiple_batches = numbers.split(', ')
                for number in multiple_batches:
                    self.verify_number(number)
            else:
                self.verify_number(numbers)
        except TypeError:
            self.verify_number(numbers)

    def verify_callback(self):
        if self.batch_field.get() != '':
            batches = self.batch_field.get()
            self.input_batches(batches)
            # input_batches(str([x for x in range(52)]))

    def verify_return(self, junk):  # junk needed for return key
        if self.batch_field.get() != '':
            batches = self.batch_field.get()
            self.input_batches(batches)

    def main(self):
        self.thread()
        self.root.mainloop()

    def thread(self):
        t = threading.Thread(target=self.monitor)
        t.daemon = True
        t.start()
    
    
bvs = BatchVerificationSystem()
# bvs.monitor()
bvs.main()
