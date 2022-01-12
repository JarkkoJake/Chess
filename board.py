# board.py
# Author: Jarkko Heinonen
# Description: A class modelling a chess board

from tile import Tile
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from queen import Queen
from knight import Knight
from king import King

class Board:

    # creates an empty board
    def __init__(self, game):
        
        self.__tiles = []
        self.__colours = ["white", "black"] # colours of the chess tiles

        # generates a chessboard pattern
        for row in range(8):
            rowtiles = []
            for col in range(8):
                rowtiles.append(Tile(self.__colours[col % 2 - row % 2]))
            self.__tiles.append(rowtiles)

        self.__selected = None
        self.__game = game

        self.load()

    # loads all chess pieces to their original positions
    def load(self):

        # load the pawns for both sides
        for i in range(8):
            self.set_piece(Pawn(self.__colours[0]), 6, i)
            self.set_piece(Pawn(self.__colours[1]), 1, i)

        # load rooks for both sides
        for i in range(2):
            self.set_piece(Rook(self.__colours[0]), 7, i * 7)
            self.set_piece(Rook(self.__colours[1]), 0, i * 7)

        # load bishops for both sides
        for i in range(2):
            self.set_piece(Bishop(self.__colours[0]), 7, 2 + 3 * i)
            self.set_piece(Bishop(self.__colours[1]), 0, 2 + 3 * i)

        # load queens for both sides
        self.set_piece(Queen(self.__colours[0]), 7, 3)
        self.set_piece(Queen(self.__colours[1]), 0, 3)

        # load kings for both sides
        self.set_piece(King(self.__colours[0], self.__game), 7, 4)
        self.set_piece(King(self.__colours[1], self.__game), 0, 4)

        # load knights to both sides
        for i in range(2):
            self.set_piece(Knight(self.__colours[0]), 7, 1 + i * 5)
            self.set_piece(Knight(self.__colours[1]), 0, 1 + i * 5)
            
    
# Setters

    # select a piece to move
    def set_selected(self, piece):
        if piece.get_captured():
            return
        self.__selected = piece

    # set a piece to a tile
    def set_piece(self, piece, row, column):
        self.get_tile(row, column).set_piece(piece)

# Getters

    def get_selected(self):
        return self.__selected

    def get_tiles(self):
        return self.__tiles

    def get_tile(self, row, column):
        return self.__tiles[row][column]

    def get_colours(self):
        return self.__colours

# Prints

    def __str__(self):
        for row in self.__tiles:
            for col in row:
                print(col.get_colour(), end = "")
            print()
        return ""
    
