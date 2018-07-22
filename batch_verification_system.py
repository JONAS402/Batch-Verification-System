#!/usr/bin/python3

import os
import time
import pymysql
from tkinter import *
from tkinter import messagebox


def about_callback():
    messagebox.showinfo("About...", "Written by David Hayler.\nEmail: S1lv3r_h4z3@protonmail.com.\nBuild Date: {0}.\nVersion: {1}".format(build_date, version))


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
        tex.insert(END, "batch : {} is not in the Printed files folder.\n\n".format(batch))
        tex.see(END)
    else:
        stationary, postage, umi, inserts, date, time = process_file(data_file)

        date_split = date.split('/')
        date = "-".join(date_split[::-1])
        datetime = date + " " + time
        sql = "INSERT INTO BVS(BATCH, STATIONARY, POSTAGE, UMI, INSERTS, ITEMS, CREATION_DATE) \
       VALUES ('%s', '%s', '%s', '%s', '%s', %s, %s )" % (batch, stationary, postage, umi, inserts, batch_count, "'" + datetime + "'")
        print(sql)
        cursor.execute(sql)
        db.commit()

        tex.insert(END, "batch number:{}\n".format(batch))
        tex.insert(END, "batch date:{}\n".format(date))
        tex.insert(END, "Stationary type:{}\n".format(stationary))
        tex.insert(END, "postage: {}\n".format(postage))
        tex.insert(END, "UMI/INSERTS: {0}/{1}\n".format(umi, inserts))
        tex.insert(END, "items: {}\n".format(batch_count))
        tex.insert(END, 'Batch added.\n\n')
        tex.see(END)
        print("batch number: {}".format(batch))
        print("batch date: {}".format(date))
        print("stationary: {}".format(stationary))
        print("postage: {}".format(postage))
        print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
        print("items: {}".format(batch_count))


def process_file(filename):
    data_file = os.path.join(printedFiles, filename)
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
            date = "/".join(date[::-1])

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
            tex.insert(END, "batch number: {0} too long.".format(number))
            tex.see()
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


def verify_callback():
    if batch_field.get() != '':
        batches = batch_field.get()
        input_batches(batches)
        # input_batches(str([x for x in range(52)]))


def verify_return(junk):   # junk needed for return key
    if batch_field.get() != '':
        batches = batch_field.get()
        input_batches(batches)


# printedFiles = 'D:/Dropbox/Printed'
# printedFiles = '/home/jonas/Dropbox/src/Printed'
printedFiles = '/home/jonas/Printed'

version = 1.3
# build_date = '28/07/2017'
# build_date = '17/08/2017'
build_date = '30/08/2017'


root = Tk()
root.wm_title('Batch Verification System')
top_frame = Frame(root)
top_frame.grid(column=0, row=0, sticky=(N, W, E, S))
tex = Text(master=top_frame)

try:
    db = pymysql.connect("localhost", "jonas", "dennis", "bvs_db")
    cursor = db.cursor()
except pymysql.err.OperationalError as e:
    print(e)
    tex.insert(END, "unable to connect:\n{} \n".format(e))
else:
    tex.insert(END, "Connected to database.\n")


day = time.strftime("%d")
month = time.strftime("%B")
year = time.strftime("%Y")

hour = time.strftime("%H")
minutes = time.strftime("%M")
#print("{0}/{1}/{2} {3}:{4}".format(year, month, day, hour, minutes))


menubar = Menu(root)
infomenu = Menu(menubar, tearoff=0)
filemenu = Menu(menubar, tearoff=0)


bottom_frame = Frame(root)
bottom_frame.grid(column=0, row=1, sticky=(W, E))


menubar.add_cascade(label='Menu', menu=infomenu)
infomenu.add_command(label="About...", command=about_callback)
infomenu.add_command(label="Quit", command=root.quit)


batch_label = Label(top_frame, text="Enter batch to verify:")
batch_field = Entry(top_frame)
verify_button = Button(top_frame, text="Verify", fg='black', bg='green', command=verify_callback)

tex.grid(row=2, column=0, columnspan=3)
batch_label.grid(row=0, column=0)
batch_field.grid(row=0, column=1)
batch_field.bind("<Return>", verify_return)
verify_button.grid(row=0, column=2)

root.config(menu=menubar)


w = 563   # width for the Tk root
h = 371   # height for the Tk root

# get display screen width and height
ws = root.winfo_screenwidth()    # width of the screen
hs = root.winfo_screenheight()   # height of the screen

# calculate x and y coordinates for positioning the Tk root window
# centered
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.mainloop()
