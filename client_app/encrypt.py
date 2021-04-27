#!python3

import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def encrypt(server_key_path, message):
    key = RSA.importKey(open(server_key_path).read())
    cipher = PKCS1_OAEP.new(key)
    return base64.b64encode(cipher.encrypt(message.encode('utf-8')))