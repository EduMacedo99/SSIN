from os import chmod
import requests
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
from request_service import prepare_request
from utils import *


def save_key_pair():
    key = RSA.generate(2048)
    with open("private.key", 'w+b') as content_file:
        #chmod("private.key", 600)
        content_file.write(key.exportKey('PEM'))
    public_key = key.publickey()
    with open("public.key", 'w+b') as content_file:
        content_file.write(public_key.exportKey('OpenSSH'))

def request_set_pub_key(username):
    with open("public.key", 'rb') as content_file:
        public_key = content_file.read()
    data = {"username":username, "public_key":str(binascii.hexlify(public_key))[2:-1]}
    res = requests.post(SERVER_ADDRESS + "/service/public_key",
        json = data 
    )
    res_content = res.json()
    print("> Server: " + str(res_content))

    if res.ok: 
        print("> Set Pub Key with success.\n")
    else:
        print("> Error trying to set pub key.\n")