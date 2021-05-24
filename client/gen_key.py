from os import chmod
import requests
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from datetime import datetime

import symmetric_encryption 
from request_service import prepare_request
from utils import *


def save_key_pair():
    key = RSA.generate(2048)
    with open("private.key", 'wb') as content_file:
        #chmod("/tmp/private.key", 600)
        content_file.write(key.exportKey('PEM'))
    public_key = key.publickey()
    with open("public.key", 'wb') as content_file:
        content_file.write(public_key.exportKey('OpenSSH'))

def request_set_pub_key(username, key_token):
    with open("public.key", 'r') as content_file:
        public_key = content_file.read()
    
    config = {"USERNAME":username, "TOKEN":key_token[1], "KEY":key_token[0]}
    res = requests.post(SERVER_ADDRESS + "/service/public_key",
        json = prepare_request(config, {"public_key":public_key, "time": str(datetime.now())})
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Set Pub Key with success.\n")
    else:
        print("> Server: " + res_content["msg"])
        print("> Error trying to set pub key.\n")