import pygame

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[[] for i in range(size)] for _ in range(size)]
        self.start_x = 0
        self.start_y = 0
        self.cell_size = 50
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

    def get_pos(self, pos):
        x, y = pos
        cell_x = (x - self.start_x) // self.cell_size
        cell_y = (y - self.start_y) // self.cell_size
        return (cell_x, cell_y)
    
    def check_stack(self, pos):
        x, y = pos
        if 0 <= x and x < self.size and 0 <= y and y < self.size:
            return self.board[y][x]
        return None

    def possible_moves(self, pixel):
        pos = self.get_pos(pixel)
        x, y = pos
        #you can only move as many pieces as the height of the stack
        stack = self.check_stack(pos)
        if stack is not None:
            max=len(stack)
            print("here")
            #return a list of possible moves
            return [(x,y,x+i,y+j) for i in range(-max,max+1) for j in range(-max,max+1) if (i,j)!=(0,0) and 0<=x+i<self.size and 0<=y+j<self.size and abs(j)<=max-abs(i) and self.board[y+j][x+i] != None]
    
    def draw(self, window):
        board_width = self.size * self.cell_size
        board_height = self.size * self.cell_size
        self.start_x = (window.get_width() - board_width) // 2
        self.start_y = (window.get_height() - board_height) // 2
        orange = pygame.image.load("proj/proj1/sprites/orange.jpg")  
        blue = pygame.image.load("proj/proj1/sprites/blue.jpg")
        empty = pygame.image.load("proj/proj1/sprites/black.jpg")  # Load the image for default cells
        orange = pygame.transform.scale(orange, (self.cell_size, self.cell_size))
        blue = pygame.transform.scale(blue, (self.cell_size, self.cell_size))
        empty = pygame.transform.scale(empty, (self.cell_size, self.cell_size))
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                # not None -> exists, cell -> not empty, cell[0] -> color of the piece on top of the stack 
                if cell is not None:
                    image = empty
                    if cell and cell[-1] == 'Orange':
                        #print(cell)
                        image = orange
                    elif cell and cell[-1] == 'Blue':
                        #print(cell)
                        image = blue
                    window.blit(image, (self.start_x + j * self.cell_size, self.start_y + i * self.cell_size))
    
    def draw_stack(self,pixel,window):
        pos = self.get_pos(pixel)
        stack = self.check_stack(pos)
        print(stack)
        orange = pygame.image.load("proj/proj1/sprites/orange.jpg")
        orange = pygame.transform.scale(orange, (self.cell_size, self.cell_size))
        blue = pygame.image.load("proj/proj1/sprites/blue.jpg")
        blue = pygame.transform.scale(blue, (self.cell_size, self.cell_size))
        black = pygame.image.load("proj/proj1/sprites/black.jpg")
        black = pygame.transform.scale(black, (self.cell_size, self.cell_size))
        if stack is not None:
            for i in range(5):
                if i >= len(stack):
                    window.blit(black, (0 , window.get_height()- self.cell_size - i * self.cell_size))
                elif stack[i] == 'Orange':
                    window.blit(orange, (0 , window.get_height()- self.cell_size - i * self.cell_size))
                elif stack[i] == 'Blue':
                    window.blit(blue, (0, window.get_height()- self.cell_size - i * self.cell_size))
        else:
            print("No stack at this position")
            return None