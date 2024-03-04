from model.Board import Board
from controller.GameController import GameController
from view.GameView import GameView


class GameState:
    def __init__(self, size, orange, blue):
        self.board = Board(size)
        self.orange = orange
        self.blue = blue
        self.gameController = GameController(0, 0)
        self.gameView = GameView(self.board)
        """
        self.player1 = 'Orange'
        self.player2 = 'Blue'
        self.current_player = self.player1
        self.current_possible_moves = None
        self.current_cell = None
        """

    def run(self, event, window):
        self.gameController.handle_event(event)
        self.gameView.draw(window)