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
                    if cell and cell[0] == 'Orange':
                        image = orange
                    elif cell and cell[0] == 'Blue':
                        image = blue
                    window.blit(image, (self.start_x + j * self.cell_size, self.start_y + i * self.cell_size))