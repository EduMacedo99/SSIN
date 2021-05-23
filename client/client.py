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
from threading import Thread
import atexit

import symmetric_encryption
import auth
from request_service import ExceptionUserNotFound
from socket_functions import send_message, listen_socket
from request_service import request_service, request_set_ip, request_get_ip, request_public_key
from utils import *

SERVER_KEY_PATH = "resources/server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
SIZE = 16

keyToDecrypt = ''

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
        exit(-1)


def server_reg(username, one_time_ID):
    
    print('> Start Registration.')
    
    # prepare encryption variables
    iv =  symmetric_encryption.create_new_iv(SIZE)
    symmetric_key = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(SIZE))

    # First-Registration -> get server public key
    # get server public key
    response = requests.get(SERVER_URL + "register")
    open(SERVER_KEY_PATH, 'wb').write(response.content)

    # encrypt one_time_id, symmetric_key and iv with serverd public  key
    key = RSA.importKey(open(SERVER_KEY_PATH).read())
    cipher = PKCS1_OAEP.new(key)

    one_time_ID_encrypt = base64.b64encode(
        cipher.encrypt(one_time_ID.encode("utf-8")))
    encrypt_key = base64.b64encode(
        cipher.encrypt(symmetric_key.encode("utf-8")))
    encrypt_iv = base64.b64encode(cipher.encrypt(iv.encode('utf-8')))
    token_encrypt = requests.post(
        SERVER_URL + "register/get_token",
        json={
            "ID_encrypt": one_time_ID_encrypt.decode(),
            "encrypt_key": encrypt_key.decode(),
            "encrypt_iv": encrypt_iv.decode(),
            "username": username
        },
    )
    # print(token_encrypt.status_code)
    if token_encrypt.status_code == 404:
        print('Wrong username')
        return saveEnv
    elif token_encrypt.status_code == 401:
        print('Wrong oneTimeID')
        return saveEnv
    else:
        token_encrypt = token_encrypt.json()
        # print("encrypted token: " + token_encrypt["token"])
        decrypted_token = symmetric_encryption.decrypt(
            token_encrypt["token"], iv.encode(), symmetric_key.encode())
        # print("decryptedtoken: " + decrypted_token)
        print("> Server Registration was successfull!\n")
        saveEnv.append(symmetric_key)
        saveEnv.append(decrypted_token)
        return saveEnv


def main_menu(username, my_port, config):
    print("Options:")
    print("1 - Request service")
    print("2 - Send message")
    print("3 - Exit")
    option = int(input("option: "))
    
    if option == 1:
        request_service(config)
        
    elif option == 2:
        username_2 = input("Which client do you want to contact?\n")
        try:
            address_and_port = request_get_ip(config, username_2)
            public_key = request_public_key(config, username_2)
            port = int(address_and_port.split(",")[1])
            print(port)
            print(public_key)
            message = input("Write your message:\n")

            cipher = PKCS1_OAEP.new(public_key)

            encrypted_message = base64.b64encode(
                cipher.encrypt(message.encode("utf-8")))
        
            send_message(encrypted_message, port)
            main_menu(username, my_port, config)
        except ExceptionUserNotAvailable:
            print("> This client is not available at the moment, try again later\n")
            main_menu(username, my_port, config)
        except ExceptionUserNotFound:
            print("> This username does not exist in the server database\n")
            main_menu(username, my_port, config)
            
    elif option == 3:
        print("> Exiting ...\n")
        return
    
    else:
        print("Invalid option\n")
        main_menu(username, my_port, config)
     
    main_menu(username, my_ip_port, config)

def decrypt_and_read_dotenv():
    global keyToDecrypt
    counter = 0
    while counter < 3:

        # ask for password
        username = input('Username: ')

        password = getpass()

        keyToDecrypt = username+password

        try:
            pyAesCrypt.decryptFile(".env.aes", ".env", keyToDecrypt)
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


    print('(KEY TO DECRYPT > ' + keyToDecrypt + ")")
    # delete newly created .env
    os.remove(".env")
    #print(config)
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
    exit(-1)
    
#TODO Por dentro d euma função para desparguetar
print('(2 KEY TO DECRYPT > ' + keyToDecrypt + ")")

try:
    pyAesCrypt.decryptFile(".env.aes", ".env", keyToDecrypt)
    os.remove(".env.aes")
except ValueError:
    print('\n> .env was corrupted. Exiting...')
    exit(-1)

try:
    dotenv_file = dotenv.find_dotenv(
        raise_error_if_not_found=True)  # argumento file name existe
except OSError:
    print('.env not found')

dotenv.set_key(dotenv_file, "TOKEN", new_config["TOKEN"])

pyAesCrypt.encryptFile(".env", ".env.aes", keyToDecrypt)

os.remove('.env')

print("> Authentication done.\n")
my_ip_port = str(ip_port_tuple[0]) + ":" + str(ip_port_tuple[1]) 

listener_thread = Thread(target=listen_socket, args=(ip_port_tuple[1],))
listener_thread.daemon = True
listener_thread.start()

# Services
print("> client session address: " + my_ip_port)
# TODO: Como andar de um lado para o outro sem estar sempre a pedir password?
# agora está a dar o new_config que veio na autenticação e assim nao pede
request_set_ip(new_config, my_ip_port)
main_menu(username, my_ip_port, new_config)

    
