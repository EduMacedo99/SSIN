import requests
import simmetric_encryption
import os, binascii
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import secrets


SERVER_KEY_PATH = "server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
one_time_ID = "123456"
iv = b"aaaaaaaaaaaaaaaa"
key_str = b"aaaaaaaaaaaaaaaa"
# First-Registration
# get server public key
# response = requests.get("http://127.0.0.1:3000/register")
# open('SERVER_KEY_PATH', 'wb').write(response.content)

key = RSA.importKey(open(SERVER_KEY_PATH).read())
cipher = PKCS1_OAEP.new(key)
one_time_ID_encrypt = base64.b64encode(cipher.encrypt(one_time_ID.encode("utf-8")))

password = secrets.token_hex(32)
print("pass: " + password)
encrypt_password = base64.b64encode(cipher.encrypt(password.encode("utf-8")))
cena = simmetric_encryption.encrypt("cenas", iv, key_str)
print("cena: " + cena)
token_encrypt = requests.post(
    SERVER_URL + "register/get_token",
    json={
        "token": one_time_ID_encrypt,
        "encrypt_pass": encrypt_password,
        "cenas": cena,
    },
).json()
print("encrypted token: " + token_encrypt["token"])
decrypted_token = simmetric_encryption.decrypt(token_encrypt["token"], iv, key_str)
print("decryptedtoken: " + decrypted_token)
