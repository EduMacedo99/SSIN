import socket

LOCALHOST = '127.0.0.1'
SERVER_PORT = 3000


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
                response = bytes("SERVER SENT: " + str(data), "ascii")
                if not data:
                    break
                conn.sendall(response)


def connect_socket(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((LOCALHOST, port))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

