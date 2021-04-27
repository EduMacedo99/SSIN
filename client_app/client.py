
import requests
import encrypt

SERVER_KEY_PATH = 'server_public.pem'
one_time_ID = "123456"
# First-Registration
# get server public key
# response = requests.get("http://127.0.0.1:3000/register")
# open('server_public.pem', 'wb').write(response.content)

message = encrypt.encrypt(SERVER_KEY_PATH, one_time_ID)
token = requests.post(
    "http://127.0.0.1:3000/register/get_token", json={'token': message})


