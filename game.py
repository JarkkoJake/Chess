# game.py
# Author: Jarkko Heinonen
# Description: A game class to run a simplified version of chess

# READ ME
# this file has a lot of uncommented testing code, which has been redefined
# in the GUI

from board import Board
from pawn import Pawn

class Game:
    def __init__(self):
        self.__board = Board(self)
        self.set_turn(self.__board.get_colours()[0])
        self.__king_captured = False
        self.play()
        
    def play(self):
        print(self)
        while True:
            self.round()
            if self.__king_captured:
                break

        print(self.__king_captured, " king was captured!")

    def round(self):
        piece = None
        while piece == None or piece.get_colour() != self.__turn:
            user_select = input("What piece to move? (row col)")
            position = user_select.split(" ")
            piece = self.select(int(position[0]), int(position[1]))
        tile = None
        while tile == None or tile not in piece.get_available_tiles(self.get_board()):
            move_select = input("Move piece? (row col)")
            move = move_select.split(" ")
            tile = self.get_board().get_tile(int(move[0]), int(move[1]))
        piece.move(tile, self.get_board())
        print(self)
        self.__turn = self.__board.get_colours()[self.__turn == self.__board.get_colours()[0]]

    def select(self, row, col):
        tile = self.get_board().get_tile(row, col)
        return tile.get_piece()

    def game_over(self, colour):
        self.__king_captured = colour

    def set_turn(self, turn):
        self.__turn = turn
    
    def get_turn(self):
        return self.__turn

    def get_king_captured(self):
        return self.__king_captured

    def get_board(self):
        return self.__board

    def __str__(self):
        rows = []
        for r in self.__board.get_tiles():
            row = []
            for tile in r:
                if tile.get_piece() == None:
                    row.append("Ee")
                elif tile.get_piece().get_colour() == "white":
                    row.append("w" + str(type(tile.get_piece()).__name__)[0])
                elif tile.get_piece().get_colour() == "black":
                    row.append("b" + str(type(tile.get_piece()).__name__)[0])
            rows.append("".join(row))
        string = "\n".join(rows)
        return string
