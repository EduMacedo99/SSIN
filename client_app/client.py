import random
import string
import requests
import simmetric_encryption
import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

SERVER_KEY_PATH = "server_public.pem"
SERVER_URL = "http://127.0.0.1:3000/"
one_time_ID = "123456"

# prepare encryption variables
size = 16
iv = ''.join(random.choice(string.ascii_lowercase) for x in range(size))
simmetric_key = ''.join(random.choice(string.ascii_lowercase)
                        for x in range(size))

# First-Registration -> get server public key
# get server public key
# response = requests.get("http://127.0.0.1:3000/register")
# open('SERVER_KEY_PATH', 'wb').write(response.content)

# encrypt one_time_ID, simmetric_key and iv with server public  key
key = RSA.importKey(open(SERVER_KEY_PATH).read())
cipher = PKCS1_OAEP.new(key)

one_time_ID_encrypt = base64.b64encode(
    cipher.encrypt(one_time_ID.encode("utf-8")))
encrypt_key = base64.b64encode(cipher.encrypt(simmetric_key.encode("utf-8")))
encrypted_iv = base64.b64encode(cipher.encrypt(iv.encode('utf-8')))

# simmetric encryption test
message = "this is testing"
enc_message = simmetric_encryption.encrypt(
    message, iv.encode(), simmetric_key.encode())

token_encrypt = requests.post(
    SERVER_URL + "register/get_token",
    json={
        "ID": one_time_ID_encrypt,
        "encrypt_key": encrypt_key,
        "iv": encrypted_iv,
        "message": enc_message,
    },
).json()

print("encrypted token: " + token_encrypt["token"])
decrypted_token = simmetric_encryption.decrypt(
    token_encrypt["token"], iv.encode(), simmetric_key.encode())
print("decryptedtoken: " + decrypted_token)

print("encrypted message: " + token_encrypt["message"])
decrypted_token = simmetric_encryption.decrypt(
    token_encrypt["message"], iv.encode(), simmetric_key.encode())
print("decryptedmessage: " + decrypted_token)
