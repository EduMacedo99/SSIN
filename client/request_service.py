import requests
import symmetric_encryption 

from utils import *


def request_service(config):  
    print("> Choose the desired service:")
    print("     1 - Square root")
    print("     2 - Cubic root")
    print("     3 - Parametrized n-root")
    
    username = config["USERNAME"]
    curr_token = config["TOKEN"]
    symmetric_key = config["KEY"]
    
    service_id = int(input("Service: "))
    radicand = input("Choose the radicand: ")
    
    service_data = {"service_id": service_id, "radicand":radicand }
    
    if service_id == 3:
        service_data["index"] = input("Choose Index: ")
    elif service_id != 1 and service_id !=2:
        print("Invalid option:", service_id)
        return
       
    # Encrypt token
    symmetric_key_iv = symmetric_encryption.create_new_iv(SIZE)
    enc_token = symmetric_encryption.encrypt(curr_token, symmetric_key_iv.encode(), symmetric_key.encode())
        
    # Request service
    res = requests.get(SERVER_ADDRESS + "/service", 
        json={
            "msg":"Client choose service " + str(service_id) + ".",
            "username": username,
            "cl_token": enc_token,
            "new_iv": symmetric_key_iv,
            "service_data": service_data
        } 
    )
    res_content = res.json()
    print("> Server: " + res_content["msg"])
    
    # If server sended answer
    if res.ok: 
        print("> Service done with success.")


def request_set_ip(username, ip):
    if username == None:
        raise ExceptionNoUsernameFound
    data = {"username":username, "ip_address":ip}
    
    token = requests.post(
        SERVER_ADDRESS + "/service/set_ip", params=data)
    #print(token.text)


def request_get_ip(username):
    if username == None:
        raise ExceptionNoUsernameFound
    data = {"username":username}
    
    token = requests.post(
        SERVER_ADDRESS + "/service/get_ip", params=data)
        
    if (token.text == "USER_NOT_FOUND"):
        raise ExceptionUserNotFound
    else:
        return token.text.split(" ")[-1]


# if __name__=='__main__':
#     request_service("Pedro")
#     request_set_ip("Pedro", "127.0.0.1:1000")
#     request_get_ip("Pedro")
