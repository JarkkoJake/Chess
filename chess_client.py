# chess_client.py
# Author: Jarkko Heinonen
# Description: Chess client for multiplayer

import socket
import tkinter as tk
from ChessGui import ChessGui
from threading import Thread
from pygame import mixer

# addresses to the server
PORT = 5050
SERVER = "192.168.1.104"
ADDR = (SERVER, PORT)

# communication protocol information
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
RESTART_MESSAGE = "!RESTART"

# create socket to handle the connection to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# send a message to the server
def send(msg):

    # encode the message
    message = msg.encode(FORMAT)

    # encode messages length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # add empty padding to the length so that it is the size of the header
    send_length += b" " * (HEADER - len(send_length))

    # send message length and message
    client.send(send_length)
    client.send(message)

# wait for a message from the server
def recieve():

    # decode the message length
    msg_length = client.recv(HEADER).decode(FORMAT)

    # decode the next message which is recieved with the length
    msg = client.recv(int(msg_length)).decode(FORMAT)
    
    return msg

# chess client inheriting from the regular chess gui
class ChessClient(ChessGui):

    def __init__(self):
        ChessGui.__init__(self)
    
    def play(self):

        # recieve a number from the server, this number determines
        # this clients colour
        number = int(recieve())
        self.__colour = self.get_board().get_colours()[number]

        # initialize mixer and sound to play after turn ends
        mixer.init()
        mixer.music.load("turnsound.wav")

        # load the window
        self.load_window()

    
    def update(self):

        # update the gui
        ChessGui.update(self)

        # if its your turn, play the sound
        if self.get_turn() == self.__colour:
            mixer.music.play()

        # use a thread to take possible input from the server
        self.waiter = Thread(target= self.take_input)
        self.waiter.start()
    
    # creates a chess piece button, states are enabled only for your colour
    # and on your turn
    def piece_button(self, piece, i):

        # load a picture for the piece
        image = self.get_images()[piece.get_colour() + type(piece).__name__]
        
        # create a button that will select the chess piece
        button = tk.Button(self.get_gui_tiles()[i],
                           command= lambda: self.select(piece),
                           bg = self.get_board().get_tiles()[i//8][i%8]\
                           .get_colour(), image = image, borderwidth=0)

        # disable the button if it is not yours or if its the opponents turn
        if (piece.get_colour() != self.__colour) or \
           (self.__colour != self.get_turn()):
            button.config(state=tk.DISABLED)
            
        # highlight if the piece is the previously moved one
        if piece == self.get_last_moved():
            button.config(bg= "red")
            
        # add button to the piece button list
        self.get_current_piece_buttons().append(button)

        # place the button in the middle of the tile
        button.place(width=50, height=50, x = 11, y = 11)

    # sends the users move to the server
    def move(self, piece, tile):

        # move is send as a tuple containing 2 tuples, from tile and to tile
        # cordinates (row, column)

        # from tile is the pieces original position
        from_tile = piece.get_position(self.get_board())

        # to tile is the tiles position on the board
        tiles = self.get_board().get_tiles()

        # this for loop figures out the tiles position
        r = 0
        for row in tiles:
            c = 0
            for til in row:
                if til == tile:
                    to_tile = (r, c)
                c += 1
            r += 1

        # create the tuple from the cordinates and send it to the server
        move = (from_tile, to_tile)
        send(str(move))

    # takes instructions from the server
    def take_input(self):

        # waits for server output
        server_output = recieve()

        # if the output is restart message, reset the game and return
        if server_output == RESTART_MESSAGE:
            ChessGui.reset(self)
            return

        # else, the server instruction should be a move:

        # this code is a bruteforced way to get the cordinates from the
        # servers message
        move_list = server_output.split("), (")
        from_tile = (int(move_list[0][2]), int(move_list[0][5]))
        to_tile = (int(move_list[1][0]), int(move_list[1][3]))

        # select a chess piece based on the server instruction
        tiles = self.get_board().get_tiles()
        piece = tiles[int(from_tile[0])][int(from_tile[1])].get_piece()

        # select the tile base on the server instruction
        tile = self.get_board().get_tile(int(to_tile[0]), int(to_tile[1]))

        # move the piece to the tile
        piece.move(tile, self.get_board())

        # set the piece to last moved
        self.set_last_moved(piece)

        # play the next round
        self.round()

    # sends a restart message to the server, restarting the game for both
    # clients, should be changed to require both clients to request a restart
    def reset(self):
        send(RESTART_MESSAGE)
        
CC = ChessClient()
CC.get_window().mainloop()
