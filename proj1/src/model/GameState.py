from model.Board import Board
from controller.GameController import GameController
from view.GameView import GameView
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, PIECE_ORANGE
import random
import copy
from time import sleep

class GameState:
    def __init__(self, state, size, orange, blue):
        self.state = state
        self.orange = orange    # Player 1
        self.blue = blue        # Player 2
        self.board = Board(self, size)
        self.gameController = GameController(self)

        starting_cell = self.get_starting_cell()
        self.gameView = GameView(self, self.board, starting_cell, self.orange, self.blue)

        self.turn = 1

    def get_starting_cell(self):
        board_width = self.board.size * CELL_SIZE
        board_height = self.board.size * CELL_SIZE

        start_x = (SCREEN_WIDTH - board_width) // 2
        start_y = (SCREEN_HEIGHT - board_height) // 2
        return (start_x, start_y)


    def is_outside_board(self, cell_x, cell_y):
        return cell_x >= self.board.get_size() or cell_y >= self.board.get_size() or cell_x < 0 or cell_y < 0

    # Takes a pixel and returns the position of the corresponding cell
    def get_pos(self, pixel):
        x, y = pixel
        (starting_cell_x,starting_cell_y) = self.get_starting_cell()
        cell_y = (x-starting_cell_x) // CELL_SIZE # Represents Columns
        cell_x = (y-starting_cell_y) // CELL_SIZE # Represents Rows
        if self.is_outside_board(cell_x, cell_y): return (-1,-1)
        return (cell_x, cell_y)
    
    def get_current_player(self):
        return self.orange if self.turn % 2 == 1 else self.blue
    
    def get_next_player(self):
        return self.orange if self.turn % 2 == 0 else self.blue

    def next_turn(self):
        self.turn += 1

    def did_win(self):
        if self.verify_win():
            winner = self.get_current_player()
            self.state.to_end(winner)
            return True
        return False

    def verify_win(self):
        return (self.get_next_player().get_stack_count() == 0 and self.board.verify_lost(self.get_next_player()))
    
    def add_to_player_stack(self):
        current_player = self.get_current_player()
        current_player.add_stack_piece()

    def remove_from_player_stack(self):
        current_player = self.get_current_player()
        return current_player.remove_stack_piece()
    
    def add_to_player_cells_color(self, cell, color):
        if color == PIECE_ORANGE:
            self.orange.add_cell(cell)
        else:
            self.blue.add_cell(cell)
    
    def add_to_player_cells(self, cell, player):
        player.add_cell(cell)

    def remove_from_player_cells(self, cell, player):
        player.remove_cell(cell)
    
    def unselect_cell(self):
        self.board.current_possible_moves = None
        self.board.selected_cell = None
        self.unselect_saved_player_stack(self.get_current_player())

    def no_cell_selected(self):
        return (self.board.current_possible_moves == None and self.get_current_player().stack_selected == False)
    
    def can_select_cell(self, cell):
        return (self.board.is_player_stack(cell, self.get_current_player()))

    def select_cell(self, cell):
        if self.can_select_cell(cell):
            self.board.current_possible_moves = self.board.get_possible_moves(cell)
            self.board.selected_cell = cell
        else:
            self.unselect_cell()

    def handle_saved_player_stack_selection(self, player):
        if player.stack_selected:
            self.unselect_saved_player_stack(player)
        else:
            self.select_saved_player_stack(player)

    def select_saved_player_stack(self, player):
        if(not player.has_saved_pieces()):
            return
        player.select_stack()
    
    def unselect_saved_player_stack(self, player):
        player.unselect_stack()

    def place_saved_piece(self, cell, player):
        if player.stack_selected:
            self.board.place_saved_piece(cell, player)
            self.remove_from_player_stack()
            self.unselect_saved_player_stack(player)
            if(not self.did_win()):
                self.next_turn()

    def move_stack(self, cell):
        if cell in self.board.current_possible_moves:
            self.board.make_move(cell, self.get_current_player())
            if(not self.did_win()):
                self.next_turn()
                print("Cells: " + str(self.get_current_player().get_cells()))
        self.unselect_cell()
    
    # Function used specifically for the AI to calculate the tree
    def make_move(self, cell, board):
        return None

    def make_move(self, cell):
        player = self.get_current_player()
        if(player.stack_selected):
            self.place_saved_piece(cell, player)
        else:
            self.move_stack(cell)

    def is_bot_playing(self):
        return self.get_current_player().is_bot()
    
    def handle_easy_bot(self, bot):
        if bot.has_saved_pieces():
            self.handle_saved_player_stack_selection(bot)
            self.place_saved_piece(self.board.get_random_cell(), bot)
        else:
            selectable_cells = self.board.get_selectable_cells(bot)
            random_select = random.choice(selectable_cells)
            self.select_cell(random_select)
            movable_cells = self.board.current_possible_moves
            random_move = random.choice(movable_cells)
            self.move_stack(random_move)

    def handle_medium_bot(self, bot):
        print("VALID MOVES")
        print(self.board.get_valid_moves(bot))
        #board = copy.deepcopy(self.board)

    def handle_hard_bot(self, bot):
        pass
            
    def handle_bot(self, bot):
        sleep(0.2)
        if(bot.is_easy_bot()):
            self.handle_easy_bot(bot)
        elif(bot.is_medium_bot()):
            self.handle_medium_bot(bot)
        elif(bot.is_hard_bot()):
            self.handle_hard_bot(bot)

    def handle_player(self):
        player = self.get_current_player()
        if player.is_bot():
            self.handle_bot(player)
        else:
            self.gameController.handle_event(player)

    def run(self, window):
        self.handle_player()
        self.gameView.draw(window)

    def to_quit(self):
        self.state.to_quit()
