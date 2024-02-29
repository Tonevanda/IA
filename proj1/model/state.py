import pygame

class State:
    def __init__(self):
        self.player1 = 'Orange'
        self.player2 = 'Blue'
        self.current_player = self.player1
        self.current_possible_moves = None
        self.current_cell = None

    def make_move(self, pos, board):
        x, y = pos
        xs, ys = self.current_cell
        board[y][x].extend(board[ys][xs])
        board[ys][xs] = []
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


        