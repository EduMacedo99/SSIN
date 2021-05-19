#!python3
from request_service import ExceptionUserNotFound
from socket_functions import connect_socket, listen_socket
import os
import os.path
from os import path
from dotenv import load_dotenv, dotenv_values
import dotenv
import pyAesCrypt
from request_service import request_service, request_set_ip, request_get_ip
from getpass import getpass
import re
import random
import string
import requests
import symmetric_encryption
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from utils import *


def registration():
    counter_pw = 0
    username = input(
        'Insert the username you chose on the server registration:\n')
    ID = input('Insert the unique ID you were given in the server registration:\n')

    success = serverReg(ID)

    if success:

        print('\nServer Registration was successfull!')

        # polos a escolher uma password
        while counter_pw < 3:
            # Ask for strong password
            print('Insert your a new password for this device. The password should at least:\n\t- Have 8 characters or more\n\t- Include Uppercase letters\n\t- Include numbers')
            save_pw = getpass()

            rexes = ('[A-Z]', '[a-z]', '[0-9]')

            if len(save_pw) >= 8 and all(re.search(r, save_pw) for r in rexes):
                print('Strong password. Trying to register...')
                break
            else:
                print('Password not strong enough... Try again')
                counter_pw += 1
                if counter >= 3:
                    print("Maximum tries exceeded. Exiting...")
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
        dotenv.set_key(dotenv_file, "USERNAME", username)
        dotenv.set_key(dotenv_file, "ID", ID)

        # encriptá-lo
        pyAesCrypt.encryptFile(".env", ".env.aes", username+save_pw)

        # APAGA MALUCO
        f.close()
        os.remove(".env")

    else:
        # dizer que username/id estão mal e tentar outra vez
        print('Something went wrong')


def serverReg(one_time_ID):
    SERVER_KEY_PATH = "resources/server_public.pem"
    SERVER_URL = "http://127.0.0.1:3000/"

    # prepare encryption variables
    size = 16
    iv = ''.join(random.choice(string.ascii_lowercase) for x in range(size))
    symmetric_key = ''.join(random.choice(string.ascii_lowercase)
                            for x in range(size))

    # First-Registration -> get server public key
    # get server public key
    response = requests.get("http://127.0.0.1:3000/register")
    open('SERVER_KEY_PATH', 'wb').write(response.content)

    # encrypt one_time_ID, symmetric_key and iv with server public  key
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
            "ID_encrypt": one_time_ID_encrypt,
            "encrypt_key": encrypt_key,
            "encrypt_iv": encrypt_iv,
        },
    ).json()
    print("encrypted token: " + token_encrypt["token"])
    decrypted_token = symmetric_encryption.decrypt(
        token_encrypt["token"], iv.encode(), symmetric_key.encode())
    print("decryptedtoken: " + decrypted_token)
    print('server registration done')
    return True


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


#main_menu()


########################################################### MAIN SCRIPT ###########################################################


#pyAesCrypt.encryptFile(".env", ".env.aes", password)
#pyAesCrypt.decryptFile(".env.aes", ".env", password)
counter = 0

# ver se .env.aes existe - se não existir é pq nao houve registo
if path.exists(".env.aes"):

    print('> Already Registered\n> Proceeding with authentication')

    while counter < 3:

        # ask for password
        username = input('Username: ')

        password = getpass()

        try:
            pyAesCrypt.decryptFile(".env.aes", ".env", username+password)
            break
        except ValueError:
            print('Wrong username/password (or file is corrupted).')
            counter += 1
            if counter >= 3:
                print('Number of tries exceeded. Terminating program...')
                exit()

    # get info
    try:
        dotenv_file = dotenv.find_dotenv(
            raise_error_if_not_found=True)  # argumento file name existe
    except OSError:
        print('.env not foud')
        exit()

    config = dotenv_values(".env")
    print(config)

    # delete newly created .env
    os.remove(".env")
    my_port = random.randint(1024, 49151)
    request_set_ip(username, LOCALHOST + ":" + my_port)
    main_menu()
    request_service(username)
else:
    registration()
