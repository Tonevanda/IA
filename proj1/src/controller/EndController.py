import pygame

class EndController:
    def __init__(self, end_state):
        self.end_state = end_state

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.end_state.play_again()
                elif event.key == pygame.K_q or event.type == pygame.QUIT:
                    self.end_state.to_quit()
            