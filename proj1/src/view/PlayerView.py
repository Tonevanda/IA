import pygame

class PlayerView:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)  # Choose the font for the text

    def draw(self, window):
        # Draw player name
        name = str(self.player)
        name_surface = self.font.render(name, True, (255, 255, 255))  # Create a surface with the player's name
        window.blit(name_surface, (20, 20))  # Draw the name at position (20, 20)

        # Draw stack count
        stack_count = self.player.get_stack_count()
        stack_count_surface = self.font.render(f'Stack Count: {stack_count}', True, (255, 255, 255))  # Create a surface with the stack count
        window.blit(stack_count_surface, (20, 60))  # Draw the stack count at position (20, 60)