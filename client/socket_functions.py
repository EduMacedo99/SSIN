import socket
from utils import *



def listen_socket(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                print(str(data)[2:-1])
                print("you: ", end="")
                response = bytes(input(), "ascii")
                if not data:
                    break
                conn.sendall(response)
                print("other user: ", end="")


def connect_socket(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOCALHOST, port))
            while True:
                print("you: ", end="")
                message = input()
                s.sendall(bytes(message, "ascii"))
                print("other user: ", end="")
                data = s.recv(1024)
                print(str(data)[2:-1])
        return 0
    except ConnectionRefusedError:
        raise ExceptionUserNotAvailable

