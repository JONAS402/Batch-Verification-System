#!/usr/bin/python3

import os
import random
import time

sample = './src/00638_00019_Banco_1_1_3.prn'

save_dir = '/home/jonas/Printed/'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def date_string():
    day = time.strftime("%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    hour = time.strftime("%H")
    minutes = time.strftime("%M")
    today = "{0}/{1}/{2}".format(year, month, day)
    # print(today)
    return today


dates = [x for x in range(1,32)]
batch_size = [x for x in range(1, 401)]
stationaries =["Banco", "Default", "Speccare", "St", "Jh", "Saga"]
postages = ["First Class", "Second Class", "Airmail", 'TNT', 'None']

with open(sample, 'rb') as f:
    first = f.readlines(1024)
lines = []
for line in first:
    head = line.decode('UTF-8')
    lines.append(line)
    
    
def create_head(date):
    for line in lines:
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
            break


def create_batches():

        for i in range(30, 40 + 1):
            number = '{:05}'.format(i)
            umi = random.choice(['y', 'n'])
            inserts = random.choice(['y', 'n'])
            stationary = random.choice(stationaries)
            batch_count = random.choice(batch_size)
            postage = random.choice(postages)
            date = date_string()
            print("batch number: {}".format(number))
            print("batch date: {}".format(date))
            print("stationary: {}".format(stationary))
            print("postage: {}".format(postage))
            print("UMI/INSERTS: {0}/{1}".format(umi, inserts))
            print("items: {}\n".format(batch_count))
            for pack in range(batch_count + 1):
                create_pack(pack, number, date, stationary, postage, umi, inserts)
            postage, umi, inserts = create_pack(99999, number, date, stationary, postage, umi, inserts)

            create_ini("00000", number, stationary, postage, umi, inserts)


def create_pack(pack, number, date, stationary, postage, umi, inserts):
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

    item = str(number) + '_' + str(pack) + '_' + stationary + '_' + str(umi) + '_' + str(inserts) + '_' + str(postage) + '.prn'
    # print("pack {0}\nDate:{1}".format(item, date))

    head = create_head(date)
    savefile = os.path.join(save_dir, item)
    print(savefile)
    with open(savefile, 'w') as s:
        s.write(head)
    return postage, umi, inserts
            

create_batches()
