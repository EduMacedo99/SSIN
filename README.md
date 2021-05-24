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
    $ cd client
    $ python client.py

* Main Menu
    1. Request service
        1. Calculation of square root (security level: 1)
        2. Calculation of cubic  root (security level: 2)
        3. Paramaterized n-root (security level: 3)
    2. Send message


# Encrypt Process

## Registration
---------------------------------------------

---------------------------------------------
## Authentication
---------------------------------------------
### Client Challenge Request:
* not encrypted: username, new_iv
* encrypted: token, msg, TODO:**time**

### Server Response:
* not encrypted: challenge, new_iv
* encrypted: succ_msg
---------------------------------------------
### Client Challenge Solved Request:
* not encrypted: username, new_iv
* encrypted: "challenge", ip_port, TODO:**time**

### Server Response:
* not encrypted: new_iv
* encrypted: new_token, succ_msg
---------------------------------------------
## Services
---------------------------------------------
### Client set ip Request:
* not encrypted: username, new_iv
* encrypted: token, ip_port, TODO:**time**

### Server Response:
* not encrypted: new_iv
* encrypted: succ_msg
---------------------------------------------
---------------------------------------------
### Client get ip Request:
* not encrypted: username, new_iv
* encrypted: token, username_2, TODO:**time**

### Server Response:
* not encrypted: new_iv, ip_port
* encrypted: ip_port, succ_msg
---------------------------------------------
---------------------------------------------
### Client service Request:
* not encrypted: username, new_iv
* encrypted: token, service_data, TODO:**time**

### Server Response:
* not encrypted: new_iv
* encrypted: succ_msg with the value
---------------------------------------------
---------------------------------------------
### Client set public_key Request:
* not encrypted: username, new_iv
* encrypted: token, public_key, TODO:**time**

### Server Response:
* not encrypted: new_iv
* encrypted: succ_msg
---------------------------------------------
---------------------------------------------
### Client get public_key Request:
* not encrypted: username, new_iv
* encrypted: token, username_2, TODO:**time**

### Server Response:
* not encrypted: new_iv, ip_port
* encrypted: public_key, succ_msg
---------------------------------------------