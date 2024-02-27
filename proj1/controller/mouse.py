import pygame
from model.state import State
class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def handleClick(self, pos, board,state):
        x, y = pos
        cell_x = (x - board.start_x) // board.cell_size
        cell_y = (y - board.start_y) // board.cell_size

        # Check if the click is within the board
        if 0 <= cell_x < board.size and 0 <= cell_y < board.size:
            state.make_move((cell_x,cell_y), board.board)


        # Check other conditions
        # ...