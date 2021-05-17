#!python3
import os
import os.path
from os import path
from dotenv import load_dotenv, dotenv_values
import dotenv
import pyAesCrypt
from request_service import request_service
from getpass import getpass
import re
import time

def registration():
    counter_pw = 0
    username = input('Insert the username you chose on the server registration:\n')
    ID = input('Insert the unique ID you were given in the server registration:\n')
    
    success = serverReg()

    if success:

        #polos a escolher uma password
        while counter_pw < 3:
            #Ask for strong password
            print('Insert your a new password for this device. The password should at least:\n\t- Have 8 characters or more\n\t- Include Uppercase letters\n\t- Include numbers')
            save_pw = getpass()

            rexes = ('[A-Z]', '[a-z]', '[0-9]')

            if len(save_pw) >= 8 and all(re.search(r, save_pw) for r in rexes):
                print('Strong password. Trying to register...')
                break
            else:
                print('Password not strong enough... Try again')
                counter_pw +=1
                if counter >= 3: 
                    print("Maximum tries exceeded. Exiting...")
                    exit()

        #criar ficheiro .env, por a info, encriptalon e apagá-lo
        f = open(".env", "x")

        #Desencriptar o .aes escrever para lá as variáveis e voltar a encriptá-lo como na autenticação
        try:
            dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True) #argumento file name existe 
        except OSError:
            print('.env not foud')

        config = dotenv_values(".env")

        #por info
        dotenv.set_key(dotenv_file, "USERNAME", username)
        dotenv.set_key(dotenv_file, "ID", ID)
        
        #encriptá-lo
        pyAesCrypt.encryptFile(".env", ".env.aes", username+save_pw)

        #APAGA MALUCO
        f.close()
        os.remove(".env")


    else:
        #dizer que username/id estão mal e tentar outra vez
        print('Something went wrong')

def serverReg():
    print('codigo do raul aqui (?)')
    return True


########################################################### MAIN SCRIPT ###########################################################


#pyAesCrypt.encryptFile(".env", ".env.aes", password)
#pyAesCrypt.decryptFile(".env.aes", ".env", password)
counter = 0

#ver se .env.aes existe - se não existir é pq nao houve registo
if path.exists(".env.aes"):
    
    while counter < 3:
        print('> Already Registered\n> Proceeding with authentication')
        
        #ask for password
        username = input('Username: ')
        
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



