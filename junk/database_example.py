import sqlite3
import os


db = sqlite3.connect('/sdcard/qpython/database.db')
db.row_factory = sqlite3.Row

#db.execute('drop table if exists person')
#db.execute('create table music (artist text, album text, year int, track text)')
count = 0
DIR = '/storage/3339-3632/Media/MUSIC'
for root, folder, files in os.walk(DIR):
    if len(files) > 1:
        structure = root.split('/')
        album = structure[len(structure) -1]
        artist = structure[len(structure) -2]
        if artist != 'MUSIC':
            if '(' in album or ')' in album:
                lalbum = list(album)
                first_p = lalbum.index('(')
                second_p = lalbum.index(')')
                nums = "0123456789"
                if lalbum[first_p +2] in nums and lalbum[second_p -1] in nums:
                    lalbum[first_p] = '['
                    lalbum[second_p] = ']'
                    year = "".join(lalbum[first_p +1:second_p])
                    album = "".join(lalbum)
            if '[' in album or ']' in album:
                lalbum = list(album)
                first_b = lalbum.index('[')
                second_b = lalbum.index(']')
                nums = "0123456789"
                if lalbum[first_b +2] in nums and lalbum[second_b -1] in nums:
                    lalbum[first_b] = '['
                    lalbum[second_b] = ']'
                    year = "".join(lalbum[first_b +1:second_b])
                    album = "".join(lalbum)
            else:
                year = 1900
            #print("artist: {0} album: {1} year: {2}".format(artist, album, year))
            #print("tracklist")
            for file in files:
                if file.endswith('.m4a') or file.endswith('.M4A') or file.endswith('.mp3') or file.endswith('.MP3'):
                    if '_' in file:
                        file = file.replace('_', ' ')
                        if '-' in file:
                            file = file.replace('-', ' - ')
                    if artist in file or album in file:
                        lfile = file.split(' - ')
                        if artist in lfile:
                            lfile.remove(artist)
                    
                    #print("artist: {0} album: {1} year: {2} trackname: {3}".format(artist, album, year, file))
                    count +=1
                    #db.execute("insert into music (artist, album, year, track) values (?, ?, ?, ?)", (artist, album, year, file))


db.cursor()
table = db.execute(" SELECT * FROM music WHERE artist='Katatonia'")
db.commit() #push updates to database

for each in table:
    print(dict(each))

db.close()
print("{} files added to music database".format(count))