#!python3

import os
from dotenv import load_dotenv, find_dotenv, dotenv_values


config = dotenv_values(".env")

try: registered = config['REGISTERED']
except KeyError:
    registered = '0'

print(registered)

def registration():
    username = input('Insert the username you chose on the server registration:\n')
    ID = input('Insert the unique ID you were given in the server registration:\n')

    #Aqui tentamos fazer registar no server 
    print('trying to register...')

    #exemplo
    success = 1

    if success == 1:
        print()



if registered == '0':
    registration()
else: 
    print('already successfully registered\n Initiating authentication')

    