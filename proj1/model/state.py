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
        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        if(board[ys][xs]!= [] and board[ys][xs][-1]==self.current_player and pos in self.current_possible_moves):
            board[y][x].extend(board[ys][xs])
            board[ys][xs] = []
            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1


        