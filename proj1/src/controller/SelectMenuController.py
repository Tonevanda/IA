from config import BOARD_SIZES
import pygame

class SelectMenuController:
    def __init__(self, select_menu_state):
        self.select_menu_state = select_menu_state

    # Handles the events that happen during the select menu
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                for i, player_type in enumerate(self.select_menu_state.player_types): # Iterate through the player types
                    rect_orange = pygame.Rect(50 + i * 150, 100, 80, 80)
                    rect_blue = pygame.Rect(50 + i * 150, 200, 80, 80)

                    if rect_orange.collidepoint(mouse_pos):
                        self.select_menu_state.update_selected_orange(player_type)
                    elif rect_blue.collidepoint(mouse_pos):
                        self.select_menu_state.update_selected_blue(player_type)

                for i, _ in enumerate(BOARD_SIZES): # Iterate through the board sizes
                    rect_size = pygame.Rect(50 + i * 150, 340, 80, 80)

                    if rect_size.collidepoint(mouse_pos):
                        self.select_menu_state.update_selected_size(i) # Update the selected size
                
                play_button = pygame.Rect(50, 450, 150, 50)
                if play_button.collidepoint(mouse_pos):
                    self.select_menu_state.start_game()
            if event.type == pygame.QUIT:
                self.select_menu_state.to_quit()