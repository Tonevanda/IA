from model.Player import Player
from controller.SelectMenuController import SelectMenuController
from view.SelectMenuView import SelectMenuView

class SelectMenuState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.player_types = ["Player", "Easy Bot", "Medium Bot", "Hard Bot"]
        self.selected_orange = 0    # Index of the currently selected player 1 (orange)
        self.selected_blue = 0      # Index of the currently selected player 2 (blue)
        self.size = 8
        self.controller = SelectMenuController(self)
        self.view = SelectMenuView(self)

    def start_game(self):
        self.state_manager.start_game(self.size, Player('Orange', self.player_types[self.selected_orange]), Player('Blue', self.player_types[self.selected_blue]))

    def update_selected_orange(self, player):
        match player:
            case "Player":
                self.selected_orange = 0
            case "Easy Bot":
                self.selected_orange = 1
            case "Medium Bot":
                self.selected_orange = 2
            case "Hard Bot":
                self.selected_orange = 3
    
    def update_selected_blue(self, player):
        match player:
            case "Player":
                self.selected_blue = 0
            case "Easy Bot":
                self.selected_blue = 1
            case "Medium Bot":
                self.selected_blue = 2
            case "Hard Bot":
                self.selected_blue = 3

    def to_quit(self):
        self.state_manager.to_quit()

    def run(self, window):
        self.controller.handle_event()
        self.view.draw(window)