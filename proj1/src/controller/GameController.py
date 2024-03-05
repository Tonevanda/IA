import pygame

class GameController:
    def __init__(self, game_state, x, y):
        self.game_state = game_state
        self.x = x
        self.y = y
        
    # Checks if the click is in the corner of the window
    # TODO: way without window?
    def clicked_corner(self, pixel, window, board):
        x, y = pixel
        return x > window.get_width()-board.cell_size and y > window.get_height()-(board.cell_size*5)

    def handle_click(self, pixel, window):
        (cell_x,cell_y) =  self.game_state.board.get_pos(pixel)

        if self.clicked_corner(pixel, window, self.game_state.board):
            self.game_state.board.current_cell = (0,0)
        elif (cell_x,cell_y) == (-1,-1):
            self.game_state.board.current_possible_moves = None
            self.game_state.board.current_cell = None
        else:    
            if 0 <= cell_x < self.game_state.board.size and 0 <= cell_y < self.game_state.board.size and self.game_state.board.board[cell_y][cell_x] != None:
                if self.game_state.board.current_possible_moves == None and self.game_state.board.current_cell != (0,0):
                    print("here")
                    self.game_state.board.current_possible_moves = self.game_state.board.possible_moves(pixel)
                    self.game_state.board.current_cell = (cell_x,cell_y)
                else:
                    self.game_state.board.make_move((cell_x,cell_y), self.game_state.board)
                    self.game_state.board.current_possible_moves = None
                    self.game_state.board.current_cell = None
            else:
                self.game_state.board.current_possible_moves = None
                self.game_state.board.current_cell = None
        
    def handle_event(self, event, window):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos, window)
