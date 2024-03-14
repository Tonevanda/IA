from config import PIECE_BLUE, PIECE_ORANGE
import numpy as np

class Player:
    def __init__(self, color, player_type):
        self.color = color
        self.stack_pieces = 0
        self.player_type = player_type
        self.stack_selected = False
        self.cells = np.empty((0, 2), int)

    def get_cells(self):
        return [tuple(cell) for cell in self.cells]

    def add_cell(self, cell):
        self.cells = np.append(self.cells, [cell], axis=0)

    def remove_cell(self, cell):
        self.cells = np.delete(self.cells, np.where(np.all(self.cells == cell, axis=1)), axis=0)

    def get_player_type(self):
        return self.player_type
    
    def get_color(self):
        return self.color
    
    def get_color_bits(self):
        return PIECE_ORANGE if self.color == 'Orange' else PIECE_BLUE

    def get_stack_count(self):
        return self.stack_pieces
    
    def has_saved_pieces(self):
        return self.stack_pieces > 0
    
    def add_stack_piece(self):
        self.stack_pieces += 1

    def remove_stack_piece(self):
        self.stack_pieces -= 1

    def select_stack(self):
        self.stack_selected = True
    
    def unselect_stack(self):
        self.stack_selected = False

    def is_bot(self):
        return self.player_type == 'Easy Bot' or self.player_type == 'Hard Bot' or self.player_type == 'Medium Bot'

    def is_easy_bot(self):
        return self.player_type == 'Easy Bot'

    def is_medium_bot(self):
        return self.player_type == 'Medium Bot'
    
    def is_hard_bot(self):
        return self.player_type == 'Hard Bot'

    def __str__(self):
        return self.color + ' ' + self.player_type