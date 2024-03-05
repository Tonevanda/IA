import pygame

class PlayerView:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def draw_name(self, window, position, color):
        name = str(self.player)
        name_surface = self.font.render(name, True, color)  # Create a surface with the player's name
        window.blit(name_surface, position)  # Draw the name at position (20, 20)

    def draw_stack(self, window, position, color):
        pygame.draw.rect(window, (0, 0, 0), position, 3)

        stack_count = self.player.get_stack_count()
        stack_count_text = self.font.render(f'{stack_count}x', True, (0, 0, 0))
        text_rect = stack_count_text.get_rect(center=((position[0]+(position[2]//2)), (position[1]+(position[3]//2))))

        # Draw a circle inside the box
        circle_radius = min(position[2], position[3]) // 3  # The radius of the circle is half the smaller dimension of the box
        pygame.draw.circle(window, color, text_rect.center, circle_radius)  # Remove the last argument to fill the circle

        # Draw stack count
        window.blit(stack_count_text, text_rect.topleft)  # Draw the stack count


    def draw(self, window):
        if (self.player.get_color() == "Orange"):
            self.draw_name(window, (20, 20), (255, 100, 0))
            self.draw_stack(window, (50, 50, 80, 80), (255, 100, 0))
        else:
            self.draw_name(window, (590, 20), (50, 50, 255))
            self.draw_stack(window, (630, 50, 80, 80), (50, 50, 255))
        
        

        