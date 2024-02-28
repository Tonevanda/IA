import pygame
from view.board import Board
from controller.mouse import Mouse
from model.state import State

def main():

    # Prompt user for board size
    boardSize = int(input("Enter the size of the board (m x m): "))

    # Pygame setup
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Focus")

    # Create state
    state = State()


    # Create and draw board
    board = Board(boardSize)
    board.draw(window)

    # Create mouse
    mouse = Mouse(0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.handleClick(event.pos, board, state)
                board.draw(window)
                board.draw_stack(event.pos, window)
                print(board.possible_moves(event.pos))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()