import pygame
from model.state import State
class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def handleClick(self, pixel, board, state, window):
        (cell_x,cell_y) = board.get_pos(pixel)
        if self.check_corner(pixel, window, board):
            state.current_cell = (0,0)
        elif (cell_x,cell_y) == (-1,-1):
            state.current_possible_moves = None
            state.current_cell = None
        else:    
            print(cell_x,cell_y)
            if 0 <= cell_x < board.size and 0 <= cell_y < board.size:
                if state.current_possible_moves == None and state.current_cell != (0,0):
                    print("here")
                    state.current_possible_moves = board.possible_moves(pixel)
                    state.current_cell = (cell_x,cell_y)
                else:
                    state.make_move((cell_x,cell_y), board)
                    state.current_possible_moves = None
                    state.current_cell = None
        
    def check_corner(self, pixel, window, board):
        x, y = pixel
        if x > window.get_width()-board.cell_size and y > window.get_height()-(board.cell_size*5):
            return True
        return False