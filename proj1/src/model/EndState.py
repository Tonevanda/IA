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

    def run(self, event, window):
        self.endView.draw(window, self.winner)
        self.endController.handle_event(event)