import random
import string
import requests
import symmetric_encryption
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import json

SERVER_KEY_PATH = "resources/server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
one_time_ID = "123456"

# prepare encryption variables
size = 16
iv = ''.join(random.choice(string.ascii_lowercase) for x in range(size))
symmetric_key = ''.join(random.choice(string.ascii_lowercase)
                        for x in range(size))

# First-Registration -> get server public key
# get server public key
# response = requests.get("http://127.0.0.1:3000/register")
# open('SERVER_KEY_PATH', 'wb').write(response.content)

# encrypt one_time_ID, symmetric_key and iv with server public  key
key = RSA.importKey(open(SERVER_KEY_PATH).read())
cipher = PKCS1_OAEP.new(key)

one_time_ID_encrypt = base64.b64encode(
    cipher.encrypt(one_time_ID.encode("utf-8")))
encrypt_key = base64.b64encode(cipher.encrypt(symmetric_key.encode("utf-8")))
encrypt_iv = base64.b64encode(cipher.encrypt(iv.encode('utf-8')))

# #############symmetric encryption test#####################3
message = "this is testing"
enc_message = symmetric_encryption.encrypt(
    message, iv.encode(), symmetric_key.encode())
print("enc_message: " + enc_message)
##############################################################

token_encrypt = requests.post(
    SERVER_URL + "register/get_token",
    json={
        "ID_encrypt": one_time_ID_encrypt,
        "encrypt_key": encrypt_key,
        "encrypt_iv": encrypt_iv,
        "message": enc_message,
    },
).json()

# decrypt token, maybe store it encrypted would be better
print("encrypted token: " + token_encrypt["token"])
decrypted_token = symmetric_encryption.decrypt(
    token_encrypt["token"], iv.encode(), symmetric_key.encode())
print("decryptedtoken: " + decrypted_token)

print("encrypted message: " + token_encrypt["final_message"])
decrypted_token = symmetric_encryption.decrypt(
    token_encrypt["final_message"], iv.encode(), symmetric_key.encode())
print("decryptedmessage: " + decrypted_token)


# save private data into a file for now
username = "rita"
data = {}
data["username"] = username
data["symmetric_key"] = symmetric_key
data["iv"] = iv
data["token"] = decrypted_token
with open("resources/" + username + "_protected_data.txt", "w+") as outfile:
    json.dump(data, outfile)
