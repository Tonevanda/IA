import pygame
from config import SCREEN_WIDTH

class EndView:
    def __init__(self):
        pass

    def draw_winner(self, window, winner):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{winner} won", 1, (0, 200, 0))
        text_rect = text_surface.get_rect(center=(window.get_width() // 2, 50))
        window.blit(text_surface, text_rect.topleft)

    def draw_play_again(self, window):
        button_color = (0, 255, 0)  # RGB for green
        button_position = ((window.get_width() // 2)-150, window.get_height() - 100) # Position at bottom of screen
        button_size = (300, 50)  # Width and height of button

        # Draw button
        pygame.draw.rect(window, button_color, pygame.Rect(button_position, button_size))

        # Add text to button
        font = pygame.font.Font(None, 36)  # Choose the font for the text
        text = font.render("Press 'r' to play again", True, (0, 0, 0))  # Create the text
        text_rect = text.get_rect(center=(button_position[0] + button_size[0] // 2, button_position[1] + button_size[1] // 2))  # Position the text
        window.blit(text, text_rect)  # Draw the text

    def draw_quit(self, window):
        button_color = (255, 0, 0)
        button_position = ((window.get_width() // 2)-150, window.get_height() - 50)
        button_size = (300, 50)

        pygame.draw.rect(window, button_color, pygame.Rect(button_position, button_size))

        font = pygame.font.Font(None, 36)
        text = font.render("Press 'q' to quit", True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_position[0] + button_size[0] // 2, button_position[1] + button_size[1] // 2))
        window.blit(text, text_rect)


    def draw(self, window, winner):
        self.draw_winner(window, winner)
        self.draw_play_again(window)
        self.draw_quit(window)
