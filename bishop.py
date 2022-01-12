# bishop.py
# Author: Jarkko Heinonen
# Description: A bishop chess piece that inherits from chesspiece class

from chesspiece import ChessPiece

class Bishop(ChessPiece):

    def __init__(self, colour):
        ChessPiece.__init__(self, colour)

    # checks what tiles are available for the bishop
    def get_available_tiles(self, board):
        
        # store available tiles in a list
        available_tiles = []
        tiles = board.get_tiles()

        # available tiles are based on the bishops current position
        position = self.get_position(board)

        # loop is checking 4 diagonal directions
        for i in range(1, 5):

            # tile amount keeps track of how many(eth) tile we are checking
            # in the direction of horizontal and vertical moves
            tile_amount = 1
            horizontal_move = -1 + 2 * (i % 2)
            vertical_move = -1 + 2 * (i // 3)

            # use for demonstration
            #print(horizontal_move, ", ", vertical_move)

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

        
