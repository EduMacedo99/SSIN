#!python3
import os
import os.path
import re
import random
import string
import requests
import base64
import dotenv
import pyAesCrypt
from os import path
from dotenv import load_dotenv, dotenv_values
from getpass import getpass
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import symmetric_encryption
import auth
from request_service import ExceptionUserNotFound
from socket_functions import connect_socket, listen_socket
from request_service import request_service, request_set_ip, request_get_ip
from utils import *

SERVER_KEY_PATH = "resources/server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
SIZE = 16


# TODO: desparguetar isto
saveEnv = []

def registration(username):
    
    print("\n> Start Registration.\n")
    
    counter_pw = 0
    ID = input('Insert the unique ID you were given in the server registration:\n')

    server_info = server_reg(username, ID)

    if len(server_info) > 0:

        # polos a escolher uma password
        while counter_pw < 3:
            # Ask for strong password
            print('> Insert your a new password for this device. The password should at least:\n\t- Have 8 characters or more\n\t- Include Uppercase letters\n\t- Include numbers')
            save_pw = getpass()

            rexes = ('[A-Z]', '[a-z]', '[0-9]')

            if len(save_pw) >= 8 and all(re.search(r, save_pw) for r in rexes):
                print('\n> Strong password.')
                break
            else:
                print('\n> Password not strong enough... Try again')
                counter_pw += 1
                if counter_pw >= 3:
                    print("> Maximum tries exceeded. Exiting...")
                    exit()

        # criar ficheiro .env, por a info, encriptalon e apagá-lo
        f = open(".env", "x")

        # Desencriptar o .aes escrever para lá as variáveis e voltar a encriptá-lo como na autenticação
        try:
            dotenv_file = dotenv.find_dotenv(
                raise_error_if_not_found=True)  # argumento file name existe
        except OSError:
            print('.env not found')

        config = dotenv_values(".env")

        # Colocar info no .env
        dotenv.set_key(dotenv_file, "KEY", saveEnv[0])
        dotenv.set_key(dotenv_file, "TOKEN", saveEnv[1])
        dotenv.set_key(dotenv_file, "USERNAME", username)
        dotenv.set_key(dotenv_file, "ID", ID)

        # encriptá-lo
        pyAesCrypt.encryptFile(".env", ".env.aes", username+save_pw)

        # APAGA MALUCO
        f.close()
        os.remove(".env")

    else:
        print('> Error: Something went wrong')


def server_reg(username, one_time_id):
    
    print('> Start Registration.')
    
    # prepare encryption variables
    iv =  symmetric_encryption.create_new_iv(SIZE)
    symmetric_key = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(SIZE))

    # First-Registration -> get server public key
    # get server public key
    response = requests.get(SERVER_URL + "register")
    open('SERVER_KEY_PATH', 'wb').write(response.content)

    # encrypt one_time_id, symmetric_key and iv with serverd public  key
    key = RSA.importKey(open(SERVER_KEY_PATH).read())
    cipher = PKCS1_OAEP.new(key)

    one_time_id_encrypt = base64.b64encode(
        cipher.encrypt(one_time_id.encode("utf-8")))
    encrypt_key = base64.b64encode(
        cipher.encrypt(symmetric_key.encode("utf-8")))
    encrypt_iv = base64.b64encode(cipher.encrypt(iv.encode('utf-8')))
    token_encrypt = requests.post(
        SERVER_URL + "register/get_token",
        json={
            "ID_encrypt": one_time_id_encrypt.decode(),
            "encrypt_key": encrypt_key.decode(),
            "encrypt_iv": encrypt_iv.decode(),
            "username": username
        }, 
    ).json()
    # print("encrypted token: " + token_encrypt["token"])
    decrypted_token = symmetric_encryption.decrypt(
        token_encrypt["token"], iv.encode(), symmetric_key.encode())
    # print("decryptedtoken: " + decrypted_token)

    saveEnv.append(symmetric_key)
    saveEnv.append(decrypted_token)
    
    print("> Server Registration was successfull!\n")

    return saveEnv


def main_menu():
    print("Options:")
    print("1 - Request service")
    print("2 - Send message")
    print("3 - Wait for messages")
    option = int(input())
    if option == 1:
        request_service
    elif option == 2:
        username = input("Which client do you want to contact?\n")
        try:
            address_and_port = request_get_ip(username)
            port = int(address_and_port.split(":")[1])
            print(port)
            connect_socket(port)
        except ExceptionUserNotAvailable:
            print("This client is not available at the moment\n")
            main_menu()
        except ExceptionUserNotFound:
            print("This username does not exist in the server database\n")
            main_menu()
    elif option == 3:
        #username = dotenv_values(".env")["USERNAME"]
        username = "Pedro"
        my_port = random.randint(1024, 49151)
        request_set_ip(username, LOCALHOST + ":" + str(my_port))
        listen_socket(my_port)
    else:
        print("Invalid option\n")
        main_menu()


def decrypt_and_read_dotenv():
    counter = 0
    while counter < 3:

        # ask for password
        username = input('Username: ')

        password = getpass()

        try:
            pyAesCrypt.decryptFile(".env.aes", ".env", username+password)
            break
        except ValueError:
            print('\n> Wrong username/password (or file is corrupted).')
            counter += 1
            if counter >= 3:
                print('> Number of tries exceeded. Terminating program...')
                exit()

    # get info
    try:
        dotenv_file = dotenv.find_dotenv(
            raise_error_if_not_found=True)  # argumento file name existe
    except OSError:
        print('.env not foud')
        exit()

    config = dotenv_values(".env")

    # delete newly created .env
    os.remove(".env")
    # print(config)
    return config

def user_is_registred(username):
    # ver se .env.aes existe - se não existir é pq nao houve registo
    # TODO: criar folders para cada cliente ou qq coisa, assim depois de 1 cliente estar registrado, o proximo vai dar true mesmo n estando
    return path.exists(".env.aes")

def authentication():
    # Identifying the collaborator locally
    dotenv_config = decrypt_and_read_dotenv()
    
    if (len(dotenv_config) < 2):
        print("> Error: Authentication failed locally.")
        exit()
      
    # Authenticate with the server and start a new session
    # return ip_port of current session for the client
    return auth.authentication_server(dotenv_config, SERVER_URL, SIZE) 

########################################################### MAIN SCRIPT ###########################################################
username = input("\nInsert the username you chose on the server registration:\n")

if user_is_registred(username) == False:
    registration(username)
    proceed = input("Do you want to proceed with login? [y|n]\n")
    if proceed == "n":
        print('> Exiting...\n')
        exit()     
else:    
    print('\n> Already Registered.')
    
print('> Proceeding with authentication.\n')  
try:
    (new_config, ip_port_tuple) = authentication()
except:
    print("> Something went wrong.")
    exit()
    
# TODO: Save in the env the new config
# if not, the second login will not work

print("> Authentication done.\n")
my_ip_port = str(ip_port_tuple[0]) + ":" + str(ip_port_tuple[1]) 

# Services
print("> client session address: " + my_ip_port)
request_set_ip(username, my_ip_port)
main_menu()
request_service(username)

    
