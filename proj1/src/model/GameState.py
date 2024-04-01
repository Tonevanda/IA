from model.Board import Board
from model.MCTS import MCTS
from model.Move import Move
from controller.GameController import GameController
from view.GameView import GameView
from config import PIECE_ORANGE, MEDIUM_BOT_DEPTH, HARD_BOT_DEPTH, PLAYER_HINT_DEPTH, MCTS_ITERATIONS
from typing import Dict
from collections import defaultdict
import random
import copy
import hashlib
import time


class GameState:
    # Hashmap that stores, for each pair of board, and pair of player stacks, and depth, the value of the state
    # ((board hash, player1_stack, player2_stack), eval_func, depth) -> value
    # TODO: Could be a hash of the whole state (hash256 has 2^256 so probability of collisions is low and it is better and more efficient)
    #memo: Dict[Tuple[Tuple[str, int, int], str, int], int] = defaultdict(int)
    memo: Dict[str, int] = defaultdict(int)
    states_evaluated = 0
    states_avoided = 0
    branches_pruned_total = 0
    branches_pruned_move = 0

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
            print("States evaluated: ", GameState.states_evaluated)
            print("States avoided: ", GameState.states_avoided)
            print("Total branches pruned: ", GameState.branches_pruned_total)
            GameState.branches_pruned_total = 0
            GameState.branches_pruned_move = 0
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
        if(player.get_hint() != None):
            return
        hint = self.get_hint()
        player.set_hint(hint)

    def get_hint(self) -> tuple:
        state = self.copy()
        _, best_move = self.negamax(state, PLAYER_HINT_DEPTH, float('-inf'), float('inf'), 1, self.eval_hard)

        if best_move == None:
            best_move = self.board.get_valid_moves(self.get_current_player())[0]

        return best_move
    
    def handle_mcts_bot(self, bot):
        mcts = MCTS(self.copy())
        best_node = mcts.search(num_iterations=MCTS_ITERATIONS)

        best_move = best_node.state.get_last_move()
        print(f"Best move: {best_move}")
        if best_move.is_from_personal_stack():
            self.select_saved_player_stack(bot)
            self.place_saved_piece(best_move.get_destination(), bot)
        else:
            self.select_cell(best_move.get_origin())
            self.make_move(best_move.get_destination())

    def handle_easy_bot(self, bot):
        if bot.has_saved_pieces():
            self.select_saved_player_stack(bot)
            self.place_saved_piece(self.board.get_random_cell(), bot)
        else:
            selectable_cells = bot.get_cells()

            cell = random.choice(list(selectable_cells))

            self.select_cell(cell)

            movable_cells = self.board.current_possible_moves
            random_move = random.choice(movable_cells)
            self.move_stack(random_move, bot)

    def handle_medium_bot(self, bot):
        state = self.copy()
        best_value, best_move = self.negamax(state, MEDIUM_BOT_DEPTH, float('-inf'), float('inf'), 1, self.eval_medium)

        if best_move != None:
            initial_position = best_move.get_origin()
            destination = best_move.get_destination()
            if(best_move.is_from_personal_stack()):
                self.select_saved_player_stack(self.get_current_player())
                self.place_saved_piece(destination, self.get_current_player())
            else:
                self.select_cell(initial_position)
                self.make_move(destination)
        else:
            self.handle_easy_bot(bot)

    def handle_hard_bot(self, bot):
        state = self.copy()
        _, best_move = self.negamax(state, HARD_BOT_DEPTH, float('-inf'), float('inf'), 1, self.eval_hard)

        if best_move != None:
            initial_position = best_move.get_origin()
            destination = best_move.get_destination()

            if(best_move.is_from_personal_stack()):
                self.select_saved_player_stack(self.get_current_player())
                self.place_saved_piece(destination, self.get_current_player())
            else:
                self.select_cell(initial_position)
                self.make_move(destination)
            print("Move made: ", best_move)
        else:
            print("Playing random")
            self.handle_easy_bot(bot)
            
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
        elif(bot.is_mcts_bot()):
            self.handle_mcts_bot(bot)
            return True
        return False

    def handle_player(self):
        player = self.get_current_player()
        has_played = False
        if player.is_bot():
            print(f"------------------- {player} is playing (Turn {self.turn}) -------------------")
            start = time.time()
            has_played = self.handle_bot(player)
            print(f"{self.get_current_player()} took {time.time() - start} seconds to make a move!")
            print(f"Branched pruned this move: {GameState.branches_pruned_move}")
            GameState.branches_pruned_move = 0
            print("\n")
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
    
    def eval_total_pieces(self, current_player, next_player) -> int:
        return current_player.get_total_pieces() - next_player.get_total_pieces()

    def eval_cells(self, current_player, next_player) -> int:
        return len(current_player.get_cells()) - len(next_player.get_cells())
    
    def eval_controlled_cells(self, current_player, next_player) -> int:
        return len(current_player.get_controlled_cells()) - len(next_player.get_controlled_cells())
    
    def eval_stack(self, current_player, next_player) -> int:
        return current_player.get_stack_count() - next_player.get_stack_count()
    
    def eval_hidden_enemy_pieces(self, state, current_player, next_player) -> int:
        return state.board.get_enemy_pieces_in_my_control(current_player) - state.board.get_enemy_pieces_in_my_control(next_player)

    #def eval_medium(self, state, depth) -> int:
    #    if state.verify_win():
    #        return 10000 + depth
    #    return  state.eval_total_pieces(state.get_current_player(), state.get_next_player())

    def eval_medium(self, state, depth) -> int:
        if state.verify_win():
            return 10000 + depth
        return ((4 * state.eval_total_pieces(state.get_current_player(), state.get_next_player())) + 
                (3 * state.eval_cells(state.get_current_player(), state.get_next_player())) + 
                (2 * state.eval_controlled_cells(state.get_current_player(), state.get_next_player())) + 
                (state.eval_stack(state.get_current_player(), state.get_next_player())) + 
                (state.board.eval_board(state.get_current_player()) - state.board.eval_board(state.get_next_player()))
                )

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
        return ((4 * state.eval_total_pieces(state.get_current_player(), state.get_next_player())) + 
                (3 * state.eval_cells(state.get_current_player(), state.get_next_player())) + 
                (2 * state.eval_controlled_cells(state.get_current_player(), state.get_next_player())) + 
                (state.eval_stack(state.get_current_player(), state.get_next_player())) + 
                (state.eval_hidden_enemy_pieces(state, state.get_current_player(), state.get_next_player()))
                )
    
    def add_to_memo(self, state: 'GameState', depth: int, value: int, eval_func: str) -> None:
        current_player = state.get_current_player()
        next_player = state.get_next_player()

        board = state.board.get_board()

        key = str((board, repr(current_player), repr(next_player), eval_func, depth))
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        GameState.memo[key_hash] = value

        opponent_key = str((board, repr(next_player), repr(current_player), eval_func, depth))
        opponent_key_hash = hashlib.sha256(opponent_key.encode()).hexdigest()
        GameState.memo[opponent_key_hash] = -value

        mirror_board = state.board.get_mirror_board(board)
        mirror_key = str((mirror_board, repr(current_player), repr(next_player), eval_func, depth))
        mirror_key_hash = hashlib.sha256(mirror_key.encode()).hexdigest()
        GameState.memo[mirror_key_hash] = value

        opponent_mirror_key = str((mirror_board, repr(next_player), repr(current_player), eval_func, depth))
        opponent_mirror_key_hash = hashlib.sha256(opponent_mirror_key.encode()).hexdigest()
        GameState.memo[opponent_mirror_key_hash] = -value

    def negamax(self, state: 'GameState', depth: int, alpha: int, beta: int, color: int, eval_func) -> tuple:
        if depth == 0 or state.verify_win():
            return color * eval_func(state, depth), None

        GameState.states_evaluated += 1
        key = str((state.board.get_board(), repr(state.get_current_player()), repr(state.get_next_player()), eval_func.__name__, depth))
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash in GameState.memo:
            GameState.states_avoided += 1
            return GameState.memo[key_hash], None

        maxEval = float('-inf')
        best_moves = []
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

            value = -new_state.negamax(new_state, depth-1, -beta, -alpha, -color, eval_func)[0]
            if value > maxEval:
                maxEval = value
                best_moves = [move]
            elif value == maxEval:
                best_moves.append(move)
            alpha = max(alpha, value)
            if beta <= alpha:
                GameState.branches_pruned_total += 1
                GameState.branches_pruned_move += 1
                break

        self.add_to_memo(state, depth, maxEval, eval_func.__name__)

        return maxEval, random.choice(best_moves)
    
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