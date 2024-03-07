import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

class GameController:
    def __init__(self, game_state):
        self.game_state = game_state
        
    # Checks if the click is in the corner of the window
    # TODO: There must be a better way to do this // Not being used rn I think
    def clicked_corner(self, cell):
        (cell_x,cell_y) =  cell
        x, y = cell_x*50, cell_y*50 # Missing + starting cell
        return x > SCREEN_WIDTH - CELL_SIZE and y > SCREEN_HEIGHT - CELL_SIZE*5

    def clicked_piece(self, cell):
        (cell_x,cell_y) =  cell
        print("Cell: " + str(cell))
        stack = self.game_state.board.get_stack(cell)
        return (not self.game_state.board.is_none_stack(stack))
        # return 0 <= cell_x < self.game_state.board.size and 0 <= cell_y < self.game_state.board.size and self.game_state.board.board[cell_y][cell_x] != None

    # TODO: Maybe don't use pygame.mouse.get_pos() and replace with cell
    def clicked_saved_player_stack(self):
        player = self.game_state.get_current_player()
        mouse_pos = pygame.mouse.get_pos()

        if player.get_color() == 'Orange':
            check_rect = pygame.Rect(50, 50, 80, 80)
        elif player.get_color() == 'Blue':
            check_rect = pygame.Rect(630, 50, 80, 80)

        return check_rect.collidepoint(mouse_pos)

    def handle_click(self, cell):

        #if self.clicked_corner(cell):
        #    self.game_state.board.selected_cell = (0,0)
        #    print("Corner clicked")
        if self.clicked_saved_player_stack():
            print("Stack clicked")
        elif cell == (-1,-1):
            self.game_state.board.current_possible_moves = None
            self.game_state.board.selected_cell = None
        else:    
            if self.clicked_piece(cell):
                if self.game_state.board.current_possible_moves == None and self.game_state.board.selected_cell != (0,0):
                    self.game_state.board.current_possible_moves = self.game_state.board.get_possible_moves(cell)
                    print("Clicked Piece: " + str(cell) + " Possible moves: " + str(self.game_state.board.current_possible_moves))
                    self.game_state.board.selected_cell = cell
                else:
                    self.game_state.board.make_move(cell, self.game_state.board)
                    self.game_state.board.current_possible_moves = None
                    self.game_state.board.selected_cell = None
                
            else:
                self.game_state.board.current_possible_moves = None
                self.game_state.board.selected_cell = None
                

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(self.game_state.get_pos(event.pos))


