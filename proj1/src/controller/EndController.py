import pygame

class EndController:
    def __init__(self, end_state):
        self.end_state = end_state

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.end_state.play_again()
            elif event.key == pygame.K_q:
                self.end_state.to_quit()
            