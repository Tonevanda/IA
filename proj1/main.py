import pygame
from view.boardView import BoardView
from model.board import Board
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

    # Create board model and board view
    board = Board(boardSize)
    boardView = BoardView(board)
    # Create mouse
    mouse = Mouse(0, 0)

    # Draw board
    window.fill((255, 255, 255))
    boardView.draw(window)
    boardView.draw_stack2(window, state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.handle_click(event.pos, board, state, window)
                boardView.draw(window)
                boardView.draw_stack(event.pos, window)
                boardView.draw_stack2(window, state)
                

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()