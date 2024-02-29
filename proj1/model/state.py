import pygame

class State:
    def __init__(self):
        self.player1 = 'Orange'
        self.player2 = 'Blue'
        self.current_player = self.player1
        self.current_possible_moves = None

    def make_move(self, pos, board):
        x, y = pos
        board[y][x].append(self.current_player)
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


        