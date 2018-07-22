import _mysql

db = _mysql.connect(host="localhost", user="jonas",
                  passwd="dennis", db="bvs_db")

#CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
#    -> species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
#db.query("""create table BVS (batch INT, stationary VARCHAR(20), postage VARCHAR(20), umi VARCHAR(20), inserts VARCHAR(20), day INT, month VARCHAR(20), year INT)""")
#db.query("""insert into music (batch, stationary, postage, umi, inserts, day, month, year) values (?, ?, ?, ?, ?, ?), (artist, album, year, file, )""")
batch = 12234
stationary = 'banco'
postage = 'airmail'
umi = 'yes'
inserts = 'no'
day = 6
month = 'feb'
year = 2017
db.query("""INSERT INTO BVS (batch, stationary, postage, umi, inserts, day, month, year) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (batch, stationary, postage, umi, inserts, day, month, year))
db.commit()
db.query("""DESCRIBE BVS;""")
r = db.store_result()
print(r.fetch_row())