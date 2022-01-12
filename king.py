# king.py
# Author: Jarkko Heinonen
# Description: A king chess piece that inherits from chesspiece class

from chesspiece import ChessPiece
from rook import Rook

class King(ChessPiece):

    def __init__(self, colour, game):
        ChessPiece.__init__(self, colour)

        # these are used to track if the king can castle or not
        self.set_has_moved(False)
        self.__rooks = []

        # is used to end the game, if captured
        self.__game = game
    

    # checks what tiles are available for the king
    def get_available_tiles(self, board):

        # store available tiles in a list
        available_tiles = []
        tiles = board.get_tiles()

        # kings available tiles are based on current position on the board
        position = self.get_position(board)

        # loop check all 8 tiles around the king
        for i in range(8):
            vertical_move = (-1 + 2 * (i % 2)) * (i > 1)
            horizontal_move = ((-1 + 2 * ((i // 4) + (i == 1))) * (i < 6))

            # continue to next tile if we are of the board vertically or
            # horizontally
            if not 0 <= (position[0] + vertical_move) <= 7:
                continue
            if not 0 <= (position[1] + horizontal_move) <= 7:
                continue

            # check the tile
            tile = tiles[position[0] + vertical_move]\
                   [position[1] + horizontal_move]

            #if there is a chess piece...
            if tile.get_piece() != None:

                # allied piece - just continue to next tile
                if tile.get_piece().get_colour() == self.get_colour():
                    continue

                # enemy piece - add tile to available tiles and continue
                if tile.get_piece().get_colour() != self.get_colour():
                    available_tiles.append(tile)
                    continue

            # empty tiles will just be added to available tiles
            else:
                available_tiles.append(tile)

        # add rooks to the list if not done so before
        if len(self.__rooks) == 0:
            self.add_rooks(board)

        # if the king has not moved, check for castles
        if not self.__has_moved:
            self.check_castle(available_tiles, board)

        return available_tiles

    def check_castle(self, available_tiles, board):

        # check castling for both rooks
        for rook in self.__rooks:

            # if the rook has moved, castling is not allowed
            # therefore continue to next rook
            if rook.get_has_moved():
                continue

            
            tiles = board.get_tiles()
            king_position = self.get_position(board)
            rook_position = rook.get_position(board)

            # direction = 1 for the rook on the right and -1 for left
            direction = 1 - 2 * (rook_position[1] < \
                                 king_position[1])

            # this loop checks the tiles between the king and rook
            for i in range(1, 5):

                # break out of loop if out of the board
                if not (0 <= king_position[1] + direction * i <= 7):
                    break

                # this tile is currently being checked
                tile = tiles[king_position[0]][king_position[1] + \
                                               direction * i]

                # if the tile is free, continue to next tile
                if tile.get_piece() == None:
                    continue

                # if the tile is the rook
                if type(tile.get_piece()) == Rook:

                    # add the tile tile previous to this one
                    # to available tiles and dont check any furhter
                    # (break out of loop)
                    available_tiles.append(tiles[king_position[0]]\
                                           [king_position[1] + direction\
                                            * i + direction * -1])
                    break

                # else aka if there is a piece on the tile thats not the rook
                # just break out of loop
                else:
                    break

    # adds rooks to the rooks list
    def add_rooks(self, board):
        
        tiles = board.get_tiles()

        # adds 2 rooks to the lists based on own colour
        for i in range(0, 2):
            rook = tiles[7 * (self.get_colour() == board.get_colours()[0])]\
                   [7 * i].get_piece()

            # only add the rook if it is still there
            if (type(rook) == Rook):
                self.__rooks.append(rook)

    # moves the king
    def move(self, tile, board):

        # save the original position
        original_position = self.get_position(board)

        # move the king
        ChessPiece.move(self, tile, board)

        # if the king had not previously moved...
        if not self.get_has_moved():

            # set the has moved attribute
            self.set_has_moved(True)

            # if the king moved more than 1 tile (castling)...
            if abs(self.get_position(board)[1] - original_position[1]) != 1:

                # direction which the king moved (1 right, -1 left)
                direction = 1 - 2 * (self.get_position(board)[1] < \
                                     original_position[1])

                tiles = board.get_tiles()

                # rook is the piece in the next tile based on the direction
                # and new position of the king
                rook = tiles[original_position[0]][self.get_position(board)[1]\
                                                   + direction].get_piece()

                # rooks new tile is the next to the king opposite of the
                # direction (rook jumps over the king)
                rooks_tile = tiles[original_position[0]]\
                             [self.get_position(board)[1] - \
                              direction]

                # set rook to its new tile
                rooks_tile.set_piece(rook)

                # make the rook know it has moved
                rook.set_has_moved(True)

                # remove rook from its original tile
                tiles[original_position[0]][self.get_position(board)[1] + \
                               direction].set_piece(None)
# getters

    def get_game(self):
        return self.__game
    
    def get_has_moved(self):
        return self.__has_moved

# setters

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved

    def set_captured(self, captured):
        
        ChessPiece.set_captured(self, captured)

        # end the game if the king gets captured
        if captured == True:
            self.__game.game_over(self.get_colour())
