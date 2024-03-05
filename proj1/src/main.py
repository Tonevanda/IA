import pygame
from model.State import State
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def pygame_setup():
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Focus")
    return window

def start(window):
    state = State()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                state.run(event, window)
                if(state.get_state() == None):
                    running = False
        pygame.display.flip()
    pygame.quit()

def main():
    window = pygame_setup()
    start(window)

if __name__ == "__main__":
    main()