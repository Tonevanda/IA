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

    def copy(self):
        new_state = GameState.__new__(GameState)
        new_state.state = self.state
        new_state.turn = self.turn
        new_state.board = self.board.copy()
        new_state.orange = copy.deepcopy(self.orange)
        new_state.blue = copy.deepcopy(self.blue)
        return new_state

    def get_starting_cell(self):
        board_width = self.board.size * CELL_SIZE
        board_height = self.board.size * CELL_SIZE

        start_x = (SCREEN_WIDTH - board_width) // 2
        start_y = (SCREEN_HEIGHT - board_height) // 2
        return (start_x, start_y)


    def is_outside_board(self, cell_x, cell_y):
        return cell_x >= self.board.get_size() or cell_y >= self.board.get_size() or cell_x < 0 or cell_y < 0

    # Takes a pixel and returns the position of the corresponding cell
    def get_pos(self, pixel: tuple) -> tuple:
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
        print(str(self.get_next_player()), " cells:")
        print(self.get_next_player().get_cells())
        return (self.get_next_player().get_stack_count() == 0 and len(self.get_next_player().get_cells()) == 0)
    
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
        self.unselect_cell()

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
            selectable_cells = bot.get_cells()
            selectable_cells_board = self.board.get_selectable_cells(bot)
            selectable_cells_bitboard = self.board.get_bitboard_selectable_cells(bot)

            print ("Selectable Cells Bitboard: " + str(selectable_cells_bitboard))

            random_select = tuple(random.choice(selectable_cells))
            random_board = random.choice(selectable_cells_board)
            random_bitboard = random.choice(selectable_cells_bitboard)

            #self.select_cell(random_select)
            #self.select_cell(random_board)
            self.select_cell(random_bitboard)
            movable_cells = self.board.current_possible_moves
            random_move = random.choice(movable_cells)
            self.move_stack(random_move)
            print("Moved from: " + str(random_select) + " to " + str(random_move))

    def handle_medium_bot(self, bot):

        best_value = float('-inf')
        best_move = None
        player = self.get_current_player() 
        opponent = self.get_next_player()
        for move in self.board.get_valid_moves(bot):
            new_state = self.copy()
            initial_position = move.get_origin()
            destination = move.get_destination()

            if(move.is_from_personal_stack()):
                new_state.handle_saved_player_stack_selection(new_state.get_current_player())
                new_state.place_saved_piece(destination, new_state.get_current_player())
            else:
                new_state.select_cell(initial_position)
                new_state.make_move(destination)

            #print("Move: " + str(move))
            move_value = self.minimax(new_state, 0, float('-inf'), float('inf'), False, player, opponent)
            # Call to Negamax
            # move_value = self.negamax(new_state, 0, float('-inf'), float('inf'), 1)

            if move_value > best_value:
                best_value = move_value
                best_move = move

        self.select_cell(best_move.get_origin())
        print("Selected Origin: " + str(best_move.get_origin()))
        self.make_move(best_move.get_destination())
        print("Selected Destination: " + str(best_move.get_destination()))

    def handle_hard_bot(self, bot):
        pass
            
    def handle_bot(self, bot):
        if(bot.is_easy_bot()):
            sleep(0.2)
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

    def eval(self, player, opponent) -> int:
        # Pieces in the personal stack are more valuable than pieces on the board
        return (player.get_stack_count() - opponent.get_stack_count()) * 10 + len(player.get_cells()) - len(opponent.get_cells())
    
    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player, opponent):
        if depth == 0 or state.verify_win():
            return state.eval(player, opponent)
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in state.board.get_valid_moves(state.get_current_player()):

                new_state = state.copy()
                initial_position = move.get_origin()
                destination = move.get_destination()

                if(move.is_from_personal_stack()):
                    new_state.handle_saved_player_stack_selection(new_state.get_current_player())
                    new_state.place_saved_piece(destination, new_state.get_current_player())
                else:
                    new_state.select_cell(initial_position)
                    new_state.make_move(destination)

                eval = new_state.minimax(new_state, depth-1, alpha, beta, False, player, opponent)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for move in state.board.get_valid_moves(state.get_current_player()):

                new_state = state.copy()
                initial_position = move.get_origin()
                destination = move.get_destination()

                if(move.is_from_personal_stack()):
                    new_state.handle_saved_player_stack_selection(new_state.get_current_player())
                    new_state.place_saved_piece(destination, new_state.get_current_player())
                else:
                    new_state.select_cell(initial_position)
                    new_state.make_move(destination)

                eval = new_state.minimax(new_state, depth-1, alpha, beta, True, player, opponent)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        
    def negamax(self, state, depth, alpha, beta, color):
        if depth == 0 or state.verify_win():
            return color * state.eval(state.get_current_player(), state.get_next_player())
        
        maxEval = float('-inf')
        for move in state.board.get_valid_moves(state.get_current_player()):
            new_state = state.copy()
            initial_position = move.get_origin()
            destination = move.get_destination()

            if(move.is_from_personal_stack()):
                new_state.handle_saved_player_stack_selection(new_state.get_current_player())
                new_state.place_saved_piece(destination, new_state.get_current_player())
            else:
                new_state.select_cell(initial_position)
                new_state.make_move(destination)

            eval = -new_state.negamax(new_state, depth-1, -beta, -alpha, -color)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        return maxEval