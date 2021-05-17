#!python3
import os
import os.path
from os import path
from dotenv import load_dotenv, dotenv_values
import dotenv
import pyAesCrypt
from request_service import request_service
from getpass import getpass


#pyAesCrypt.encryptFile(".env", ".env.aes", password)
#pyAesCrypt.decryptFile(".env.aes", ".env", password)

#ver se .env.aes existe - se não existir é pq nao houve registo
if path.exists(".env.aes"):
    #already registered
    #ask for password
    password = getpass()
    #decrypt file (TODO: por num while para 3 tentativas)
    try:
        pyAesCrypt.decryptFile(".env.aes", ".env", password)
    except ValueError:
        print('Wrong password (or file is corrupted).')
    #get info
    try:
        dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True) #argumento file name existe 
    except OSError:
        print('.env not foud')

    config = dotenv_values(".env") 
    print(config)   
    #delete newly created .env
    os.remove(".env")
else:
    registration()


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

    # if success == 1:
    #     dotenv.set_key(dotenv_file, "REGISTERED", '1')
    #     dotenv.set_key(dotenv_file, "USERNAME", username)
    #     dotenv.set_key(dotenv_file, "ID", ID)
    #     #polos a escolher uma password

    # else:
    #     dotenv.set_key(dotenv_file, "REGISTERED", '0')
    #     print('Invalid username/ID')



if registered == '0':
    registration()
else: 
    print('Already successfully registered\n Initiating authentication')
    
    username = config['USERNAME']
    print(username)
    request_service(username)
