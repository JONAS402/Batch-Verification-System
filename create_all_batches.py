#!/usr/bin/python3

import os
import random
import time

sample = './src/00638_00019_Banco_1_1_3.prn'

print_dir = '/home/jonas/EQ/Print/'

if not os.path.exists(print_dir):
    os.makedirs(print_dir)

def date_string():
    day = time.strftime("%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    hour = time.strftime("%H")
    minutes = time.strftime("%M")
    today = "{0}/{1}/{2}".format(year, month, day)
    # print(today)
    return today


#dates = [x for x in range(1,32)]
batch_size = [x for x in range(1, 401)]
stationaries =["Banco", "Default", "Speccare", "St", "Jh", "Saga"]
postages = ["First Class", "Second Class", "Airmail", 'TNT', 'None']

with open(sample, 'rb') as f:
    #d = f.read(1024)
    first = f.readlines(1024)
lines = []
for line in first:
    head = line.decode('UTF-8')
    lines.append(line)


def create_head(date):
    work_id = random.randint(100000000, 200000000)
    with open(sample, 'r') as f:
        d = f.read(2048)
    r = d.replace('145590379', str(work_id))
    e = r.replace('2017/07/28', date)
    #print(e)
    return e
    

def create_head2(date):
    for line in lines:

        if "Microsoft Word" in str(line):
            #print(line)
            front, junk = str(line).split(' - ')
            #print(z)
            num = random.randint(100000000, 200000000)
            new = front + " - " + str(num) + '.xml"\n'
            #print(new)
        if "DATE" in str(line):
            line_index = lines.index(line)
            lines.remove(line)
            try:
                line = str(line, 'utf-8')
            except TypeError:
                line = line
            front, _ = line.split(' = ')
            back = '"' + date + '"\n'
            word = []
            #print(date)
            word.append(front)
            word.append(back)
            lines.insert(line_index, " = ".join(word))
            head = ""
            for end in lines:
                try:
                    head += end
                except TypeError:
                    head += str(end, 'utf-8')
            return head


def create_ini(pack, number, stationary, postage, umi, inserts, save_dir=print_dir):
    item = str(number) + '_' + str(pack) + '_' + stationary + '_' + str(umi) + '_' + str(inserts) + '_' + str(postage) + '.ini'
    filename = os.path.join(save_dir, item)
    print(filename)
    with open(filename, 'w') as s:
        pass
    s.close()


def create_pack(pack, number, date, stationary, postage, umi, inserts, save_dir=print_dir):
    pack = '{:05}'.format(pack)
    if umi == 'y' or umi == 1:
        umi = 1
    else:
        umi = 0
    if inserts == 'y' or inserts == 1:
        inserts = 1
    else:
        inserts = 0
    if postage == 'None':
        postage = '0'
    elif postage == 'First Class':
        postage = '1'
    elif postage == 'Airmail':
        postage = '2'
    elif postage == 'Second Class':
        postage = '3'
    elif postage == 'TNT':
        postage = '6'
        # 00638_00000_Banco_1_1_3.prn
        # batch_pack_stat_umi_ins_post.

    item = str(number) + '_' + str(pack) + '_' + stationary + '_' + str(umi) + '_' + str(inserts) + '_' + str(
        postage) + '.prn'
    # print("pack {0}\nDate:{1}".format(item, date))

    head = create_head(date)
    savefile = os.path.join(save_dir, item)
    print(savefile)
    with open(savefile, 'w') as s:
        s.write(head)
    return postage, umi, inserts


def create_closed_batches(number_of_batches, startnum=1):
    print("creating CLOSED batches")
    for i in range(startnum, number_of_batches +1):
        number = '{:05}'.format(i)
        umi = random.choice(['y', 'n'])
        inserts = random.choice(['y', 'n'])
        stationary = random.choice(stationaries)
        batch_count = random.choice(batch_size)
        postage = random.choice(postages)
        date = date_string()
        print("creating batch: {}".format(number))
        #print("batch date: {}".format(date))
        #print("stationary: {}".format(stationary))
        #print("postage: {}".format(postage))
        #print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
        #print("items: {}\n".format(batch_count))
        for pack in range(batch_count +1):
            create_pack(pack, number, date, stationary, postage, umi, inserts)
        postage, umi, inserts = create_pack(99999, number, date, stationary, postage, umi, inserts)

        create_ini("00000", number, stationary, postage, umi, inserts)


def create_printed_batches(startnum, number_of_batches):
    print("creating PRINTED batches")
    printed_dir = '/home/jonas/EQ/Printed'
    if not os.path.exists(printed_dir):
        os.makedirs(printed_dir)
    print("test")
    for i in range(startnum):
        print(i)
    for i in range(startnum, number_of_batches +1):
        print(i)
        number = '{:05}'.format(i)
        umi = random.choice(['y', 'n'])
        inserts = random.choice(['y', 'n'])
        stationary = random.choice(stationaries)
        batch_count = random.choice(batch_size)
        postage = random.choice(postages)
        date = date_string()
        print("creating batch: {}".format(number))
        #print("batch date: {}".format(date))
        #print("stationary: {}".format(stationary))
        #print("postage: {}".format(postage))
        #print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
        #print("items: {}\n".format(batch_count))
        for pack in range(batch_count +1):
            create_pack(pack, number, date, stationary, postage, umi, inserts, save_dir=printed_dir)

        postage, umi, inserts = create_pack(99999, number, date, stationary, postage, umi, inserts, save_dir=printed_dir)

        create_ini("00000", number, stationary, postage, umi, inserts, save_dir=printed_dir)


def create_open_batches(startnum, number_of_batches):
    print("creating OPEN batches")
    for i in range(startnum, number_of_batches +1):
        number = '{:05}'.format(i)
        umi = random.choice(['y', 'n'])
        inserts = random.choice(['y', 'n'])
        stationary = random.choice(stationaries)
        batch_count = random.choice(batch_size)
        postage = random.choice(postages)
        date = date_string()
        print("creating batch: {}".format(number))
        #print("batch date: {}".format(date))
        #print("stationary: {}".format(stationary))
        #print("postage: {}".format(postage))
        #print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
        #print("items: {}\n".format(batch_count))
        for pack in range(batch_count +1):
            create_pack(pack, number, date, stationary, postage, umi, inserts)
        #create_pack(99999, number, date, stationary, postage, umi, inserts)

    
create_closed_batches(10)
create_open_batches(11, 20)
create_printed_batches(21, 30)
