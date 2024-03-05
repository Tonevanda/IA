class Board:
    def __init__(self, game_state, size):
        self.game_state = game_state
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.make_board()
        self.selected_cell = None

        self.current_possible_moves = None
        
        """
        self.orange_stack = []
        self.blue_stack = []
        self.player1 = 'Orange'
        self.player2 = 'Blue'
        self.current_player = self.player1
        """

    def get_size(self):
        return self.size

    # Checks if the cell is on the edge of the board
    def is_on_edge(self, row, col):
        return row == 0 or row == self.size-1 or col == 0 or col == self.size-1

    def make_board(self):
        column_counter = 0
        row_counter = 0
        current_color = 'Orange' # Orange starts

        for row in range(self.size):

            for col in range(self.size):
                if(self.is_on_edge(row, col)):
                    self.board[row][col] = []
                else:
                    self.board[row][col] = [current_color]
                    column_counter += 1
                    if(column_counter % 2 == 0):
                        if(current_color == 'Orange'):
                            current_color = 'Blue'
                        else:
                            current_color = 'Orange'

            row_counter += 1
            if(row_counter % 2 == 0):
                current_color = 'Blue'
            else:
                current_color = 'Orange'

        self.make_hexagon()

                
    def make_hexagon(self):
        cut = int(self.size * 0.25)
        for i in range(self.size):
            for j in range(self.size):
                if i < cut and j < cut - i:
                    self.board[i][j] = None
                elif i < cut and j > self.size - (cut - i) - 1:
                    self.board[i][j] = None
                elif i >= self.size - cut and j < cut - (self.size - i - 1):
                    self.board[i][j] = None
                elif i >= self.size - cut and j > self.size - (cut - (self.size - i - 1)) - 1:
                    self.board[i][j] = None

    # Takes a position and returns the stack at that position
    def get_stack(self, pos):
        x, y = pos
        if 0 <= x and x < self.size and 0 <= y and y < self.size:
            return self.board[y][x]
        return None

    def get_selected_cell(self):
        return self.selected_cell

    def get_selected_stack(self):
        if self.selected_cell is not None:
            return self.get_stack(self.selected_cell)
        return None

    # Takes a cell and returns a list of possible moves in the corresponding cell
    def possible_moves(self, cell):
        x, y = cell
        #you can only move as many pieces as the height of the stack
        stack = self.get_stack(cell)
        if stack is not None:
            max=len(stack)
            # i and j are the offsets from the current position. They vary between -max and max+1
            # the condition 0<=x+i<self.size and 0<=y+j<self.size ensures that the move is within the board
            # the condition abs(j)<=max-abs(i) ensures that that diagonal moves aren't used (because they can't)
            # the condition self.board[y+j][x+i] != None ensures that the move is inside the hexagon
            return [(x+i,y+j) for i in range(-max,max+1) for j in range(-max,max+1) if (i,j)!=(0,0) and 0<=x+i<self.size and 0<=y+j<self.size and abs(j)<=max-abs(i) and self.board[y+j][x+i] != None]
        
    def make_move(self, pos, board):
        x, y = pos
        xs, ys = self.selected_cell
        current_player = self.game_state.get_current_player().get_color()
        if (self.selected_cell == (0,0)): # Selected from own stack
            self.board[y][x].append(current_player)
            self.game_state.remove_from_player_stack()
            self.stack_handling(board, x, y)

        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        elif(board.board[ys][xs]!= [] and board.board[ys][xs][-1]==self.game_state.get_current_player().get_color() and pos in self.current_possible_moves):
            board.board[y][x].extend(board.board[ys][xs])
            board.board[ys][xs] = []
            self.stack_handling(board, x, y)
            

    #if the stack at the destination is higher than 5, the pieces are removed until it is 5 high
    #and if any of the pieces removed are the current player's color, they are added to the stack of the current player
    def stack_handling(self, board, x, y):
        while len(board.board[y][x]) > 5:
                if board.board[y][x].pop(0) == self.game_state.get_current_player().get_color():
                    self.game_state.add_to_player_stack()

        if(not self.game_state.did_win()):
            self.game_state.next_turn()  

    # Given a cell, returns if it belongs to a given player
    def is_player_piece(self, cell, player):
        (i, j) = cell
        color = player.get_color()
        return self.board[i][j] != None and self.board[i][j] != [] and self.board[i][j][-1] == color

    # Checks if the board has any pieces of a given player
    def verify_lost(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if self.is_player_piece((i, j), player):
                    return False
        return True