import pygame
from model.state import State
class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def handleClick(self, pixel, board, state):
        (cell_x,cell_y) = board.get_pos(pixel)

        # Check if the click is within the board
        if 0 <= cell_x < board.size and 0 <= cell_y < board.size:
            state.make_move((cell_x,cell_y), board.board)

        # Check other conditions
        # ...