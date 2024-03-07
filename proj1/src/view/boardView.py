import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class BoardView:
    def __init__(self, board_model, starting_cell):
        self.board = board_model
        (starting_cell_x, starting_cell_y) = starting_cell
        self.starting_cell_x = starting_cell_x
        self.starting_cell_y = starting_cell_y

    def draw_board(self, window):
        for i, row in enumerate(self.board.board):
            for j, cell in enumerate(row):
                if cell is not None:
                    pygame.draw.rect(window, (0, 0, 0), (self.starting_cell_x + j * CELL_SIZE, self.starting_cell_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
                    for k, piece in enumerate(cell):
                        if piece == 'Orange':
                            color = (255, 100, 0)
                            light_color = (255, 150, 50)
                        elif piece == 'Blue':
                            color = (50, 50, 255)
                            light_color = (100, 100, 255)
                        pygame.draw.circle(window, (0, 0, 0), (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 + k * -5), CELL_SIZE // 2 - 3)
                        pygame.draw.circle(window, color, (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 + k * -5), CELL_SIZE // 2 - 5)
                        pygame.draw.circle(window, light_color, (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2 - 5, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 - 5 + k * -5), CELL_SIZE // 4)

    def draw(self, window):
        #self.draw_board(window)
        pass
    
    """ Positional Drawing
    def generic_draw(self, stack, window, pos):
        orange = self.get_orange()
        blue = self.get_blue()
        empty = self.get_empty()

        if stack is not None:
            for i in range(5):
                if i >= len(stack):
                    window.blit(empty, (pos , window.get_height()- CELL_SIZE - i * CELL_SIZE))
                elif stack[i] == 'Orange':
                    window.blit(orange, (pos , window.get_height()- CELL_SIZE - i * CELL_SIZE))
                elif stack[i] == 'Blue':
                    window.blit(blue, (pos , window.get_height()- CELL_SIZE - i * CELL_SIZE))
        else:
            print("No stack at this position")
            return None
    """