import pygame
from model.State import State

def pygame_setup():
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Focus")
    return window

def start(window):
    # Create state
    state = State()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                quit = state.run(event, window)
                if quit:
                    running = False
        pygame.display.flip()
    pygame.quit()

def main():
    # Pygame setup
    window = pygame_setup()
    start(window)
    
    """
    # Create state
    GameState = GameState()

    # Create board model and board view
    board = Board(boardSize)
    boardView = BoardView(board)
    # Create mouse
    mouse = GameController(0, 0)

    # Draw board
    boardView.draw(window)
    boardView.draw_stack2(window, GameState)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.handle_click(event.pos, board, GameState, window)
                boardView.draw(window)
                boardView.draw_stack(event.pos, window)
                boardView.draw_stack2(window, GameState)
                

        pygame.display.flip()

    pygame.quit()
    """

if __name__ == "__main__":
    main()