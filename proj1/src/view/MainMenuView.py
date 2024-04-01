import pygame

class MainMenuView:
    def __init__(self):
        pass

    # Draws the main menu
    def draw(self, window):
        window.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Welcome to Focus!", 1, (10, 10, 10))
        window.blit(text, (250, 100))
        text = font.render("Press 'p' to play", 1, (10, 10, 10))
        window.blit(text, (250, 200))
        text = font.render("Press 'q' to quit", 1, (10, 10, 10))
        window.blit(text, (250, 300))

        small_font = pygame.font.Font(None, 24)
        developer_text = small_font.render("Developed by: João Lourenço, Tiago Cruz and Tomás Xavier", 1, (10, 10, 10))
        window.blit(developer_text, (250, 400))