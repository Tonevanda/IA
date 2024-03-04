from model.MainMenuState import MainMenuState
from model.SelectMenuState import SelectMenuState
from model.GameState import GameState
from model.EndState import EndState

class State:
    def __init__(self):
        self.current_state = MainMenuState(self)

    def run(self, event, window):
        if(self.current_state == None):
            return True
        self.current_state.run(event, window)
        return False

    def to_select_menu(self):
        if isinstance(self.current_state, MainMenuState):
            self.current_state = SelectMenuState(self)

    def start_game(self, size, Orange, Blue):
        if isinstance(self.current_state, SelectMenuState):
            self.current_state = GameState(size, Orange, Blue)

    def to_end(self):
        if isinstance(self.current_state, GameState):
            self.current_state = EndState(self)

    def to_main_menu(self):
        if isinstance(self.current_state, EndState):
            self.current_state = MainMenuState(self)
    
    def to_quit(self):
        self.current_state = None

    def get_state(self):
        return self.current_state
    