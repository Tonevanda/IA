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
        if (self.current_cell == (0,0)):
            board.board[y][x].append(self.current_player)
            if self.current_player == 'Orange':
                board.orangeStack.pop()
            else:
                board.blueStack.pop()
            self.stack_handling(board, x, y)

        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        elif(board.board[ys][xs]!= [] and board.board[ys][xs][-1]==self.current_player and pos in self.current_possible_moves):
            board.board[y][x].extend(board.board[ys][xs])
            board.board[ys][xs] = []
            #if the stack at the destination is higher than 5, the pieces are removed until it is 5 high
            #and if any of the pieces removed are the current player's color, they are added to the stack of the current player
            self.stack_handling(board, x, y)

    def stack_handling(self, board, x, y):
        while len(board.board[y][x]) > 5:
                if board.board[y][x].pop(0) == self.current_player:
                    if self.current_player == self.player1:
                        board.orangeStack.append('Orange')
                    else:
                        board.blueStack.append('Blue')
            
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1


        