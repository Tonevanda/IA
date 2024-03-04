from view.MainMenuView import MainMenuView
from controller.MainMenuController import MainMenuController

class MainMenuState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.controller = MainMenuController(self)
        self.view = MainMenuView()

    def to_select_menu(self):
        self.state_manager.to_select_menu()
    
    def to_quit(self):
        self.state_manager.to_quit()

    def run(self, event, window):
        self.controller.handle_event(event)
        self.view.draw(window)