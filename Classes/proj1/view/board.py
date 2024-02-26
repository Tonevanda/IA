import pygame

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
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
        cell_size = 50
        board_width = self.size * cell_size
        board_height = self.size * cell_size
        start_x = (window.get_width() - board_width) // 2
        start_y = (window.get_height() - board_height) // 2
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell is not None:
                    pygame.draw.rect(window, (255, 255, 255), (start_x + j * cell_size, start_y + i * cell_size, cell_size, cell_size))