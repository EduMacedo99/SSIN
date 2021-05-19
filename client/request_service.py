import requests

SERVER_ADDRESS = "http://127.0.0.1:3000"

class ExceptionNoUsernameFound(Exception):
    pass

def request_service(username):
    print("Choose the desired service:")
    print("1 - Square root")
    print("2 - Cubic root")
    print("3 - Parametrized n-root")
    service_id = int(input())
    radicand = input("Choose the radicand")
    if username == None:
        raise ExceptionNoUsernameFound
    data = {"username":username, "service":service_id, "radicand":radicand}
    if service_id == 3:
        data["index"] = input("Choose the index")
    elif service_id != 1 and service_id !=2:
        print("Invalid option:", service_id)
        return
    print(data)
    token = requests.get(
        SERVER_ADDRESS + "/service", params=data)
    print(token.text)


def request_set_ip(username, ip):
    if username == None:
        raise ExceptionNoUsernameFound
    data = {"username":username, "ip_address":ip}
    
    print(data)
    token = requests.post(
        SERVER_ADDRESS + "/service/set_ip", params=data)
    print(token.text)


def request_get_ip(username):
    if username == None:
        raise ExceptionNoUsernameFound
    data = {"username":username}
    
    print(data)
    token = requests.post(
        SERVER_ADDRESS + "/service/get_ip", params=data)
    print(token.text)


if __name__=='__main__':
    request_service("Pedro")
    request_set_ip("Pedro", "127.0.0.1:1000")
    request_get_ip("Pedro")
