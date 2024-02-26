import pygame

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[i for i in range(size)] for _ in range(size)]
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
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell is not None:
                    color = (255, 0, 0) if cell == "Clicked" else (255,255,255)
                    pygame.draw.rect(window, color, (self.start_x + j * self.cell_size, self.start_y + i * self.cell_size, self.cell_size, self.cell_size))