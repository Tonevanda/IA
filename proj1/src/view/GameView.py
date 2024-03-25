from view.BoardView import BoardView
from view.PlayerView import PlayerView
import pygame
from config import SCREEN_WIDTH

class GameView:
    def __init__(self, game_state, board, starting_cell, orange, blue):
        self.game_state = game_state
        self.board_view = BoardView(board, starting_cell)
        self.orange_view = PlayerView(orange)
        self.blue_view = PlayerView(blue)

    def draw_turn(self, window):
        font = pygame.font.Font(None, 36)
        current_player = self.game_state.get_current_player()
        text_surface = font.render(f"{current_player}'s turn", 1, (10, 10, 10))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
        window.blit(text_surface, text_rect.topleft)

    # TODO: This (and every other draw) should draw with the window.size and not with a fixed size
    def draw(self, window):
        window.fill((255, 255, 255))
        self.board_view.draw(window)
        self.orange_view.draw(window)
        self.blue_view.draw(window)
        self.draw_turn(window)

