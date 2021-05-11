import base64
import requests
import json
import symmetric_encryption 
from Crypto.Cipher import AES
import socket

SERVER_IP_URL = "http://127.0.0.1:3000"
# TODO: correct username... (only "rita" works for now)
USERNAME = input("username please:")
PROTECTED_DATA_PATH = "client_app/resources/" + USERNAME + "_protected_data.txt"
BUFFER_SIZE = 1024

"""
Perform an automatic authentication of the client with the server for each session
- Identifying and authenticating the collaborator locally
- Authenticate with the server
"""

is_registered = False

################# Identifying and authenticating the collaborator locally ################# 
# Find env file of client
# TODO: ...
# Decrypt their private information
# password = " "
# TODO: ...
try:
    json_file = open(PROTECTED_DATA_PATH)
    data = json.load(json_file)
    curr_token = data["token"]
    symmetric_key = data["symmetric_key"]
    symmetric_key_iv = data["iv"]
    is_registered = True
except IOError:
    print("error: cant open <" + USERNAME + "> protected data.")

################# Authenticate with the server ############################################
# Inform server which port is going to be used in this session
# Choose port -> em cada sessão, deverão escolher, pode ser o sistema operativo, um porto e comunica-lo ao servidor
# TODO: ...
# port = 5005 
port = int(input("port:"))

# Inform server you want to start a new session, and send the ip+port you choose
if is_registered:
    try:
        res = requests.get(SERVER_IP_URL + "/auth", 
            json={
                "username": USERNAME,#I'm username
                "port": port,
                } 
        ).json()
        challenge_n = res["challenge"]
        print("server: " + res["text"] + "\n challenge N: " + challenge_n)
        
        # Connect to the channel to talk to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), port))

        # Prove you are "username" and solve the challenge N 
        # Encrypt N, and send it back
        enc_message = symmetric_encryption.encrypt(challenge_n, symmetric_key_iv.encode(), symmetric_key.encode())

        # Send to server the answer
        s.send(base64.b64decode(enc_message))

        # Wait for reply
        reply = s.recv(BUFFER_SIZE)
        print("server: " + reply.decode("utf-8"))
        
        # If authorized, decrypt the new token and save it
        # TODO: ...
        
        
    except IOError:
        print("error: failed to establish a connection with the server.")
