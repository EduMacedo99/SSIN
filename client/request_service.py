from Crypto.PublicKey import RSA
import requests
import base64
import binascii

import symmetric_encryption 
from utils import *

# Return json data with username, cl_token and new_iv, and the other things in the data 
def prepare_request(config, data):
    
    username = config["USERNAME"]
    curr_token = config["TOKEN"]
    symmetric_key = config["KEY"]
    
    # Encrypt token
    symmetric_key_iv = symmetric_encryption.create_new_iv(SIZE)
    enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
    
    res = {"username": username, "cl_token":enc_token, "new_iv": symmetric_key_iv}
    
    # Encrypt others
    for i in data.keys():
        res[i] = symmetric_encryption.encrypt(data[i], symmetric_key_iv.encode(), symmetric_key.encode())
    
    return res


def request_service(config):  
    if config == None:
        raise ExceptionNoUsernameFound
    
    print("\n> Choose the desired service:")
    print("     1 - Square root")
    print("     2 - Cubic root")
    print("     3 - Parametrized n-root")
    
    service_id = input("Service: ")
    radicand = input("Choose the radicand: ")
    
    data = {"service_id": service_id, "radicand":radicand }
    
    if service_id == "3":
        data["index"] = input("Choose Index: ")
    elif service_id != "1" and service_id !="2":
        print("Invalid option:", service_id)
        return
    
    # Request service
    res = requests.get(SERVER_ADDRESS + "/service", 
        json = prepare_request(config, data)
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok or res.status_code == 501: # or dont have permission
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        if res.status_code != 501:
            print("> Service done with success.\n")
        else:
            print("> Service failed.\n")
    else:
        print("> Server: " + res_content["msg"])
        print("> Service failed.\n")


def request_set_ip(config, ip):
    if config == None:
        raise ExceptionNoUsernameFound
    
    # Request to set ip
    res = requests.post(SERVER_ADDRESS + "/service/set_ip",
        json = prepare_request(config, {"ip_address": ip})
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Set IP done with success.\n")
    else:
        print("> Server: " + res_content["msg"])
        raise ExceptionNoUsernameFound

def request_get_ip(config, username_2):
    if config == None or username_2 == None:
        raise ExceptionNoUsernameFound

    # Request ip of username_2
    res = requests.get(SERVER_ADDRESS + "/service/get_ip",
        json = prepare_request(config, {"username_2":username_2}) 
    )
    res_content = res.json()
    
    # If server response was ok
    if res.ok: 
        # Get new IV
        iv_response = res_content["new_iv"]
        # Decrypt msg
        msg_response= symmetric_encryption.decrypt(res_content["msg"], iv_response.encode(), config["KEY"].encode())
        print("> Server: " + msg_response)
        print("> Get IP with success.\n")
        return  res_content["ip_port"]
    else:
        print("> Server: " + res_content["msg"])
        if res.status_code == 501:
            raise ExceptionUserNotAvailable
        else:
            raise ExceptionUserNotFound


def request_public_key(config, username_2):
    data = prepare_request(config, {})
    data["msg"] = "Client wants to know pub key of " + username_2
    data["username_2"] = username_2
    res = requests.get(SERVER_ADDRESS + "/service/public_key",
        json = data 
    )
    res_content = res.json()
    #print("> Server: " + res_content["msg"])
    
    # If server response was ok
    if res.ok: 
        print("> Get public key with success.\n")
        return  RSA.importKey(binascii.unhexlify(res_content["public_key"]))
    else:
        raise ExceptionUserNotFound

