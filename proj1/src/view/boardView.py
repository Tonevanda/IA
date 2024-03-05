import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class BoardView:
    def __init__(self, board_model, starting_cell):
        self.board = board_model
        (starting_cell_x, starting_cell_y) = starting_cell
        self.starting_cell_x = starting_cell_x
        self.starting_cell_y = starting_cell_y

    def get_orange(self):
        orange = pygame.image.load("../resources/orange.jpg")
        orange = pygame.transform.scale(orange, (CELL_SIZE, CELL_SIZE))
        return orange 
    
    def get_blue(self):
        blue = pygame.image.load("../resources/blue.jpg")
        blue = pygame.transform.scale(blue, (CELL_SIZE, CELL_SIZE))
        return blue
    
    def get_empty(self):
        empty = pygame.image.load("../resources/black.jpg")
        empty = pygame.transform.scale(empty, (CELL_SIZE, CELL_SIZE))
        return empty

    def draw_board(self, window):
        orange = self.get_orange()
        blue = self.get_blue()
        empty = self.get_empty()

        for i, row in enumerate(self.board.board):
            for j, cell in enumerate(row):
                # not None -> exists, cell -> not empty, cell[0] -> color of the piece on top of the stack 
                if cell is not None:
                    image = empty
                    if cell and cell[-1] == 'Orange':
                        image = orange
                    elif cell and cell[-1] == 'Blue':
                        image = blue
                    window.blit(image, (self.starting_cell_x + j * CELL_SIZE, self.starting_cell_y + i * CELL_SIZE))

    def draw(self, window):
        self.draw_board(window)
        self.draw_stack(window)


    #draws the selected stack
    def draw_stack(self,window):
        selected_stack = self.board.get_selected_stack()
        if selected_stack is not None:
            self.generic_draw(selected_stack, window, 0)

        
    #same as before but bottom right corner
    def draw_stack2(self,window,state):
        if(state.current_player == "Orange"):
            stack = self.board.orange_stack
        else:
            stack = self.board.blue_stack
        self.generic_draw(stack, window, window.get_width()-CELL_SIZE)
    
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