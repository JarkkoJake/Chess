# knight.py
# Author: Jarkko Heinonen
# Description: A knight chess piece that inherits from chesspiece class

from chesspiece import ChessPiece

class Knight(ChessPiece):

    def __init__(self, colour):
        ChessPiece.__init__(self, colour)

    # checks what tiles are available for the knight
    def get_available_tiles(self, board):

        # store available tiles in a list
        available_tiles = []
        tiles = board.get_tiles()

        # available tiles are based on knights current position
        position = self.get_position(board)

        # this loop checks all the possible knight moves
        for i in range(8):
            horizontal_move = (-1 + 2 * (i % 2)) * (1 + i // 4)
            vertical_move = (-1 + 2 * ((i % 4) < 2)) * (2 - i // 4)

            # continue to next tile, if we are of the board vertically
            if not 0 <= (position[0] + vertical_move) <= 7:
                continue

            # continue to next tile if we are of the board horizontally
            if not 0 <= (position[1] + horizontal_move) <= 7:
                 continue

            # check the tile
            tile = tiles[position[0] + vertical_move]\
                   [position[1] + horizontal_move]

            # if there is a chess piece...
            if tile.get_piece() != None:

                # if the chess piece is allied, continue to next tile
                if tile.get_piece().get_colour() == self.get_colour():
                    continue

                # if the chess piece is enemy, add tile to available tiles
                # and continue to next tile
                if tile.get_piece().get_colour() != self.get_colour():
                    available_tiles.append(tile)
                    continue
                
            # empty tiles will be added and tileamount increased by 1
            # to continue checking tiles in the same direction
            else:
                available_tiles.append(tile)

        return available_tiles

        
    
