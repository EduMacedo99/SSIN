import socket
from utils import *

def listen_socket(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((LOCALHOST, port))
        s.listen()
        print("Waiting for messages in port "+str(port))
        while True:
            conn, addr = s.accept()
            with conn:
                print('Received message from', addr)
                data = conn.recv(1024)
                print("Message:\n" + str(data)[2:-1])
                # TODO: encrypt and store message


def send_message(message_text, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((LOCALHOST, port))
            s.sendall(bytes(message_text, "ascii"))
            print("Message sent\n\n")
        return 0
    except ConnectionRefusedError:
        raise ExceptionUserNotAvailable

