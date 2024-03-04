from view.BoardView import BoardView

class GameView:
    def __init__(self, board):
        self.board_view = BoardView(board)

    def draw(self, window):
        window.fill((255, 255, 255))
        self.board_view.draw(window)
        self.board_view.draw_stack((0,0), window)