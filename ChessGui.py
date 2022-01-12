# chessgui.py
# Author: Jarkko Heinonen
# Description: Graphical user interface for chess using tkinter

import tkinter as tk
from game import Game
from board import Board

class ChessGui(Game):

    def __init__(self):

        # initialize the window
        self.__window = tk.Tk()

        # this list stores the tiles for GUI
        self.__gui_tiles = []

        # these lists store buttons that are currently on the screen
        self.__current_piece_buttons = []
        self.__current_move_buttons = []

        # keeps track of which pieces available moves are highlighted
        # used to remove the highlighting if clicked on again
        self.__selected = None

        # keeps track of the previously moved piece and is used to
        # control its highlighting
        self.__last_moved = None

        # store images in dictionary
        self.__images = self.load_images()

        # call the game inti mehtod and load window
        Game.__init__(self)

    # starts the game, loads the board and setup the first round
    def play(self):
        self.load_window()

    # play a round
    def round(self):

        # change turn
        self.set_turn(self.get_board().get_colours()\
                      [self.get_turn() == self.get_board().get_colours()[0]])

        # reset the move and chess piece buttons
        for button in self.__current_piece_buttons:
            button.place_forget()
        self.__current_piece_buttons = []
        for button in self.__current_move_buttons:
            button.place_forget()
        self.__current_move_buttons = []

        # update the board
        self.update()

    # loads the header and main elements to the screen
    def load_window(self):

        # header containing the current players turn and reset button
        self.__turn_label = tk.Label(self.__window, text="")
        self.__turn_label.grid(row=0, column=0)
        self.__reset_button = tk.Button(self.__window, text = "reset",
                                        command = self.reset)
        self.__reset_button.grid(row=0, column=1, sticky=tk.E)

        # main - contains the game itself
        self.__board_label = tk.Label(self.__window)
        self.__board_label.grid(row = 1, column = 0, columnspan=2)

        # draw the tiles
        self.draw_tiles()
    
    # resets the game
    def reset(self):

        #remove piece- and move buttons from the screen
        for button in self.__current_move_buttons:
            button.place_forget()

        for button in self.__current_piece_buttons:
            button.place_forget()

        # reset the list for the buttons
        self.__current_move_buttons = []
        self.__current_piece_buttons = []

        # reset the king captured attribute
        self.game_over(False)

        # remove every chess piece from board
        for row in self.get_board().get_tiles():
            for tile in row:
                tile.set_piece(None)

        # reload the board
        self.get_board().load()

        # set turn to the first one (white default)
        self.set_turn(self.get_board().get_colours()[0])
        self.update()

    # draws chess board tiles to the screen
    def draw_tiles(self):

        i = 0
        for row in self.get_board().get_tiles():
            for tile in row:
                label = tk.Label(self.__board_label, bg=tile.get_colour(),
                                 width=10, height=5)
                self.__gui_tiles.append(label)
                label.grid(row = i//8, column = i % 8)
                i += 1
        self.update()

    # places buttons for the chess pieces, updates the turn in the header
    def update(self):

        self.__turn_label.config(text=self.get_turn())
        
        i = 0
        for row in self.get_board().get_tiles():
            for tile in row:
                if tile.get_piece() != None:
                    self.piece_button(tile.get_piece(), i)
                i += 1

        # if a king is captured
        if self.get_king_captured():

            # disable piece buttons
            for button in self.__current_piece_buttons:
                button.config(state=tk.DISABLED)

            # show the winner in the turn label
            string = self.get_king_captured() + " king was captured!"
            self.__turn_label.config(text=string)

    # creates a chess piece button, state is disabled if its an enemy piece
    def piece_button(self, piece, i):

        # load a picture for the piece
        image = self.__images[piece.get_colour() + type(piece).__name__]
        
        # create a button that will select the chess piece
        button = tk.Button(self.__gui_tiles[i],
                           command= lambda: self.select(piece),
                           bg = self.get_board().get_tiles()[i//8][i%8]\
                           .get_colour(), image = image, borderwidth=0)

        # disable the button if its not movable on the current turn
        if piece.get_colour() != self.get_turn():
            button.config(state=tk.DISABLED)

        # highlight if the piece is the previously moved one
        if piece == self.get_last_moved():
            button.config(bg= "red")

        # add button to the piece button list
        self.__current_piece_buttons.append(button)

        # place the button in the middle of the tile
        button.place(width=50, height=50, x = 11, y = 11)

    # selects a chess piece and highlights its available moves and
    # places buttons to them
    def select(self, piece):
        
        available_tiles = piece.get_available_tiles(self.get_board())
        tiles = self.get_board().get_tiles()

        # remove any previous hightlighting and resets the list
        for button in self.__current_move_buttons:
            button.place_forget()
        self.__current_move_buttons = []

        # if this pieces moves were highlighted previously, dont do so again
        if self.__selected == piece:
            self.__selected = None
            return

        # else set selected to the piece and hightlight available tiles
        self.__selected = piece
        
        # hightlight available tiles
        i = 0
        for row in tiles:
            for tile in row:
                if tile in available_tiles:
                    self.highlight_tile(piece, i, tile)
                i += 1

    # highlights a tile, placing a button on it to move the selected piece
    # to the tile
    def highlight_tile(self, piece, i, tile):

        button = tk.Button(self.__gui_tiles[i],
                           command = lambda: self.move(piece, tile),
                           bg = "green")

        # if there is a piece on the highlightable tile, add its image
        # to the button
        if tile.get_piece() != None:
            button.config(image = self.__images\
                          [tile.get_piece().get_colour() + \
                           type(tile.get_piece()).__name__])
        
        # adds the button to the move-button list
        self.__current_move_buttons.append(button)

        # place the button in the middle of the label
        button.place(width=50, height = 50, x = 11, y = 11)

    # moves a chess piece, called from the buttons to move pieces
    def move(self, piece, tile):

        # move the piece
        piece.move(tile, self.get_board())

        # highlight the piece
        self.set_last_moved(piece)

        # play the next round
        self.round()

    # loads images from folder to a dictionary
    def load_images(self):

        # white images
        white_pawn = tk.PhotoImage(file = "images/whitePawn.png")
        white_rook = tk.PhotoImage(file = "images/whiteRook.png")
        white_bishop = tk.PhotoImage(file = "images/whiteBishop.png")
        white_knight = tk.PhotoImage(file = "images/whiteKnight.png")
        white_queen = tk.PhotoImage(file = "images/whiteQueen.png")
        white_king = tk.PhotoImage(file = "images/whiteKing.png")

        # black images
        black_pawn = tk.PhotoImage(file = "images/blackPawn.png")
        black_rook = tk.PhotoImage(file = "images/blackRook.png")
        black_bishop = tk.PhotoImage(file = "images/blackBishop.png")
        black_knight = tk.PhotoImage(file = "images/blackKnight.png")
        black_queen = tk.PhotoImage(file = "images/blackQueen.png")
        black_king = tk.PhotoImage(file = "images/blackKing.png")

        # creating the dictionary
        image_dict = {"whitePawn": white_pawn, "whiteRook": white_rook,
                      "whiteBishop": white_bishop, "whiteKnight": white_knight,
                      "whiteQueen": white_queen, "whiteKing": white_king,
                      "blackPawn": black_pawn, "blackRook": black_rook,
                      "blackBishop": black_bishop, "blackKnight": black_knight,
                      "blackQueen": black_queen, "blackKing": black_king}
        return image_dict

# setters

    def set_last_moved(self, piece):
        self.__last_moved = piece

# getters

    def get_last_moved(self):
        return self.__last_moved
    
    def get_window(self):
        return self.__window
    
    def get_images(self):
        return self.__images
    
    def get_gui_tiles(self):
        return self.__gui_tiles
    
    def get_current_move_buttons(self):
        return self.__current_move_buttons
    
    def get_current_piece_buttons(self):
        return self.__current_piece_buttons

GUI = ChessGui()
GUI.get_window().mainloop()
