#!python3

import os
from dotenv import load_dotenv, dotenv_values
import dotenv

dotenv_file = dotenv.find_dotenv()
config = dotenv_values(".env")

empty = False

try: registered = config['REGISTERED']
except KeyError:
    registered = '0'
    empty = True

print(registered)

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

    