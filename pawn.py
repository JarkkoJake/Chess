# pawn.py
# Author: Jarkko Heinonen
# Description: A pawn chess piece that inherits from chesspiece class

from chesspiece import ChessPiece

class Pawn(ChessPiece):

    def __init__(self, colour):
        ChessPiece.__init__(self, colour)

        # the first move is tracked since the pawn is able to move 2 tiles
        # instead of 1 on its first move
        self.set_has_moved(False)

    # checks what tiles are available for the pawn
    def get_available_tiles(self, board):

        # store available tiles in a list
        available_tiles = []
        tiles = board.get_tiles()

        # available tiles are based on the pawns current position
        position = self.get_position(board)
        
        # white pawn can only move upwards, so index goes down, direction is
        # either 1 for non-white pawn or -1 for white pawn
        direction = -1 + 2 * (self.get_colour() == board.get_colours()[1])

        # check one or two tiles infront of the pawn, based on if the pawn
        # has moved or not
        for i in range(1, 2 + (int(not self.__has_moved))):

            # break if we are of the board vertically
            if not (0 <= (position[0] + i * direction) <= 7):
                break

            # break if there is a chess piece infront of the pawn
            if tiles[position[0] + i * direction][position[1]].get_piece():
                break

            # add emtpy tiles infront of the pawn to available tiles
            else:
                available_tiles.append(tiles[position[0] + i * direction]\
                                       [position[1]])

        # check both diagonals for captures
        for i in range(2):

            # continue to next diagonal if we are of the board vertically
            if not (0 <= position[1] - 1 + i * 2 <= 7):
                continue

            # only add diagonal to available tiles if there is a enemy piece
            # try is being used here to avoid errors with empty tiles
            try:
                if tiles[position[0] + direction][position[1] - 1 + 2 * i]\
                   .get_piece().get_colour() != self.get_colour():
                    available_tiles.append(tiles[position[0] + direction]\
                                           [position[1] - 1 + 2 * i])
            except:
                continue

        return available_tiles

    def move(self, tile, board):
        ChessPiece.move(self, tile, board)
        self.set_has_moved(True)

# Setters

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved
    
# Getters

    def get_has_moved(self):
        return self.__has_moved
