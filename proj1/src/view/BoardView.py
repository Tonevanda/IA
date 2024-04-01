from config import PIECE_ORANGE, PIECE_BLUE
import pygame

class BoardView:
    def __init__(self, board_model, starting_cell, cell_size, orange, blue):
        self.board = board_model
        self.cell_size = cell_size
        (starting_cell_x, starting_cell_y) = starting_cell
        self.starting_cell_x = starting_cell_x
        self.starting_cell_y = starting_cell_y
        self.orange = orange
        self.blue = blue

    # Draw the hint on the board
    def draw_hint(self, window):
        window_width, window_height = window.get_size()
        starting_cell_x = (window_width - self.board.size * self.cell_size) // 2 # Calculate the starting x position of the board
        starting_cell_y = (window_height - self.board.size * self.cell_size) // 2 # Calculate the starting y position of the board

        if self.orange.hint is not None: # If the orange player has a hint
            hint = self.orange.hint
            if hint.is_from_personal_stack():
                pygame.draw.rect(window, (0, 255, 0), (50, 50, 80, 80))
                destination = hint.get_destination()
                pygame.draw.rect(window, (200, 0, 0), (starting_cell_x + destination[1] * self.cell_size, starting_cell_y + destination[0] * self.cell_size, self.cell_size, self.cell_size))
            else:
                origin = hint.get_origin()
                destination = hint.get_destination()
                pygame.draw.rect(window, (0, 255, 0), (starting_cell_x + origin[1] * self.cell_size, starting_cell_y + origin[0] * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(window, (200, 0, 0), (starting_cell_x + destination[1] * self.cell_size, starting_cell_y + destination[0] * self.cell_size, self.cell_size, self.cell_size))
            
        elif self.blue.hint is not None: # If the blue player has a hint
            hint = self.blue.hint
            if hint.is_from_personal_stack():
                pygame.draw.rect(window, (0, 255, 0), (window_width - 160, 50, 80, 80))
                destination = hint.get_destination()
                pygame.draw.rect(window, (200, 0, 0), (starting_cell_x + destination[1] * self.cell_size, starting_cell_y + destination[0] * self.cell_size, self.cell_size, self.cell_size))
            else:
                origin = hint.get_origin()
                destination = hint.get_destination()
                pygame.draw.rect(window, (0, 255, 0), (starting_cell_x + origin[1] * self.cell_size, starting_cell_y + origin[0] * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(window, (200, 0, 0), (starting_cell_x + destination[1] * self.cell_size, starting_cell_y + destination[0] * self.cell_size, self.cell_size, self.cell_size))

    # Draw the board
    def draw_board(self, window):
        window_width, window_height = window.get_size()
        starting_cell_x = (window_width - self.board.size * self.cell_size) // 2
        starting_cell_y = (window_height - self.board.size * self.cell_size) // 2

        for i in range(self.board.size):
            for j in range(self.board.size):
                stack = self.board.get_stack((i, j))
                if(not self.board.is_none_stack(stack)):
                    pygame.draw.rect(window, (0, 0, 0), (starting_cell_x + j * self.cell_size, starting_cell_y + i * self.cell_size, self.cell_size, self.cell_size), 2)
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
                        pygame.draw.circle(window, (0, 0, 0), (starting_cell_x + j * self.cell_size + self.cell_size // 2, starting_cell_y + i * self.cell_size + self.cell_size // 2 + k * -5), self.cell_size // 2 - 3)
                        pygame.draw.circle(window, color, (starting_cell_x + j * self.cell_size + self.cell_size // 2, starting_cell_y + i * self.cell_size + self.cell_size // 2 + k * -5), self.cell_size // 2 - 5)
 
                        pygame.draw.circle(window, light_color, (starting_cell_x + j * self.cell_size + self.cell_size // 2 - 5, starting_cell_y + i * self.cell_size + self.cell_size // 2 - 5 + k * -5), self.cell_size // 4)
    
    # Draw the possible moves on the board
    def draw_possible_moves(self, window):
        window_width, window_height = window.get_size()
        starting_cell_x = (window_width - self.board.size * self.cell_size) // 2
        starting_cell_y = (window_height - self.board.size * self.cell_size) // 2

        if self.board.current_possible_moves is not None: # Will only draw the current possible moves if there are any
            current_cell = self.board.selected_cell
            pygame.draw.rect(window, (255, 255, 0), (starting_cell_x + current_cell[1] * self.cell_size, starting_cell_y + current_cell[0] * self.cell_size, self.cell_size, self.cell_size))
            for move in self.board.current_possible_moves:
                pygame.draw.rect(window, (0, 200, 0), (starting_cell_x + move[1] * self.cell_size, starting_cell_y + move[0] * self.cell_size, self.cell_size, self.cell_size))
   
    # Draw the board, possible moves, and hints
    def draw(self, window):
        self.draw_possible_moves(window)
        self.draw_hint(window)
        self.draw_board(window)
