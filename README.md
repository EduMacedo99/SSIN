# FEUP-SSIN

## Install
    $ npm install

## Create Database
    $ cd database
    $ cat create.sql | sqlite3 Database.db

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
    3. Wait for messages


# NOTES:
TODO: 1 - Segundo o pdf é o server que gera o username, e não o cliente, o cliente apenas lhe dá o nome dele ou assim:

"At the same time, a username (string with a maximum of 8 characters) and a one-time ID (a random string with 12 characters, comprised of small and capital letters and digits) is generated and communicated to the collaborator"

TODO: 2 - Encriptar mensagens nos serviços
