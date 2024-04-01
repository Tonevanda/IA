from view.EndView import EndView
from controller.EndController import EndController

class EndState:
    def __init__(self, state, winner):
        self.state = state
        self.winner = winner
        self.endView = EndView()
        self.endController = EndController(self)

    def play_again(self):
        self.state.play_again()

    def to_quit(self):
        self.state.to_quit()

    def run(self, window):
        self.endView.draw(window, self.winner) # Calls the draw method from the EndView class with the winner so it can be displayed
        self.endController.handle_event()