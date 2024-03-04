class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.start_x = 0
        self.start_y = 0
        self.cell_size = 50
        self.orangeStack = ['Orange']
        self.blueStack = ['Blue']
        self.make_board()

    def is_on_edge(self, row, col):
        return row == 0 or row == self.size-1 or col == 0 or col == self.size-1

    def make_board(self):
        column_counter = 0
        row_counter = 0
        current_color = 'Orange'

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

    # Takes a pixel and returns the position of the corresponding cell
    def get_pos(self, pixel):
        x, y = pixel
        cell_x = (x - self.start_x) // self.cell_size
        cell_y = (y - self.start_y) // self.cell_size
        if(cell_x>=self.size or cell_y>=self.size or cell_x<0 or cell_y<0):
            return (-1,-1)
        return (cell_x, cell_y)

    # Takes a position and returns the stack at that position
    def get_stack(self, pos):
        x, y = pos
        if 0 <= x and x < self.size and 0 <= y and y < self.size:
            return self.board[y][x]
        return None

    # Takes a pixel and returns a list of possible moves in the corresponding cell
    def possible_moves(self, pixel):
        pos = self.get_pos(pixel)
        x, y = pos
        #you can only move as many pieces as the height of the stack
        stack = self.get_stack(pos)
        if stack is not None:
            max=len(stack)
            # i and j are the offsets from the current position. They vary between -max and max+1
            # the condition 0<=x+i<self.size and 0<=y+j<self.size ensures that the move is within the board
            # the condition abs(j)<=max-abs(i) ensures that that diagonal moves aren't used (because they can't)
            # the condition self.board[y+j][x+i] != None ensures that the move is inside the hexagon
            return [(x+i,y+j) for i in range(-max,max+1) for j in range(-max,max+1) if (i,j)!=(0,0) and 0<=x+i<self.size and 0<=y+j<self.size and abs(j)<=max-abs(i) and self.board[y+j][x+i] != None]