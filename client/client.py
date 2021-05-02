#!python3

import os
from dotenv import load_dotenv, dotenv_values
import dotenv

from request_service import request_service

try:
    dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True) #argumento file name existe 
except OSError:
    print('.env not foud\n Creating a new one...')

config = dotenv_values(".env")
print(config)
print(config['REGISTERED'])
empty = False

try: registered = config['REGISTERED']
except KeyError:
    registered = '0'
    empty = True

def registration():
    username = input('Insert the username you chose on the server registration:\n')
    ID = input('Insert the unique ID you were given in the server registration:\n')

    #Aqui tentamos fazer registar no server 
    print('trying to register...')

    #exemplo
    success = 1

    if success == 1:
        dotenv.set_key(dotenv_file, "REGISTERED", '1')
        dotenv.set_key(dotenv_file, "USERNAME", username)
        dotenv.set_key(dotenv_file, "ID", ID)
        #polos a escolher uma password

    else:
        dotenv.set_key(dotenv_file, "REGISTERED", '0')
        print('Invalid username/ID')



if registered == '0':
    registration()
else: 
    print('Already successfully registered\n Initiating authentication')
    
    config = dotenv_values(".env")
    username = config['USERNAME']
    request_service(username)
