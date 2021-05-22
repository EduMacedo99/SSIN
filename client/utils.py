
SERVER_ADDRESS = "http://127.0.0.1:3000"
SERVER_PORT = 3000
LOCALHOST = "127.0.0.1"
SIZE = 16

class ExceptionNoUsernameFound(Exception):
    pass

class ExceptionUserNotFound(Exception):
    pass

class ExceptionUserNotAvailable(Exception):
    pass