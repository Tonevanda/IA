from model.Board import Board
from controller.GameController import GameController
from view.GameView import GameView
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class GameState:
    def __init__(self, state, size, orange, blue):
        self.state = state
        self.board = Board(self, size)
        self.orange = orange    # Player 1
        self.blue = blue        # Player 2
        self.gameController = GameController(self)

        starting_cell = self.get_starting_cell()
        self.gameView = GameView(self, self.board, starting_cell, self.orange, self.blue)

        self.turn = 1

    def get_starting_cell(self):
        board_width = self.board.size * CELL_SIZE
        board_height = self.board.size * CELL_SIZE

        start_x = (SCREEN_WIDTH - board_width) // 2
        start_y = (SCREEN_HEIGHT - board_height) // 2
        return (start_x, start_y)


    def is_outside_board(self, cell_x, cell_y):
        return cell_x >= self.board.get_size() or cell_y >= self.board.get_size() or cell_x < 0 or cell_y < 0

    # Takes a pixel and returns the position of the corresponding cell
    def get_pos(self, pixel):
        x, y = pixel
        (starting_cell_x,starting_cell_y) = self.get_starting_cell()
        cell_y = (x-starting_cell_x) // CELL_SIZE # Represents Columns
        cell_x = (y-starting_cell_y) // CELL_SIZE # Represents Rows
        if self.is_outside_board(cell_x, cell_y): return (-1,-1)
        return (cell_x, cell_y)
    
    def get_current_player(self):
        return self.orange if self.turn % 2 == 1 else self.blue
    
    def get_next_player(self):
        return self.orange if self.turn % 2 == 0 else self.blue

    def next_turn(self):
        self.turn += 1

    def did_win(self):
        if self.verify_win():
            self.state.to_end()
            return True
        return False

    def verify_win(self):
        return (self.get_next_player().get_stack_count() == 0 and self.board.verify_lost(self.get_next_player()))
    
    def add_to_player_stack(self):
        current_player = self.get_current_player()
        current_player.add_stack_piece()

    def remove_from_player_stack(self):
        current_player = self.get_current_player()
        return current_player.remove_stack_piece()
    
    def unselect_cell(self):
        self.board.current_possible_moves = None
        self.board.selected_cell = None

    def no_cell_selected(self):
        return (self.board.current_possible_moves == None and self.board.selected_cell != (0,0))
    
    def can_select_cell(self, cell):
        return (self.board.is_player_stack(cell, self.get_current_player()))

    def select_cell(self, cell):
        if self.can_select_cell(cell):
            self.board.current_possible_moves = self.board.get_possible_moves(cell)
            self.board.selected_cell = cell
        else:
            self.unselect_cell()
    
    def run(self, event, window):
        self.gameController.handle_event(event)
        self.gameView.draw(window)