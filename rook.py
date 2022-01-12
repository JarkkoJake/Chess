# rook.py
# Author: Jarkko Heinonen
# Description: A rook chess piece that inherits from chesspiece class

from chesspiece import ChessPiece

class Rook(ChessPiece):

    def __init__(self, colour):
        ChessPiece.__init__(self, colour)

        # has moved is being used to check castling
        self.set_has_moved(False)

    # checks what tiles are available for the rook
    def get_available_tiles(self, board):

        # store available tiles in a list
        available_tiles = []
        tiles = board.get_tiles()

        # available tiles are based on rooks current position
        position = self.get_position(board)

        # loop is checking through all 4 orthogonal directions
        for i in range(1, 5):

            # tile amount keeps track of how many(eth) tile is being checked
            # in the direction given by horizontal and vertical moves
            tile_amount = 1
            horizontal_move = (-1 + 2 * (i % 2)) * (i // 3)
            vertical_move = (-1 + 2 * (i % 2)) * (1 - (i // 3))
            
            while True:

                # break, if we are of the board vertically
                if not 0 <= (position[0] + vertical_move * tile_amount) <= 7:
                    break

                # break if we are of the board horizontally
                if not 0 <= (position[1] + horizontal_move * tile_amount) <= 7:
                    break

                # check the tile
                tile = tiles[position[0] + vertical_move * tile_amount]\
                       [position[1] + horizontal_move * tile_amount]

                # if there is a chess piece...
                if tile.get_piece() != None:

                    # if the chess piece is allied, just break
                    if tile.get_piece().get_colour() == self.get_colour():
                        break

                    # if the chess piece is enemy, add tile to available tiles
                    # and break
                    if tile.get_piece().get_colour() != self.get_colour():
                        available_tiles.append(tile)
                        break

                # empty tiles will be added and tileamount increased by 1
                # to continue checking tiles in the same direction
                else:
                    available_tiles.append(tile)
                    tile_amount += 1
                    
        return available_tiles
    
    def move(self, tile, board):
        ChessPiece.move(self, tile, board)
        self.set_has_moved(True)
        
# getters

    def get_has_moved(self):
        return self.__has_moved

# setters

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved
    
