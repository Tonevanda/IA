import pygame
from model.State import State
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Set up the pygame window
def pygame_setup() -> pygame.Surface:
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) # Create the window with the starting width, height and set it as a resizable window
    pygame.display.set_caption("Focus") # Set the window's title
    return window

# Start the game
def start(window: pygame.Surface) -> None:
    state = State() # Create the state object
    
    running = True
    while running:
        state.run(window)
        if(state.get_state() == None): # If the current state is None
            running = False # Stop the game loop

        pygame.display.flip()
    pygame.quit()

def main() -> None:
    window = pygame_setup() # Set up the pygame window
    start(window) # Start the game

if __name__ == "__main__":
    main()