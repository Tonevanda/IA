import pygame

class GameController:
    def __init__(self, game_state):
        self.game_state = game_state

    # Checks if the given cell clicked is a valid cell
    def clicked_piece(self, cell):
        return self.game_state.board.is_valid_cell(cell)

    # Checks if the given player stack is clicked
    def clicked_saved_player_stack(self, player):
        mouse_pos = pygame.mouse.get_pos()
        window_width, _ = pygame.display.get_surface().get_size()

        if player.get_color() == 'Orange':
            check_rect = pygame.Rect(50, 50, 80, 80)
        elif player.get_color() == 'Blue':
            check_rect = pygame.Rect(window_width - 160, 50, 80, 80)

        return check_rect.collidepoint(mouse_pos)
    
    # Checks if the player hint is clicked
    def clicked_player_hint(self, player):
        mouse_pos = pygame.mouse.get_pos()
        window_width, _ = pygame.display.get_surface().get_size()

        if player.get_color() == 'Orange':
            hint = pygame.Rect(50 + 80 + 20, 50 + 20, 60, 60)
        elif player.get_color() == 'Blue':
            hint = pygame.Rect(window_width - 160 - 80, 50 + 20, 60, 60)

        return hint.collidepoint(mouse_pos)

    # Handles the click event. Returns true if a move is made
    def handle_click(self, cell, player):
        if self.clicked_saved_player_stack(player): # If the player stack was clicked
            self.game_state.unselect_cell() # Unselect the cell
            self.game_state.handle_saved_player_stack_selection(player) # Calls the handler for the player stack
        elif self.clicked_player_hint(player): # If the hint button was clicked
            self.game_state.unselect_cell() # Unselect the cell
            self.game_state.handle_hint(player) # Calls the handler for the hint
        else:    
            if self.clicked_piece(cell): # If the cell clicked is a a piece
                if (self.game_state.no_cell_selected()): # If no cell is selected
                    self.game_state.select_cell(cell) # Select the cell
                else:
                    return self.game_state.make_move(cell) # If a cell is already selected, make the move and return True if a move was made
            else:
                self.game_state.unselect_cell() # Unselect the cell if no piece was clicked
        return False

    # Handles the events that happen during the game
    def handle_event(self, player):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = self.game_state.get_pos(event.pos)
                return self.handle_click(cell, player)
            if event.type == pygame.QUIT:
                self.game_state.to_quit()
        return False