import requests
import symmetric_encryption 
import socket

SERVER_IP_URL = "http://127.0.0.1:3000"
USERNAME = "rita"

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
# TODO: ...
curr_token = "this is testing"
symmetric_key = "wwiimwiegdgcyvdz"
symmetric_key_iv = "hsbkjbsmdpgdwfib"
is_registered = True

################# Authenticate with the server ############################################
# Inform server you want to start a new session
if is_registered:
    try:
        # (prof) em cada sessão, deverão escolher, pode ser o sistema operativo, um porto e comunica-lo ao servidor
        # Set up socket to talk to other clients after authentication, get >>port<<
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 0))
        port = s.getsockname()[1]
        print("Listening on port:", port)
        
        # Encrypt token
        enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
        
        # Exhange current token with a new token
        res = requests.get(SERVER_IP_URL + "/auth", 
            json={
                "msg":"I'm username " + USERNAME,
                "username": USERNAME,
                "token": enc_token,
                } 
        )
        res_content = res.json()
        print("Server: " + res_content["msg"])
        
        # If server sended challenge
        if res.ok: 
            # Prove you are "username" and solve the challenge N 
            # Encrypt N, and send it back
            enc_challenge = symmetric_encryption.encrypt(res_content["challenge"], symmetric_key_iv.encode(), symmetric_key.encode())
            
            # Send answer
            res = requests.get(SERVER_IP_URL + "/auth/challengeRefreshToken", 
                json={
                    "msg":"",
                    "username": USERNAME,
                    "enc_challenge": enc_challenge,
                    "port": port
                } 
            )
            res_content = res.json()
            print("Server: " + res_content["msg"])
            
            # If server sended a new token, means client is authenticated, decrypt the new token and save it
            if res.ok:
                # Decrypt token
                curr_token = symmetric_encryption.decrypt(res_content["token"], symmetric_key_iv.encode(), symmetric_key.encode())
                # Save somewhere in client protected data
                # TODO: ...
                print("Refresh token done.")
            else:
                print("Authentication denied.")
        else:
            print("Authentication denied.")

    except IOError:
        print("error: failed to establish a connection with the server.")
