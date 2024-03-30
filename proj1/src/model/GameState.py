from model.Board import Board
from controller.GameController import GameController
from view.GameView import GameView
from config import PIECE_ORANGE, MEDIUM_BOT_DEPTH, HARD_BOT_DEPTH, PLAYER_INT_DEPTH
import random
import copy
from typing import Dict, Tuple
from model.Move import Move
from collections import defaultdict
import hashlib

class GameState:
    # Hashmap that stores, for each pair of board, and pair of player stacks, and depth, the value of the state
    # ((board hash, player1_stack, player2_stack), eval_func, depth) -> value
    # TODO: Could be a hash of the whole state (hash256 has 2^256 so probability of collisions is low and it is better and more efficient)
    memo: Dict[Tuple[Tuple[str, int, int], str, int], int] = defaultdict(int)

    def __init__(self, state, size, orange, blue):
        self.state = state
        self.orange = orange    # Player 1
        self.blue = blue        # Player 2
        self.board = Board(self, size)
        self.gameController = GameController(self)
        
        self.last_move = None

        starting_cell = self.get_starting_cell()
        self.gameView = GameView(self, self.board, starting_cell, self.orange, self.blue, self.state.get_cell_size())

        self.turn = 1

    def copy(self):
        new_state = GameState.__new__(GameState)
        new_state.state = self.state 
        new_state.turn = self.turn
        new_state.orange = copy.deepcopy(self.orange)
        new_state.blue = copy.deepcopy(self.blue)
        new_state.board = self.board.copy(new_state)
        return new_state

    def get_last_move(self):
        return self.last_move

    def get_starting_cell(self):
        cell_size = self.state.get_cell_size()

        board_width = self.board.size * cell_size
        board_height = self.board.size * cell_size

        screen_width, screen_height = self.state.get_screen_size()

        start_x = (screen_width - board_width) // 2
        start_y = (screen_height - board_height) // 2
        return (start_x, start_y)

    def update_starting_cell(self, starting_cell):
        self.starting_cell = starting_cell
        self.gameView.update_starting_cell(starting_cell)

    def is_outside_board(self, cell_x, cell_y):
        return cell_x >= self.board.get_size() or cell_y >= self.board.get_size() or cell_x < 0 or cell_y < 0

    # Takes a pixel and returns the position of the corresponding cell
    def get_pos(self, pixel: tuple) -> tuple:
        x, y = pixel
        cell_size = self.state.get_cell_size()
        (starting_cell_x,starting_cell_y) = self.get_starting_cell()
        cell_y = (x-starting_cell_x) // cell_size # Represents Columns
        cell_x = (y-starting_cell_y) // cell_size # Represents Rows
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
        next_player = self.get_next_player()
        return (next_player.get_stack_count() == 0 and len(next_player.get_cells()) == 0)

    def add_to_player_stack(self):
        current_player = self.get_current_player()
        current_player.add_stack_piece()

    def remove_from_player_stack(self):
        current_player = self.get_current_player()
        return current_player.remove_stack_piece()
    
    def add_to_player_cells_color(self, cell, color):
        if color == PIECE_ORANGE:
            self.orange.add_cell(cell)
            self.orange.add_piece()
        else:
            self.blue.add_cell(cell)
            self.blue.add_piece()
    
    def add_to_player_cells(self, cell, player):
        player.add_cell(cell)

    def remove_from_player_cells(self, cell, player):
        player.remove_cell(cell)

    def remove_piece(self, player):
        player.remove_piece()
    
    def unselect_cell(self):
        self.board.current_possible_moves = None
        self.board.selected_cell = None
        self.unselect_saved_player_stack(self.get_current_player())

    def no_cell_selected(self):
        return (self.board.current_possible_moves == None and self.get_current_player().stack_selected == False)
    
    def can_select_cell(self, cell):
        stack = self.board.get_stack(cell)
        return (self.board.is_player_stack(stack, self.get_current_player()))

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
            self.last_move = Move((None, None), cell, True)
            self.unselect_saved_player_stack(player)
            return True
        return False

    def move_stack(self, cell, player):
        made_move = False
        if cell in self.board.current_possible_moves:
            self.board.make_move(cell, player)
            made_move = True
            self.last_move = Move(self.board.selected_cell, cell)
        self.unselect_cell()
        return made_move

    def make_move(self, cell):
        player = self.get_current_player()
        if(player.stack_selected):
            return self.place_saved_piece(cell, player)
        else:
            return self.move_stack(cell, player)

    def is_bot_playing(self):
        return self.get_current_player().is_bot()
    
    def handle_hint(self, player):
        hint = self.get_hint(player)
        player.set_hint(hint)

    def get_hint(self, player) -> tuple:
        best_value = float('-inf')
        best_move = None
        best_moves_list = []
        for move in self.board.get_valid_moves(player):
            new_state = self.copy()
            initial_position = move.get_origin()
            destination = move.get_destination()
            
            if(move.is_from_personal_stack()):
                new_state.select_saved_player_stack(new_state.get_current_player())
                new_state.place_saved_piece(destination, new_state.get_current_player())
            else:
                new_state.select_cell(initial_position)
                new_state.make_move(destination)
            
            move_value = self.negamax(new_state, PLAYER_INT_DEPTH - 1, float('-inf'), float('inf'), 1, self.eval_hard)
            #print("Move: ", move, "Value: ", move_value)

            if move_value == best_value:
                best_moves_list.append(move)
            elif move_value > best_value:
                best_value = move_value
                best_moves_list = [move]
                
        best_move = random.choice(best_moves_list)
        return best_move
    
    def handle_easy_bot(self, bot):
        if bot.has_saved_pieces():
            self.select_saved_player_stack(bot)
            self.place_saved_piece(self.board.get_random_cell(), bot)
        else:
            selectable_cells = bot.get_cells()

            random_select = random.choice(selectable_cells)
            cell = tuple(int(num) for num in random_select)

            self.select_cell(cell)

            movable_cells = self.board.current_possible_moves
            random_move = random.choice(movable_cells)
            self.move_stack(random_move, bot)

    def handle_medium_bot(self, bot):

        best_value = float('-inf')
        best_move = None
        best_moves_list = []
        for move in self.board.get_valid_moves(bot):
            new_state = self.copy()
            initial_position = move.get_origin()
            destination = move.get_destination()
            
            if(move.is_from_personal_stack()):
                new_state.select_saved_player_stack(new_state.get_current_player())
                new_state.place_saved_piece(destination, new_state.get_current_player())
            else:
                new_state.select_cell(initial_position)
                new_state.make_move(destination)
            
            move_value = self.negamax(new_state, MEDIUM_BOT_DEPTH - 1, float('-inf'), float('inf'), 1, self.eval_medium)
            #print("Move: ", move, "Value: ", move_value)

            if move_value == best_value:
                best_moves_list.append(move)
            elif move_value > best_value:
                best_value = move_value
                best_moves_list = [move]

        best_move = random.choice(best_moves_list)
        if(best_move.is_from_personal_stack()):
            self.select_saved_player_stack(bot)
            self.place_saved_piece(best_move.get_destination(), bot)
        else :
            self.select_cell(best_move.get_origin())
            self.make_move(best_move.get_destination())

    def handle_hard_bot(self, bot):
        best_value = float('-inf')
        best_move = None
        best_moves_list = []
        for move in self.board.get_valid_moves(bot):
            new_state = self.copy()
            initial_position = move.get_origin()
            destination = move.get_destination()
            
            if(move.is_from_personal_stack()):
                new_state.select_saved_player_stack(new_state.get_current_player())
                new_state.place_saved_piece(destination, new_state.get_current_player())
            else:
                new_state.select_cell(initial_position)
                new_state.make_move(destination)
            
            move_value = self.negamax(new_state, HARD_BOT_DEPTH - 1, float('-inf'), float('inf'), 1, self.eval_hard)
            print("Move: ", move, " Value: ", move_value)

            if move_value == best_value:
                best_moves_list.append(move)
            elif move_value > best_value:
                best_value = move_value
                best_moves_list = [move]

        best_move = random.choice(best_moves_list)
        print("Best Move: ", best_move, " Value: ", best_value)
        if(best_move.is_from_personal_stack()):
            self.select_saved_player_stack(self.get_current_player())
            self.place_saved_piece(best_move.get_destination(), self.get_current_player())
        else:
            self.select_cell(best_move.get_origin())
            self.move_stack(best_move.get_destination(), bot)
            
    def handle_bot(self, bot):
        if(bot.is_easy_bot()):
            #sleep(0.2)
            self.handle_easy_bot(bot)
            return True
        elif(bot.is_medium_bot()):
            self.handle_medium_bot(bot)
            return True
        elif(bot.is_hard_bot()):
            self.handle_hard_bot(bot)
            return True
        return False

    def handle_player(self):
        player = self.get_current_player()
        has_played = False
        if player.is_bot():
            has_played = self.handle_bot(player)
        else:
            has_played = self.gameController.handle_event(player)

        if(has_played):
            if(not player.is_bot()):
                player.clear_hint()
            if(not self.did_win()):
                self.next_turn()
            has_played = False

    def run(self, window):
        self.handle_player()
        self.gameView.draw(window)

    def to_quit(self):
        self.state.to_quit()

    def eval_medium(self, state, depth) -> int:
        if state.verify_win():
            return 1000 + depth
        current_player = state.get_current_player()
        next_player = state.get_next_player()
        return len(current_player.get_cells()) - len(next_player.get_cells())
    
    # TODO: Implement a better evaluation function
    # 1. Quantos espaços está a controlar na board (quantos mais melhor)
    # 2. Quantos espaços tem na board (quantos mais melhor)
    # 3. Quantas peças tem no total (quantas mais melhor)
    # 4. Quantas peças tem na stack pessoal (quantas mais melhor)
    # TODO: 5. Verificar se estou a "vigiar" uma peça do adversário. Será ainda melhor se eu o conseguir ver e ele não me conseguir ver a mim
    # 6. Quantas peças do inimigo "escondeu"
    def eval_hard(self, state, depth) -> int:
        if state.verify_win():
            return 10000 + depth
        
        current_player = state.get_current_player()
        next_player = state.get_next_player()
        
        
        cells_difference = len(current_player.get_cells()) - len(next_player.get_cells())
        controlled_cells_difference = len(current_player.get_controlled_cells()) - len(next_player.get_controlled_cells())
        stack_difference = current_player.get_stack_count() - next_player.get_stack_count()

        hidden_enemy_pieces = next_player.get_total_pieces() - len(next_player.get_cells()) - next_player.get_stack_count()

        total_pieces_difference = current_player.get_total_pieces() - next_player.get_total_pieces()

        return cells_difference + 2*controlled_cells_difference + stack_difference + 3*total_pieces_difference + hidden_enemy_pieces

    def hash_board(self, board):
        return hashlib.sha256(str(board).encode()).hexdigest()

    def add_to_memo(self, state: 'GameState', depth: int, value: int, eval_func: str) -> None:
        current_player_stack = state.get_current_player().get_stack_count()
        next_player_stack = state.get_next_player().get_stack_count()

        board = state.board.get_board()
        board_hash = self.hash_board(board)
        GameState.memo[((board_hash, current_player_stack, next_player_stack), eval_func, depth)] = value

        mirror_board = state.board.get_mirror_board(board)
        mirror_board_hash = self.hash_board(mirror_board)
        GameState.memo[((mirror_board_hash, current_player_stack, next_player_stack), eval_func, depth)] = value
        
        inverse_board = state.board.get_inverse_board(board)
        inverse_board_hash = self.hash_board(inverse_board)
        GameState.memo[((inverse_board_hash, next_player_stack, current_player_stack), eval_func, depth)] = -value

    def negamax(self, state: 'GameState', depth: int, alpha: int, beta: int, color: int, eval_func) -> int:
        if depth == 0 or state.verify_win():
            return color * eval_func(state, depth)
        

        key = ((self.hash_board(state.board.get_board()), state.get_current_player().get_stack_count(), state.get_next_player().get_stack_count()), eval_func.__name__, depth)
        if key in GameState.memo:
            return GameState.memo[key]

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

            eval = -new_state.negamax(new_state, depth-1, -beta, -alpha, -color, eval_func)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        self.add_to_memo(state, depth, maxEval, eval_func.__name__)

        return maxEval
    
    def minimax(self, state, depth, alpha, beta, maximizingPlayer, player, opponent):
        if depth == 0 or state.verify_win():
            return state.eval()
        
        if (state.board.get_board(), depth) in GameState.memo:
            return GameState.memo[(state.board.get_board(), depth)]

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in state.board.get_valid_moves(state.get_current_player()):

                new_state = state.copy()
                initial_position = move.get_origin()
                destination = move.get_destination()

                if(move.is_from_personal_stack()):
                    new_state.select_saved_player_stack(new_state.get_current_player())
                    new_state.place_saved_piece(destination, new_state.get_current_player())
                else:
                    new_state.select_cell(initial_position)
                    new_state.make_move(destination)

                eval = new_state.minimax(new_state, depth-1, alpha, beta, False, player, opponent)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            GameState.memo[(state.board.get_board(), depth)] = maxEval
            return maxEval
        else:
            minEval = float('inf')
            for move in state.board.get_valid_moves(state.get_current_player()):

                new_state = state.copy()
                initial_position = move.get_origin()
                destination = move.get_destination()

                if(move.is_from_personal_stack()):
                    new_state.select_saved_player_stack(new_state.get_current_player())
                    new_state.place_saved_piece(destination, new_state.get_current_player())
                else:
                    new_state.select_cell(initial_position)
                    new_state.make_move(destination)

                eval = new_state.minimax(new_state, depth-1, alpha, beta, True, player, opponent)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            GameState.memo[(state.board.get_board(), depth)] = minEval
            return minEval