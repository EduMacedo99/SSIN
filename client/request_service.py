import requests
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
    print("\n> Choose the desired service:")
    print("     1 - Square root")
    print("     2 - Cubic root")
    print("     3 - Parametrized n-root")
    
    service_id = int(input("Service: "))
    radicand = input("Choose the radicand: ")
    
    service_data = {"service_id": service_id, "radicand":radicand }
    
    if service_id == 3:
        service_data["index"] = input("Choose Index: ")
    elif service_id != 1 and service_id !=2:
        print("Invalid option:", service_id)
        return
       
    data = prepare_request(config)
    data["msg"] = "Client choose service " + str(service_id) + ".",
    data["service_data"] = service_data
        
    # Request service
    res = requests.get(SERVER_ADDRESS + "/service", 
        json = data 
    )
    res_content = res.json()
    print("> Server: " + res_content["msg"])
    
    # If server response was ok
    if res.ok: 
        print("> Service done with success.\n")
    else:
        print("> Service failed.\n")


def request_set_ip(config, ip):
    if config == None:
        raise ExceptionNoUsernameFound
    
    # Request to set ip
    res = requests.post(SERVER_ADDRESS + "/service/set_ip",
        json = prepare_request(config, {"ip_address": ip})
    )
    res_content = res.json()
    print("> Server: " + res_content["msg"])
    
    # If server response was ok
    if res.ok: 
        print("> Set IP done with success.\n")
    else:
        raise ExceptionNoUsernameFound

def request_get_ip(config, username_2):
    if config == None or username_2 == None:
        raise ExceptionNoUsernameFound
        
    data = prepare_request(config)
    data["msg"] = "Client wants to know ip of " + username_2
    data["username_2"] = username_2
    
    # Request ip of username_2
    res = requests.get(SERVER_ADDRESS + "/service/get_ip",
        json = data 
    )
    res_content = res.json()
    print("> Server: " + res_content["msg"])
    
    # If server response was ok
    if res.ok: 
        print("> Get IP with success.\n")
        return  res_content["ip_port"]
    else:
        raise ExceptionUserNotFound


def request_public_key(config, username_2):
    data = prepare_request(config)
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
        return  res_content["public_key"]
    else:
        raise ExceptionUserNotFound

