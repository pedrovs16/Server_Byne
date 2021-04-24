# IMPORTS
import socket
import threading
import time
import random
import pickle
import logging

# LOG SETTING

logging.basicConfig(filename='server_client.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# GLOBAL VALUES
HEADER = 64
PORT = 5050
SERVER = input('[IP ADDRESS] choose your (write "my" if the client use your own IP):')
if SERVER.upper() == 'MY':
    SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# CREATING SERVER
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
except:
    print('[SERVER] problem with creating server')
    logging.info('[SERVER] problem with creating server')


# TRYING TO OPEN PICKLE

def pickle_past():
    try:
        output = open('last_number.pkl', 'rb')
    except:
        mydict = {'': 1}
        output = open('last_number.pkl', 'wb')
        pickle.dump(mydict, output)
        output.close()
        output = open('last_number.pkl', 'rb')
        last_number = pickle.load(output)
        output.close()
        return last_number
    else:
        last_number = pickle.load(output)
        output.close()
        return last_number


last_number = pickle_past()


# HANDLE CLIENT FUNCTION

def handle_client(conn, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        logging.info(f"[NEW CONNECTION] {addr} connected.")

        # CHECKING IF THIS IS THE CLIENT'S FIRST CONNECTION

        connected = True
        if addr[0] in last_number:
            first_number = last_number[addr[0]]
        else:
            first_number = 0

        # SENDING FIRST NUMBER

        conn.send(f'(SERVER)[{addr}] first number: {str(first_number)}'.encode(FORMAT))
        logging.info(f'(SERVER)[{addr}] first number: {str(first_number)}')
        print(f'(SERVER)[{addr}] first number: {str(first_number)}')

        while connected:

            # RECEIVING RESULT

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f'(CLIENT)[{addr}] number return was: {msg}')
                logging.info(f'(CLIENT)[{addr}] number return was: {msg}')

            # RECEIVING QUESTION RESSULT

            msg_length = conn.recv(HEADER).decode(FORMAT)
            #
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                logging.info(f'(CLIENT)[{addr}] {msg}')

                # RESULT WAS ODD

                if msg == 'O':
                    print(f"(SERVER)[{addr}] client choose odd")
                    logging.info(f"(SERVER)[{addr}] client choose odd")
                    add = (random.randint(0, 49)) * 2 + 1
                    conn.send(f'(SERVER)[{addr}] the odd number choose was: {str(add)}'.encode(FORMAT))
                    logging.info(f'(SERVER)[{addr}] the odd number choose was: {str(add)}')
                    print(f'(SERVER)[{addr}] the odd number choose was: {str(add)}')
                    last_number.update({addr[0]: add})
                    output = open('last_number.pkl', 'wb')
                    pickle.dump(last_number, output)
                    output.close()

                # RESULT WAS EVEN

                elif msg == 'E':
                    print(f"(SERVER)[{addr}] client choose even")
                    logging.info(f"(SERVER)[{addr}] client choose even")
                    add = (random.randint(0, 49)) * 2
                    conn.send(f'(SERVER)[{addr}] the even number choose was: {str(add)}'.encode(FORMAT))
                    logging.info(f'(SERVER)[{addr}] the even number choose was: {str(add)}')
                    print(f'(SERVER)[{addr}] the odd number choose was: {str(add)}')
                    last_number.update({addr[0]: add})
                    output = open('last_number.pkl', 'wb')
                    pickle.dump(last_number, output)
                    output.close()

                # RESULT WAS DISCONNECT

                elif msg == DISCONNECT_MESSAGE:

                    connected = False
                    print(f'[LOSS CONNECTION] server loss connection with {addr}')
                    logging.info(f'[LOSS CONNECTION] server loss connection with {addr}')
            time.sleep(0.5)

        conn.close()
    except:
        print(f'[ERROR] server loss connection with {addr}')
        logging.info(f'[ERROR] server loss connection with {addr}')
        print(f"(SERVER)[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
        logging.info(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


# START FUNCTION

def start():
    try:

        # LISTENING

        server.listen()
        print(f"[LISTENING] server is listening on {SERVER}")
        logging.info(f'[LISTENING] server is listening on {SERVER}')

        # WAITING CLIENTS

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"(SERVER)[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
            logging.info(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except:
        print(f"[LISTENING] could not listen, try another IP")
        logging.info(f"[LISTENING] could not listen, try another IP")


# STARTING SERVER

print("[STARTING] server is starting...")
logging.info("[STARTING] server is starting...")
start()
