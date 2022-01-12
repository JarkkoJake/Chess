# tile.py
# Author: Jarkko Heinonen
# Description: a tile of a chess board, has a colour, can be set available and
# can contain 1 or 0 chess pieces

class Tile:

    def __init__(self, colour):
        self.set_colour(colour)
        self.set_available(False)
        self.set_piece(None)

# Setters

    # chess board colours are usually white and black/brown
    def set_colour(self, colour):
        self.__colour = colour

    # determines if a selected piece could move to this tile
    def set_available(self, available):
        self.__available = available

    # move a piece to this tile, set to none if a piece moves out of this tile
    def set_piece(self, chesspiece):
        self.__piece = chesspiece
    
# Getters

    def get_colour(self):
        return self.__colour

    def get_available(self):
        return self.__available

    # return the piece currently sitting on the tile
    def get_piece(self):
        return self.__piece
