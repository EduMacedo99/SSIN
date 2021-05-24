import socket
from request_service import request_public_key, request_get_ip
from utils import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import os 
import pyAesCrypt
from os import path
from datetime import datetime

def save_message(message, addr, key):

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if path.exists('log.txt.aes'):
        try:
            pyAesCrypt.decryptFile("log.txt.aes", "log.txt", key)
            os.remove('log.txt.aes')
        except ValueError:
            print('Was not able to decrypt the file')
        
        f = open("log.txt", "a")
    else:
        f = open("log.txt", "x")

    f.write('Message received' + ' at ' + current_time + '\n')
    f.write('> ' + message.decode('UTF-8'))
    f.write('\n')
    f.write('-----------------------------------\n')
    f.close()

    pyAesCrypt.encryptFile("log.txt", "log.txt.aes", key)
    os.remove("log.txt")

def decrypt_message(message):
    with open("private.key", 'r') as content_file:
        private_key = RSA.importKey(content_file.read())
    cipher = PKCS1_OAEP.new(private_key)
    message = cipher.decrypt(base64.b64decode(message))
    return message


def listen_socket(port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, port))
        s.listen()
        print("+ Waiting for messages in port "+str(port))
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                print('\n+ Received message from', addr)
                print("Message:")
                message = decrypt_message(data)
                print('> New Message reeived !\n')
                save_message(message, addr, key)


def send_message(config):
    username_2 = input("Which client do you want to contact?\n")
    try:
        address_and_port = request_get_ip(config, username_2)
        port = int(address_and_port.split(":")[1])
        public_key = request_public_key(config, username_2)
        message = input("Write your message:\n")
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_message = base64.b64encode(
            cipher.encrypt(message.encode("utf-8")))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOCALHOST, port))
            s.sendall(encrypted_message)
    except ConnectionRefusedError:
        print("> This client is not available at the moment, try again later\n")
    except ExceptionUserNotFound:
        print("> This username does not exist in the server database\n")

