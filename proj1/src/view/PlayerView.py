import pygame

class PlayerView:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 36)

    # Draw the player's name
    def draw_name(self, window, position, color):
        name = str(self.player)
        name_surface = self.font.render(name, True, color)  # Create a surface with the player's name
        window.blit(name_surface, position)

    # Draw the player's stack
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

    # Draw the selected stack
    def draw_selected_stack(self, window, position):
        if self.player.stack_selected:
            pygame.draw.rect(window, (255, 255, 0), position)

    # Draw the lightbulb button
    def draw_lightbulb_button(self, window, position, color):
        # Draw the button
        pygame.draw.rect(window, color, position)

        # Draw the lightbulb
        lightbulb_radius = min(position[2], position[3]) // 3  # Increase the radius
        lightbulb_center = (position[0] + position[2] // 2, position[1] + position[3] // 2 - lightbulb_radius // 2)
        pygame.draw.circle(window, (255, 255, 0), lightbulb_center, lightbulb_radius)

        # Draw a smaller yellow circle below the lightbulb
        smaller_lightbulb_center = (lightbulb_center[0], lightbulb_center[1] + lightbulb_radius - lightbulb_radius // 5)
        smaller_lightbulb_radius = lightbulb_radius // 2
        pygame.draw.circle(window, (255, 255, 0), smaller_lightbulb_center, smaller_lightbulb_radius)

        # Draw the base of the lightbulb
        base_height = lightbulb_radius // 2
        base_rect = (lightbulb_center[0] - lightbulb_radius // 3, position[1] + position[3] - base_height, 2 * lightbulb_radius // 3, base_height)
        pygame.draw.rect(window, (128, 128, 128), base_rect)

        # Draw the filament
        filament_color = (255, 69, 0)
        pygame.draw.line(window, filament_color, (base_rect[0], base_rect[1] - base_height // 2), (base_rect[0] + base_rect[2], base_rect[1] - base_height // 2), 3)

    def draw(self, window):
        window_width, window_height = window.get_size()
        stack_position = (50, 50, 80, 80)

        if (self.player.get_color() == "Orange"):
            self.draw_name(window, (20, 20), (255, 100, 0))
            self.draw_selected_stack(window, (50, 50, 80, 80))
            self.draw_stack(window, stack_position, (255, 100, 0))
            if(not self.player.is_bot()):
                lightbulb_button_position = (stack_position[0] + stack_position[2] + 10, stack_position[1] + 20, 60, 60)
                self.draw_lightbulb_button(window, lightbulb_button_position, (200, 200, 200))
        else:
            name_position = (window_width - 220, 20)
            self.draw_name(window, name_position, (50, 50, 255))
            stack_position = (window_width - 160, 50, 80, 80)
            self.draw_selected_stack(window, stack_position)
            self.draw_stack(window, stack_position, (50, 50, 255))
            if(not self.player.is_bot()):
                lightbulb_button_position = (stack_position[0] - 70, stack_position[1] + 20, 60, 60) 
                self.draw_lightbulb_button(window, lightbulb_button_position, (200, 200, 200))
