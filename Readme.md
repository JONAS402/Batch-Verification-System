Batch Verification System

this project was designed to help me get to grips with HTML, javascript, and css. the main purpose was to streamline a secondary process in a task.

the task is as follows:
a continuous stream of "batches" (bundles of letters to be printed, ranging from 1 - 400. each letter could contain up to 20 pages each.) is uploaded to a folder.
These letters are printed via custom software, once printed they are moved into a separate folder.

the secondary task is to continuosly log each batch onto a spread sheet manually, recording stationary type, batch number, postage type, number of letters ect.

i decided to streamline this process, initially just creating a python GUI attached to a SQL database, however i decided to expand on this idea.

the almost finished result now includes a nodeJs webserver which locally hosts a website which allows you to view and query the database.
The GUI now also has a separate 'monitor' process which watches and automatically adds batches that are yet to be printed into separate databases, it also logs each letters UID.


Basic setup:

install:
./installer.sh
create DB:
./create_database.py

create sample batches (on a live system, this is not required):
./create_sample_batches.py

run application and verify batches:
./Application.py

make sure sql is running then launch node server:
npm start