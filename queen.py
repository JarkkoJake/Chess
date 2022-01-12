# queen.py
# Author: Jarkko Heinonen
# Description: A queen chess piece that inherits from rook and bishop classes

from chesspiece import ChessPiece
from rook import Rook
from bishop import Bishop

class Queen(Rook, Bishop):

    def __init__(self, colour):
        ChessPiece.__init__(self, colour)

    # checks what tiles are available for the queen
    def get_available_tiles(self, board):

        # queen has all the available tiles of rook and bishop
        available_tiles = Rook.get_available_tiles(self, board) + \
                          Bishop.get_available_tiles(self, board)

        return available_tiles
