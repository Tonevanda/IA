from model.Board import Board
from controller.GameController import GameController
from view.GameView import GameView
from constants import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT


class GameState:
    def __init__(self, size, orange, blue):
        self.board = Board(size)
        self.orange = orange    # Player 1
        self.blue = blue        # Player 2
        self.gameController = GameController(self)

        starting_cell = self.get_starting_cell()
        self.gameView = GameView(self.board, starting_cell, self.orange, self.blue)

        self.turn = 1
        """
        self.player1 = 'Orange'
        self.player2 = 'Blue'
        self.current_player = self.player1
        self.current_possible_moves = None
        self.selected_cell = None
        """

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
        cell_x = (x-starting_cell_x) // CELL_SIZE
        cell_y = (y-starting_cell_y) // CELL_SIZE
        if self.is_outside_board(cell_x, cell_y): return (-1,-1)
        return (cell_x, cell_y)
    
    def get_current_player(self):
        return self.orange if self.turn % 2 == 1 else self.blue

    def next_turn(self):
        self.turn += 1

    def run(self, event, window):
        self.gameController.handle_event(event)
        self.gameView.draw(window)