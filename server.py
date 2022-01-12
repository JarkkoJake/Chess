# server.py
# Author: Jarkko Heinonen
# Description: server for communication between chess clients

import socket
import threading
import random

# port and ip that the server is hosted on
PORT = 5050
SERVER = "192.168.1.104"
ADDR = (SERVER, PORT)

# communication protocol information
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
RESTART_MESSAGE = "!RESTART"

# standard socket for ipv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# store connections
connections = []

# handles a new client connecting to the server
def handle_client(conn, addr):

    # prints out the new connection
    string = "NEW CONNECTION: " + str(addr)
    # print(string)
    
    connected = True
    while connected:

        # first message is the message length
        msg_length = conn.recv(HEADER).decode(FORMAT)

        # if message length is not 0, recieve a message based on the given
        # length
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # stop recieving messages if the client disconnectes
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # else handle the message
            handle_message(msg)

    # when connection ends, remove connection from the list and
    # close it
    connections.remove(conn)
    conn.close()

# sends a message to a connected client
def send(msg, conn):

    # encode message
    message = msg.encode(FORMAT)

    # encode messages length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # add empty padding to the message length so that it is the size
    # of the header
    send_length += b" " * (HEADER - len(send_length))

    # send message length and message
    conn.send(send_length)
    conn.send(message)

# handles a message
def handle_message(msg):

    # handle a restart request
    if msg == RESTART_MESSAGE:

        # temporarily restarting only requires one client to send a request
        # should require both parts to request a reset
        for conn in connections:
            send(RESTART_MESSAGE, conn)

    # send message to each client
    else:
        for conn in connections:
            send(msg, conn)

# starts a game of chess between 2 clients
def start_game():

    # select randomly, which client will start
    number = random.randint(0, 1)

    # send the random number to client one and its counterpart to client
    # two
    send(str(number), connections[0])
    send(str(int(not number)), connections[1])

# start the server
def start():
    server.listen()
    # print("Server listening on ", ADDR)

    # infinite loop to accept connections
    while True:
        conn, addr = server.accept()

        # if there is 2 connections, the game is already going and no more
        # connections shall be taken
        if len(connections) >= 2:
            send("Game is already going", conn)
            continue

        # add connection to the list of connections
        connections.append(conn)

        # creates a new thread for handling the client
        thread = threading.Thread(target= handle_client,
                                  args = (conn, addr))
        thread.start()

        # if there is 2 connections, start a game of chess between them
        if len(connections) == 2:
            start_game()

        # print the number of connections to the server
        string = "ACTIVE CONNECTIONS: " + str(len(connections))
        # print(string)

print("Server starting...")
start()
