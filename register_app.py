import sqlite3
import string
import random
import getpass
from hashlib import sha256

def create_table(connection=sqlite3.connect('database/Database.db')):
    conn.execute('''DROP TABLE IF EXISTS users;''')
    conn.execute('''
                 CREATE TABLE USERS (
                     username CHAR[8] NOT NULL PRIMARY KEY, 
                     password_hash TEXT,
                     security_level INT CHECK(3 >= security_level >= 1),
                     one_time_id TEXT,
                     ip_address )
                 ''')
    

def generate_id():
    chrs = string.ascii_letters + string.digits
    return ''.join([random.choice(chrs) for i in range(12)])


def new_user(username,password, security_level, one_time_id, connection=sqlite3.connect('database/Database.db')):
    conn.execute('INSERT INTO users VALUES ("'
                 + username + '", "' 
                 + sha256(bytes(password, "ascii")).hexdigest() + '", "' 
                 + security_level + '", "' 
                 + sha256(bytes(one_time_id, "ascii")).hexdigest() +
                 '", null, null);')

def display_table(connection=sqlite3.connect('database/Database.db')):
    cursor = connection.execute('''SELECT * FROM users;''')
    print("Cursor:", cursor)
    for row in cursor:
       print("username = ", row[0])
       print("password_hash = ", row[1])
       print("Security level = ", row[2])
       print("ID_hash = ", row[3])
       print("IP = ", row[4])
       print("Public Key = ", row[5])


if __name__ == "__main__":
    conn = sqlite3.connect('database/Database.db')
    print("Opened database successfully")
    
    username = input("Please enter collaborator username: \n")
    
    security_level = input("What is the security clearance level for this client? \n")
    
    one_time_id = generate_id()
    
    print("Important! Take note of your ID: ", one_time_id, "\n")
    
    password = getpass.getpass(prompt="Please enter your password\n")
    
    new_user(username, password, security_level, one_time_id, conn)
    conn.commit()
    conn.close()

    print("Register completed \n")

    display_table()
