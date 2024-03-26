import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class GameController:
    def __init__(self, game_state):
        self.game_state = game_state

    def clicked_piece(self, cell):
        stack = self.game_state.board.get_stack(cell)
        return (not self.game_state.board.is_none_stack(stack))

    # TODO: Maybe don't use pygame.mouse.get_pos() and replace with cell
    def clicked_saved_player_stack(self, player):
        mouse_pos = pygame.mouse.get_pos()

        if player.get_color() == 'Orange':
            check_rect = pygame.Rect(50, 50, 80, 80)
        elif player.get_color() == 'Blue':
            check_rect = pygame.Rect(630, 50, 80, 80)

        return check_rect.collidepoint(mouse_pos)

    def handle_click(self, cell, player):
        if self.clicked_saved_player_stack(player):
            self.game_state.handle_saved_player_stack_selection(player)
        elif cell == (-1,-1):
            self.game_state.unselect_cell()
        else:    
            if self.clicked_piece(cell):
                if (self.game_state.no_cell_selected()):
                    self.game_state.select_cell(cell)
                else:
                    return self.game_state.make_move(cell)
            else:
                self.game_state.unselect_cell()
        return False       

    def handle_event(self, player):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = self.game_state.get_pos(event.pos)
                return self.handle_click(cell, player)
            if event.type == pygame.QUIT:
                self.game_state.to_quit()
        return False