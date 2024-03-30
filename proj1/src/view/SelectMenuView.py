from config import BOARD_SIZES
import pygame

class SelectMenuView:
    def __init__(self, select_menu_state):
        self.font = pygame.font.Font(None, 36)
        self.select_menu_state = select_menu_state

    def draw(self, window):
        window.fill((255, 255, 255))
        for i, player_type in enumerate(self.select_menu_state.player_types):
            rect = pygame.Rect(50 + i * 150, 100, 80, 80) 
            pygame.draw.rect(window, (255, 100, 0), rect)  # Orange box
            if i == self.select_menu_state.selected_orange:
                pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Border for selected box

            rect = pygame.Rect(50 + i * 150, 200, 80, 80)
            pygame.draw.rect(window, (50, 50, 255), rect)  # Blue box
            if i == self.select_menu_state.selected_blue:
                pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Border for selected box

            text = self.font.render(player_type, 1, (10, 10, 10))
            window.blit(text, (50 + i * 150, 50))

        text = self.font.render("Select the size of the board:", 1, (10, 10, 10))
        window.blit(text, (50, 300))
        for i, size in enumerate(BOARD_SIZES):
            rect = pygame.Rect(50 + i * 150, 340, 80, 80)
            pygame.draw.rect(window, (100, 100, 100), rect)  # Gray box
            if i == self.select_menu_state.selected_size:  # Highlight the selected size
                pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Border for selected box

            text = self.font.render(str(size), 1, (10, 10, 10))
            window.blit(text, (60 + i * 150, 350))

        play_button = pygame.Rect(50, 450, 150, 50)
        pygame.draw.rect(window, (0, 255, 0), play_button)
        play_text = self.font.render("Start Game", 1, (10, 10, 10))
        window.blit(play_text, (60, 460))
