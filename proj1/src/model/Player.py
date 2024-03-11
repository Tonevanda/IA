from config import PIECE_BLUE, PIECE_ORANGE

class Player:
    def __init__(self, color, player_type):
        self.color = color
        self.stack_pieces = 0
        self.player_type = player_type
        self.stack_selected = False

    def get_player_type(self):
        return self.player_type
    
    def get_color(self):
        return self.color
    
    def get_color_bits(self):
        return PIECE_ORANGE if self.color == 'Orange' else PIECE_BLUE

    def get_stack_count(self):
        return self.stack_pieces
    
    def add_stack_piece(self):
        self.stack_pieces += 1

    def remove_stack_piece(self):
        self.stack_pieces -= 1

    def select_stack(self):
        self.stack_selected = True
    
    def unselect_stack(self):
        self.stack_selected = False

    def __str__(self):
        return self.color + ' ' + self.player_type