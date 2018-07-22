#!/bin/bash

echo 'Batch Verification System is installing...'

sleep 2

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip python3-tk mysql-server curl
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
echo 'Batch Verification System is installed!'

sleep 1

sudo pip3 install pymysql
echo 'python3 modules installed!'

sleep 1

echo 'creating root user in mysql, set root password:'
sudo mysqladmin -u root password
echo 'creating BVS user in mysql, login as root...'
sudo mysql -u root -p < ./create_user.sql

echo 'setting up nodejs...'

cd ./Page
npm install

echo 'Batch Verification System setup complete'

