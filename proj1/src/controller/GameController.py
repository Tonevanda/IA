import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class GameController:
    def __init__(self, game_state):
        self.game_state = game_state
        
    # Checks if the click is in the corner of the window
    # TODO: There must be a better way to do this
    def clicked_corner(self, cell):
        (cell_x,cell_y) =  cell
        x, y = cell_x*50, cell_y*50
        return x > SCREEN_WIDTH - CELL_SIZE and y > SCREEN_HEIGHT - CELL_SIZE*5


    def handle_click(self, cell):
        (cell_x,cell_y) =  cell

        if self.clicked_corner(cell):
            self.game_state.board.selected_cell = (0,0)
        elif cell == (-1,-1):
            self.game_state.board.current_possible_moves = None
            self.game_state.board.selected_cell = None
        else:    
            if 0 <= cell_x < self.game_state.board.size and 0 <= cell_y < self.game_state.board.size and self.game_state.board.board[cell_y][cell_x] != None:
                if self.game_state.board.current_possible_moves == None and self.game_state.board.selected_cell != (0,0):
                    print("here")
                    self.game_state.board.current_possible_moves = self.game_state.board.possible_moves(cell)
                    self.game_state.board.selected_cell = cell
                else:
                    self.game_state.board.make_move(cell, self.game_state.board)
                    self.game_state.board.current_possible_moves = None
                    self.game_state.board.selected_cell = None
            else:
                self.game_state.board.current_possible_moves = None
                self.game_state.board.selected_cell = None
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(self.game_state.get_pos(event.pos))
