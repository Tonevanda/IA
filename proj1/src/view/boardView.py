import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, PIECE_ORANGE, PIECE_BLUE

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
                    for k in range(5):
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

        """

        for i, row in enumerate(self.board.size):
            
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
        """
    def draw(self, window):
        self.draw_possible_moves(window)
        self.draw_board(window)
        
    
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