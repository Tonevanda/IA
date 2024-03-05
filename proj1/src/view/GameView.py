from view.BoardView import BoardView
from view.PlayerView import PlayerView

class GameView:
    def __init__(self, board, starting_cell, orange, blue):
        self.board_view = BoardView(board, starting_cell)
        self.orange_view = PlayerView(orange)
        self.blue_view = PlayerView(blue)

    def draw(self, window):
        window.fill((255, 255, 255))
        self.board_view.draw(window)
        self.orange_view.draw(window)

