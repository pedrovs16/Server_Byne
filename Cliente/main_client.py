# IMPORTS
import socket
from time import sleep
import random

# GLOBAL VALUES
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


# START CLIENT FUNCTION

def start_client():
    try:
        # RECEIVING FIRST NUMBER
        print('[CONNECTION] server is connected')
        add = 1
        number = client.recv(2048).decode(FORMAT)
        number = int(number.split()[-1])
        print(f'[SERVER]{ADDR} server sent : {number}')
        while True:
            msg = ''

            # ADD THE SERVER NUMBER TO TOTAL

            for time in range(random.randint(6, 10)):
                number += add
                print(f'[ADD] new value: {number}')
                sleep(0.5)

            # SENDING RESULT

            result = str(number).encode(FORMAT)
            msg_length = len(result)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(result)

            # CHOOSING BETWEEN ODD OR EVEN

            while msg != 'O' and msg != 'E' and msg != DISCONNECT_MESSAGE:
                msg = input('[ANSWER] choose odd or even [O/E] (to disconnect "!DISCONNECT"): ').upper()
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)

            # DISCONNECTING CLIENT

            if msg == DISCONNECT_MESSAGE:
                print('[CONNECTION] connection with server finished')
                break

            add = client.recv(2048).decode(FORMAT)
            print(add)
            add = int(add.split()[-1])
    except:
        print('[ERROR] server closed')


# CREATING CLIENT AND CONNECTING TO SERVER

try:
    SERVER = input('[IP ADDRESS] choose your IP(type "my" if the server use your own IP):')
    if SERVER.upper() == 'MY':
        SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    start_client()
except:
    print(f'[FAILED CONNECTION] client could not connect with the server {ADDR}')

