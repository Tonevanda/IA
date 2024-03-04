class Player:
    def __init__(self, color, player_type):
        self.color = color
        self.stack_pieces = []
        self.player_type = player_type

    def get_player_type(self):
        return self.player_type
    
    def get_color(self):
        return self.color
    
    def get_stack_pieces(self):
        return self.stack_pieces
    
    def add_stack_piece(self, piece):
        self.stack_pieces.append(piece)

    def remove_stack_piece(self):
        return self.stack_pieces.pop(0)

    def __str__(self):
        return self.color + ' ' + self.player_type