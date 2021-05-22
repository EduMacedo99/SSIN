import requests
import symmetric_encryption 
import socket

def authentication_server(config, server_ip_url):
    """ Authenticate with the server and start a new session 
        Return client ip_port for this session
    """
    
    username = config["USERNAME"]
    curr_token = config["TOKEN"]
    symmetric_key = config["KEY"]
    symmetric_key_iv = symmetric_encryption.create
    
    # (prof) em cada sessão, deverão escolher, pode ser o sistema operativo, um porto e comunica-lo ao servidor
    # Set up socket to talk to other clients after authentication, get >>port<<
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 0))
    ip_port = s.getsockname()
    print("Listening on:", ip_port)
        
    # Encrypt token
    enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
        
    # Exhange current token with a new token
    res = requests.get(server_ip_url + "auth", 
        json={
            "msg":"I'm username " + username + ".",
            "username": username,
            "cl_token": enc_token,
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
        res = requests.get(server_ip_url + "auth/challengeRefreshToken", 
            json={
                "msg":"Challenge solved.",
                "username": username,
                "enc_challenge": enc_challenge,
                "ip_port": ip_port
            } 
        )
        res_content = res.json()
        print("Server: " + res_content["msg"])
            
        # If server sended a new token, means client is authenticated, decrypt the new token and save it
        if res.ok:
            # Decrypt token
            curr_token = symmetric_encryption.decrypt(res_content["token"], symmetric_key_iv.encode(), symmetric_key.encode())
            
            # TODO: Save in env the new config
            config["token"] = curr_token;
            
            print("Refresh token done.")
            print(config)
        
        else:
            print("Authentication denied.")
    else:
        print("Authentication denied.")

