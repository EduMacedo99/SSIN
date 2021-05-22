# FEUP-SSIN

## Install
    $ npm install

## Create Database
    $ cd database
    $ cat create.sql | sqlite3 Database.db
    or (testing)
    $ cd server 
    $ python create_table.py

## Starrt Server & Pre-registration "face-to-face"
    $ cd server 
    $ python register_app.py
    $ node index

## First Registration &/or Authentication (New Session)
    $ cd client/_USERNAME_
    $ python ../client/client.py

* Main Menu
    1. Request service
        1. Calculation of square root (security level: 1)
        2. Calculation of cubic  root (security level: 2)
        3. Paramaterized n-root (security level: 3)
    2. Send message
    3. Wait for messages
