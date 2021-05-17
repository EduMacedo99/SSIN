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
counter = 0

#ver se .env.aes existe - se não existir é pq nao houve registo
if path.exists(".env.aes"):
    
    while counter < 3:
        print('> Already Registered\n> Proceeding with authentication')
        
        #ask for password
        username = input('Username: ')
        
        #TODO: pedir uma pass complicada
        password = getpass()

        try:
            pyAesCrypt.decryptFile(".env.aes", ".env", username+password)
            break
        except ValueError:
            print('Wrong username/password (or file is corrupted).')
            counter += 1
            if counter >= 3: exit()

    #get info
    try:
        dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True) #argumento file name existe 
    except OSError:
        print('.env not foud')
        exit()

    config = dotenv_values(".env") 
    print(config)   

    #delete newly created .env
    os.remove(".env")
    request_service(username)
else:
    registration()

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

