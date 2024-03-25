from model.MainMenuState import MainMenuState
from model.SelectMenuState import SelectMenuState
from model.GameState import GameState
from model.EndState import EndState
from model.Player import Player

class State:
    def __init__(self):
        self.current_state = MainMenuState(self)

    # Run the current state
    def run(self, window: object) -> None:
        self.current_state.run(window)

    # Change the current state to the Select Menu state
    def to_select_menu(self) -> None:
        if isinstance(self.current_state, MainMenuState): # If the current state is the Main Menu state
            self.current_state = SelectMenuState(self) # Change the current state to the Select Menu state

    # Change the current state to the Game State
    def start_game(self, size: int, Orange: 'Player', Blue: 'Player') -> None:
        if isinstance(self.current_state, SelectMenuState): # If the current state is the Select Menu state
            self.current_state = GameState(self, size, Orange, Blue) # Change the current state to the Game state

    # Change the current state to the End state
    def to_end(self, winner: 'Player') -> None: 
        if isinstance(self.current_state, GameState): # If the current state is the Game state
            self.current_state = EndState(self, winner) # Change the current state to the End state

    # Change the current state to the Select Menu state after the game ends
    def play_again(self) -> None:
        if isinstance(self.current_state, EndState): # If the current state is the End state
            self.current_state = SelectMenuState(self) # Change the current state to the Select Menu state
    
    # Quits the game by setting the current state as None that will be handled in main.py
    def to_quit(self) -> None:
        self.current_state = None

    # Get the current state
    def get_state(self) -> 'State':
        return self.current_state
    