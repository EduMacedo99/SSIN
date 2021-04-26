
import base64
from cryptography.hazmat.backends.interfaces import RSABackend
import requests
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


ID = str.encode("123456")
# First-Registration
# response = requests.get("http://127.0.0.1:3000/register")
# open('server_public.pem', 'wb').write(response.content)
token = '1234'

key = RSA.importKey(open('server_public.pem').read())
cipher = PKCS1_OAEP.new(key)
output = base64.b64encode(cipher.encrypt(token.encode('utf-8')))
token = requests.post(
    "http://127.0.0.1:3000/register/get_token", json={'token': output})
