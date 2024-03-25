import pygame
from config import CELL_SIZE, PIECE_ORANGE, PIECE_BLUE

class BoardView:
    def __init__(self, board_model, starting_cell):
        self.board = board_model
        (starting_cell_x, starting_cell_y) = starting_cell
        self.starting_cell_x = starting_cell_x
        self.starting_cell_y = starting_cell_y

    def draw_board(self, window):
        for i in range(self.board.size):
            for j in range(self.board.size):
                stack = self.board.get_stack((i, j))
                if(not self.board.is_none_stack(stack)):
                    pygame.draw.rect(window, (0, 0, 0), (self.starting_cell_x + j * CELL_SIZE, self.starting_cell_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
                    for k in range(self.board.get_stack_size(stack)):
                        piece = (stack & (0b11 << (k * 2))) >> (k * 2)
                        if piece == PIECE_ORANGE:
                            color = (255, 100, 0)
                            light_color = (255, 150, 50)
                        elif piece == PIECE_BLUE:
                            color = (50, 50, 255)
                            light_color = (100, 100, 255)
                        else:
                            continue
                        pygame.draw.circle(window, (0, 0, 0), (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 + k * -5), CELL_SIZE // 2 - 3)
                        pygame.draw.circle(window, color, (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 + k * -5), CELL_SIZE // 2 - 5)
                        pygame.draw.circle(window, light_color, (self.starting_cell_x + j * CELL_SIZE + CELL_SIZE // 2 - 5, self.starting_cell_y + i * CELL_SIZE + CELL_SIZE // 2 - 5 + k * -5), CELL_SIZE // 4)

    def draw_possible_moves(self, window):
        if self.board.current_possible_moves is not None:
            current_cell = self.board.selected_cell
            pygame.draw.rect(window, (255, 255, 0), (self.starting_cell_x + current_cell[1] * CELL_SIZE, self.starting_cell_y + current_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for move in self.board.current_possible_moves:
                pygame.draw.rect(window, (0, 200, 0), (self.starting_cell_x + move[1] * CELL_SIZE, self.starting_cell_y + move[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def draw(self, window):
        self.draw_possible_moves(window)
        self.draw_board(window)
