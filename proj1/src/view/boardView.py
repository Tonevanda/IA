import pygame

class BoardView:
    def __init__(self, board_model):
        self.board = board_model

    def draw(self, window):
        board_width = self.board.size * self.board.cell_size
        board_height = self.board.size * self.board.cell_size

        self.board.start_x = (window.get_width() - board_width) // 2
        self.board.start_y = (window.get_height() - board_height) // 2

        orange = pygame.image.load("../resources/orange.jpg")  
        blue = pygame.image.load("../resources/blue.jpg")
        empty = pygame.image.load("../resources/black.jpg")

        orange = pygame.transform.scale(orange, (self.board.cell_size, self.board.cell_size))
        blue = pygame.transform.scale(blue, (self.board.cell_size, self.board.cell_size))
        empty = pygame.transform.scale(empty, (self.board.cell_size, self.board.cell_size))

        for i, row in enumerate(self.board.board):
            for j, cell in enumerate(row):
                # not None -> exists, cell -> not empty, cell[0] -> color of the piece on top of the stack 
                if cell is not None:
                    image = empty
                    if cell and cell[-1] == 'Orange':
                        image = orange
                    elif cell and cell[-1] == 'Blue':
                        image = blue
                    window.blit(image, (self.board.start_x + j * self.board.cell_size, self.board.start_y + i * self.board.cell_size))
    

    #draws the stack at the given position in the bottom left corner of the screen
    def draw_stack(self,pixel,window):
        pos = self.board.get_pos(pixel)
        stack = self.board.get_stack(pos)
        self.generic_draw(stack, window, 0)

    #same as before but bottom right corner
    def draw_stack2(self,window,state):
        if(state.current_player == "Orange"):
            stack = self.board.orange_stack
        else:
            stack = self.board.blue_stack
        self.generic_draw(stack, window, window.get_width()-self.board.cell_size)
    
    def generic_draw(self, stack, window, pos):
        orange = pygame.image.load("../resources/orange.jpg")  
        orange = pygame.transform.scale(orange, (self.board.cell_size, self.board.cell_size))
        blue = pygame.image.load("../resources/blue.jpg")
        blue = pygame.transform.scale(blue, (self.board.cell_size, self.board.cell_size))
        black = pygame.image.load("../resources/black.jpg")
        black = pygame.transform.scale(black, (self.board.cell_size, self.board.cell_size))

        if stack is not None:
            for i in range(5):
                if i >= len(stack):
                    window.blit(black, (pos , window.get_height()- self.board.cell_size - i * self.board.cell_size))
                elif stack[i] == 'Orange':
                    window.blit(orange, (pos , window.get_height()- self.board.cell_size - i * self.board.cell_size))
                elif stack[i] == 'Blue':
                    window.blit(blue, (pos , window.get_height()- self.board.cell_size - i * self.board.cell_size))
        else:
            print("No stack at this position")
            return None