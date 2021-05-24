import socket

from Crypto import Signature
from request_service import request_public_key, request_get_ip
from utils import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64
import os 
import pyAesCrypt
from os import path
from datetime import datetime
from hashlib import sha256
from time import sleep

CIPHER_TEXT_LENGTH = 344

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
        f = open("log.txt", "w+")

    sender, message_text = [str(b) for b in message.split(b"\n")[0:2]]
    f.write('Message received' + ' at ' + current_time + ' from ' + sender + '\n')
    f.write('> ' + message_text)
    f.write('\n')
    f.write('-----------------------------------\n')
    f.close()

    pyAesCrypt.encryptFile("log.txt", "log.txt.aes", key)
    os.remove("log.txt")
    print("Options:")
    print("1 - Request service")
    print("2 - Send message")
    print("3 - Check received messages")
    print("4 - Exit")
    print("option:")

def encrypt_message(message_bytes, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = base64.b64encode(
        cipher.encrypt(message_bytes))
    #print("len(encrypted_message)")
    #print(len(encrypted_message))
    #print(encrypted_message)
    return encrypted_message

def decrypt_message(message_bytes):
    with open("private.key", 'r') as content_file:
        private_key = RSA.importKey(content_file.read())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(message_bytes))
    print(decrypted_message)
    return decrypted_message

def encrypt_long_message(message_bytes, public_key):
    splitted_message = [message_bytes[i:i+128] for i in range(0, len(message_bytes), 128)]
    encrypted_message = b""
    for part in splitted_message:
        encrypted_message += encrypt_message(part, public_key)
    return encrypted_message

def decrypt_long_message(message_bytes):
    splitted_message = [message_bytes[i:i+CIPHER_TEXT_LENGTH] for i in range(0, len(message_bytes), CIPHER_TEXT_LENGTH)]
    decrypted_message = b""
    for part in splitted_message:
        try:
            decrypted_message += decrypt_message(part)
        except:
            print("error decrypting")
    return decrypted_message

def sign_message(message):
    with open("private.key", 'r') as content_file:
        private_key = RSA.importKey(content_file.read())
    hash = SHA.new(message)
    #hash.update()
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(hash)
    print("message to hash:")
    print(message)
    print(hash)
    print(hash.digest())
    print(signature)
    return message + b"\n" + signature

def check_signature(config, complete_message):
    #print(complete_message)
    message_parts = complete_message.split("\n".encode('utf-8'))
    sender, message_text = message_parts[0:2]
    signature = b''.join(message_parts[2:])
    public_key = request_public_key(config, sender.decode('utf-8'))
    verifier = PKCS1_v1_5.new(public_key)
    hash = SHA.new(message_text)
    #hash.update()
    print("message to hash:")
    print(message_text)
    print(hash)
    print(hash.digest())
    print(signature)
    verified = verifier.verify(hash, signature)
    print("VERIFIED")
    print(verified)
    return verified




def listen_socket(config, port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, port))
        s.listen()
        print("+ Waiting for messages in port "+str(port))
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(CIPHER_TEXT_LENGTH*10)
                print('\n\n> New Message received from', addr, ' !\n')
                message = decrypt_long_message(data)
                check_signature(config, message)
                save_message(message, addr, key)


def send_message(config):
    username_2 = input("Which client do you want to contact?\n")
    try:
        address_and_port = request_get_ip(config, username_2)
        port = int(address_and_port.split(":")[1])
        message = input("Write your message:\n")
        public_key = request_public_key(config, username_2)
        #print("len(signed_message)")
        #print(len(sign_message(bytes(message, "utf-8"))))
        complete_message_bytes = bytes(config["USERNAME"], "utf-8") + b"\n" + sign_message(bytes(message, "utf-8"))
        #print("\nSIGNED MESSAGE:")
        #print(complete_message_bytes.decode("utf-8"))
        encrypted_message = encrypt_long_message(complete_message_bytes, public_key)

        #print("len(encrypted_message):")
        #print(len(encrypted_message))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOCALHOST, port))
            s.sendall(encrypted_message)
    except ConnectionRefusedError:
        print("> This client is not available at the moment, try again later\n")
    except ExceptionUserNotFound:
        print("> This username does not exist in the server database\n")

