import pygame

class MainMenuController:
    def __init__(self, main_menu_state):
        self.main_menu_state = main_menu_state

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.main_menu_state.to_select_menu()
                elif event.key == pygame.K_q:
                    self.main_menu_state.to_quit()
                if event.type == pygame.QUIT:
                    self.main_menu_state.to_quit()
        