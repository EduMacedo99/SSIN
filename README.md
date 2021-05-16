# FEUP-SSIN

## Install
    $ npm install

## Create Database
    $ cd database
    $ cat create.sql | sqlite3 Database.db

## Start Server
    $ node server/index

## Pre-registration face-to-face
    $ python server/register_app.py
    $ python client/client.py

## First Registration
    $ python client_app/client.py

## Automatic Authentication (New Session/login)
    $ python client_app/auth.py

## Services
1. Calculation of square root (security level: 1)
2. Calculation of cubic  root (security level: 2)
3. Paramaterized n-root (security level: 3)