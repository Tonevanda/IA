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
                board.orange_stack.pop()
            else:
                board.blue_stack.pop()
            self.stack_handling(board, x, y)

        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        elif(board.board[ys][xs]!= [] and board.board[ys][xs][-1]==self.current_player and pos in self.current_possible_moves):
            board.board[y][x].extend(board.board[ys][xs])
            board.board[ys][xs] = []
            self.stack_handling(board, x, y)

    #if the stack at the destination is higher than 5, the pieces are removed until it is 5 high
    #and if any of the pieces removed are the current player's color, they are added to the stack of the current player
    def stack_handling(self, board, x, y):
        while len(board.board[y][x]) > 5:
                if board.board[y][x].pop(0) == self.current_player:
                    if self.current_player == self.player1:
                        board.orange_stack.append('Orange')
                    else:
                        board.blue_stack.append('Blue')
            
        if self.current_player == self.player1:
            self.current_player = self.player2
            if(self.check_board(board) and board.blue_stack == []):
                print('Player 1 wins')
        else:
            self.current_player = self.player1
            if(self.check_board(board) and board.orange_stack == []):
                print('Player 2 wins')

    # checks if the board has any pieces of the player whose turn it is now
    def check_board(self, board):
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] != None and board.board[i][j] != [] and board.board[i][j][-1] == self.current_player:
                    return False
        return True