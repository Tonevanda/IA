import pygame

class SelectMenuController:
    def __init__(self, select_menu_state):
        self.select_menu_state = select_menu_state

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for i, player_type in enumerate(self.select_menu_state.player_types):
                rect_orange = pygame.Rect(50 + i * 150, 100, 80, 80)
                rect_blue = pygame.Rect(50 + i * 150, 200, 80, 80)

                if rect_orange.collidepoint(mouse_pos):
                    self.select_menu_state.update_selected_orange(player_type)
                elif rect_blue.collidepoint(mouse_pos):
                    self.select_menu_state.update_selected_blue(player_type)
            
            play_button = pygame.Rect(50, 300, 150, 50)
            if play_button.collidepoint(mouse_pos):
                self.select_menu_state.start_game()