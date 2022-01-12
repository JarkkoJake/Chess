# chesspiece.py
# Author: Jarkko Heinonen
# Description: Base class for chess pieces

class ChessPiece:

    def __init__(self, colour):
        self.set_colour(colour)

        self.set_captured(False)

    # move chesspiece to a tile
    def move(self, tile, board):

        # check if the tile is available
        try:
            if not (tile in self.get_available_tiles(board)):
                return
        except:
            pass
        
        # set captured if capturing an opposing piece
        if tile.get_piece() != None:
            tile.get_piece().set_captured(True)

        # remove self from old tile
        position = self.get_position(board)
        tiles = board.get_tiles()
        try:
            tiles[position[0]][position[1]].set_piece(None)
        except:
            pass
        tile.set_piece(self)

# Setters

    def set_colour(self, colour):
        self.__colour = colour

    # this is used to track if the piece is captured, if so, the piece cannot
    # be moved or selected, even from console
    def set_captured(self, captured):
        self.__captured = captured

# Getters

    def get_position(self, board):
        r = 0
        for row in board.get_tiles():
            c = 0
            for tile in row:
                if tile.get_piece() == self:
                    return (r, c)
                c += 1
            r += 1

    def get_colour(self):
        return self.__colour

    def get_captured(self):
        return self.__captured
