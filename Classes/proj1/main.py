import pygame
from view.board import Board

def main():

    # Prompt user for board size
    boardSize = int(input("Enter the size of the board (m x m): "))

    # Pygame setup
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Focus")

    # Create and draw board
    board = Board(boardSize)
    board.draw(window)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()