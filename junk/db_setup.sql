CREATE DATABASE bvs_db;
USE bvs_db;
CREATE TABLE BVS (batch INT, stationary VARCHAR(20), postage VARCHAR(20), umi VARCHAR(20), inserts VARCHAR(20), items INT, day INT, month VARCHAR(20), year INT);

INSERT INTO BVS (batch, stationary, postage, umi, inserts, items, day, month, year) VALUES (00001, 'Banco', 'Airmail', 'yes', 'no', 200, 06, 02, 2017);

CREATE TABLE packs (batch INT, packNumber INT);

INSERT INTO packs (batch, packNumber) VALUES (00001, 12453532);