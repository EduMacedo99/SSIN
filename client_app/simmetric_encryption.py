from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random
from base64 import b64decode
from base64 import b64encode
import binascii
import json
import random

# iv= get_random_bytes(16)

# Encryption
def encrypt(data, iv, key):
    data = str.encode(data)
    pad = data + b"\0" * (AES.block_size - len(data) % AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad)
    cypher_hex = b64encode(ciphertext).decode("utf-8")
    return cypher_hex


# Decryption
def decrypt(ciphertext, iv, key):
    ciphertext = b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(ciphertext)
    data = data.decode("utf-8")
    return str(b64decode(data).decode())
