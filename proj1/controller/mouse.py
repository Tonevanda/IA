import pygame
from model.state import State
class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def handleClick(self, pixel, board, state):
        (cell_x,cell_y) = board.get_pos(pixel)
        if 0 <= cell_x < board.size and 0 <= cell_y < board.size:
            if state.current_possible_moves == None:
                print("here")
                state.current_possible_moves = board.possible_moves(pixel)
                state.current_cell = (cell_x,cell_y)
            else:
                state.make_move((cell_x,cell_y), board.board)
                state.current_possible_moves = None
                state.current_cell = None
        # Check if the click is within the board
        #if 0 <= cell_x < board.size and 0 <= cell_y < board.size:
        #    state.make_move((cell_x,cell_y), board.board)

        # Check other conditions
        # ...