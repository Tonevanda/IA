PIECE_NONE =                0b11
PIECE_EMPTY =               0b00
PIECE_ORANGE =              0b01
PIECE_BLUE =                0b10
BOARD_SIZES =               [4,6,8,10,12]
CELL_SIZE =                 {4:70, 6: 70, 8: 50, 10: 50, 12: 42}
STACK_MAX_SIZES =           {4: 2, 6: 3, 8: 5, 10: 5, 12: 5}
STACK_MASKS =               {4: 0b1111, 6: 0b111111, 8: 0b1111111111, 10: 0b1111111111, 12: 0b1111111111}
MEDIUM_BOT_DEPTH =          2
HARD_BOT_DEPTH =            4
PLAYER_HINT_DEPTH =         3
MCTS_ITERATIONS =           100

class Config:
    def __init__(self) -> None:
        self.board_size = 8
        self.screen_width = 800
        self.screen_height = 600

    def update_board_size(self, size: int) -> None:
        self.board_size = size

    def get_screen_size(self):
        return self.screen_width, self.screen_height
    
    def get_cell_size(self):
        return CELL_SIZE[self.board_size]

    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height