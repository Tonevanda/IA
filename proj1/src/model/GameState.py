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
    # ((board, player1, player2, eval_func, depth) -> value
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

    # Copy constructor since we can't use the deepcopy method
    def copy(self):
        new_state = GameState.__new__(GameState) # This way it creates a new GameState without initializing it
        new_state.state = self.state 
        new_state.turn = self.turn
        new_state.orange = copy.deepcopy(self.orange)
        new_state.blue = copy.deepcopy(self.blue)
        new_state.board = self.board.copy(new_state)
        return new_state

    # Returns the last move
    def get_last_move(self):
        return self.last_move

    # Returns the starting cell, it's used to calculate the positions of the display
    def get_starting_cell(self):
        cell_size = self.state.get_cell_size()

        board_width = self.board.size * cell_size
        board_height = self.board.size * cell_size

        screen_width, screen_height = self.state.get_screen_size()

        start_x = (screen_width - board_width) // 2
        start_y = (screen_height - board_height) // 2
        return (start_x, start_y)

    # Checks if a given cell is outside the board
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
    
    # Returns the current player
    def get_current_player(self):
        return self.orange if self.turn % 2 == 1 else self.blue
    
    # Returns the next player
    def get_next_player(self):
        return self.orange if self.turn % 2 == 0 else self.blue

    # Skips to the next turn
    def next_turn(self):
        self.turn += 1

    # Checks if the game has ended and returns the value
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

    # Verifies if the current player has won. It checks if the current player has no pieces in their stack and no cells, therefore, can't play
    def verify_win(self):
        next_player = self.get_next_player()
        return (next_player.get_stack_count() == 0 and len(next_player.get_cells()) == 0)

    # Adds a piece to the current player's saved piece's stack
    def add_to_player_stack(self):
        current_player = self.get_current_player()
        current_player.add_stack_piece()

    # Removes a piece from the current player's saved piece's stack
    def remove_from_player_stack(self):
        current_player = self.get_current_player()
        return current_player.remove_stack_piece()
    
    # Adds a cell to a given player cell by the color of the piece
    def add_to_player_cells_color(self, cell, color):
        if color == PIECE_ORANGE:
            self.orange.add_cell(cell)
            self.orange.add_piece()
        else:
            self.blue.add_cell(cell)
            self.blue.add_piece()
    
    # Adds a cell to a player's list of cells
    def add_to_player_cells(self, cell, player):
        player.add_cell(cell)

    # Removes a cell from a player's list of cells
    def remove_from_player_cells(self, cell, player):
        player.remove_cell(cell)

    # Removes a piece from a players sum of total pieces
    def remove_piece(self, player):
        player.remove_piece()
    
    # Unselects the cell currently selected
    def unselect_cell(self):
        self.board.current_possible_moves = None
        self.board.selected_cell = None
        self.unselect_saved_player_stack(self.get_current_player())

    # Checks if nothing is selected (a cell or the player stack)
    def no_cell_selected(self):
        return (self.board.current_possible_moves == None and self.get_current_player().stack_selected == False)
    
    # Checks if a cell can be selected by the current player
    def can_select_cell(self, cell):
        stack = self.board.get_stack(cell)
        return (self.board.is_player_stack(stack, self.get_current_player()))

    # Selects a cell or unselects if the player can't select any cell
    def select_cell(self, cell):
        if self.can_select_cell(cell):
            self.board.current_possible_moves = self.board.get_possible_moves(cell)
            self.board.selected_cell = cell
        else: 
            self.unselect_cell()

    # Handles the selection of a player's stack
    def handle_saved_player_stack_selection(self, player):
        if player.stack_selected: # If the player's stack is already selected, unselect it
            self.unselect_saved_player_stack(player)
        else: #  If the player's stack is not selected, select it
            self.select_saved_player_stack(player)

    # Selects a player's stack
    def select_saved_player_stack(self, player):
        if(not player.has_saved_pieces()): # If the player has no pieces in their stack they shouldn't be able to select the stack
            return
        player.select_stack()
    
    # Unselects a player's stack
    def unselect_saved_player_stack(self, player):
        player.unselect_stack()

    # Places a piece from the player's stack to a given cell and returns True if the move was made
    def place_saved_piece(self, cell, player):
        if player.stack_selected: # They can only place the piece if the stack is selected
            self.board.place_saved_piece(cell, player)
            self.remove_from_player_stack()
            self.last_move = Move((None, None), cell, True)
            self.unselect_saved_player_stack(player)
            return True
        return False

    # Moves a stack to a given cell and returns True if the move was made
    def move_stack(self, cell):
        made_move = False
        if cell in self.board.current_possible_moves: # If the cell is a valid move
            self.board.make_move(cell)
            made_move = True
            self.last_move = Move(self.board.selected_cell, cell)
        self.unselect_cell()
        return made_move

    # Calls the appropriate method to make a move, depending on if it's from the stack or from the board
    def make_move(self, cell):
        player = self.get_current_player()
        if(player.stack_selected):
            return self.place_saved_piece(cell, player)
        else:
            return self.move_stack(cell)

    # Returns if the current player is a bot
    def is_bot_playing(self):
        return self.get_current_player().is_bot()
    
    # Handles the hint for the player
    def handle_hint(self, player):
        if(player.get_hint() != None): # If the player already has a hint
            return
        hint = self.get_hint() # Get the hint
        player.set_hint(hint) # Set the hint for the player

    # Returns the hint for the player using the minimax algorithm and the heuristics used in the hard bot, but with it's own depth
    def get_hint(self) -> tuple:
        state = self.copy()
        _, best_move = self.minimax(state, PLAYER_HINT_DEPTH, float('-inf'), float('inf'), True, self.eval_hard)

        if best_move == None:
            best_move = self.board.get_valid_moves(self.get_current_player())[0] # if it can't find a move, it returns the first valid move (only if depth is 0)

        return best_move
    
    # Handles the monte carlo tree search bot's move
    def handle_mcts_bot(self, bot):
        mcts = MCTS(self.copy()) # Create a new MCTS object with a copy of the current state
        best_node = mcts.search(num_iterations=MCTS_ITERATIONS)

        best_move = best_node.state.get_last_move()
        if best_move.is_from_personal_stack(): # if it's from the personal stack, play the piece from the stack
            self.select_saved_player_stack(bot)
            self.place_saved_piece(best_move.get_destination(), bot)
        else: # if it's from the board, move the stack
            self.select_cell(best_move.get_origin())
            self.make_move(best_move.get_destination())

    # Handles the easy bot's move
    def handle_easy_bot(self, bot):
        if bot.has_saved_pieces(): # if it has a piece in a stack, randomly place it
            self.select_saved_player_stack(bot)
            self.place_saved_piece(self.board.get_random_cell(), bot)
        else: # else, pick a random cell and move it
            selectable_cells = bot.get_cells()

            cell = random.choice(list(selectable_cells))

            self.select_cell(cell)

            movable_cells = self.board.current_possible_moves
            random_move = random.choice(movable_cells)
            self.move_stack(random_move)

    # Handles the medium bot's move
    def handle_medium_bot(self, bot):
        state = self.copy()
        best_value, best_move = self.negamax(state, MEDIUM_BOT_DEPTH, float('-inf'), float('inf'), 1, self.eval_medium) # Calls negamax since the heuristics used in the eval_medium function are zero-sum

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
            self.handle_easy_bot(bot) # if it can't find a move, play randomly (only if depth is 0)

    # Handles the hard bot's move
    def handle_hard_bot(self, bot):
        state = self.copy()
        _, best_move = self.minimax(state, HARD_BOT_DEPTH, float('-inf'), float('inf'), True, self.eval_hard) # Calls minimax with the heuristics used in the eval_hard function

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
    
    # Handle bot function that calls the appropriate method to make a move depending on the bot's difficulty
    # Returns true if a move is made
    def handle_bot(self, bot):
        if(bot.is_easy_bot()):
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

    # Handles the player's move
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
            has_played = self.gameController.handle_event(player) # Calls the handle event in gameController to handle the player's input

        if(has_played): # If the player has played
            if(not player.is_bot()): 
                player.clear_hint() # If it was a human player, clear the hint
            if(not self.did_win()): # If the game hasn't ended, go to the next turn
                self.next_turn()
            has_played = False

    # Run loop
    def run(self, window):
        self.handle_player()
        self.gameView.draw(window)

    # Function used to quit the game
    def to_quit(self):
        self.state.to_quit()
    
    # Heuristic function used to evaluate the state of the game. It returns the difference between the current player's total pieces and the next player's total pieces
    # Having more pieces than your opponent is a good thing, as you win the game if your opponent can't move and, this way, they have less chance of capturing your stacks
    def eval_total_pieces(self, current_player, next_player) -> int:
        return current_player.get_total_pieces() - next_player.get_total_pieces()

    # Heuristic function used to evaluate the state of the game. It returns the difference between the current player's cells and the next player's cells
    # Having more cells than your opponent is a good thing, as you win the game if your opponent doesn't have any cell left (and any piece in the stack)
    def eval_cells(self, current_player, next_player) -> int:
        return len(current_player.get_cells()) - len(next_player.get_cells())
    
    # Heuristic function used to evaluate the state of the game. It returns the difference between the current player's controlled cells and the next player's controlled cells
    # Controlling more cells than your opponent will lead to more possible moves and more chances of capturing their stacks
    def eval_controlled_cells(self, current_player, next_player) -> int:
        return len(current_player.get_controlled_cells()) - len(next_player.get_controlled_cells())
    
    # Heuristic function used to evaluate the state of the game. It returns the difference between the current player's cells controlled by the opponent and the opponent's cells controlled by the current player
    # It's good to have cells looking at the opponent's cells, as it gives you more chances of capturing their stacks, but it's bad to have your cells controlled by the opponent as they can capture them
    def eval_cells_controlled_by_opponent(self, current_player, next_player) -> int:
        player_cells = current_player.get_cells()
        opponent_control = next_player.get_controlled_cells()
        opponent_cells = next_player.get_cells()
        player_control = current_player.get_controlled_cells()

        return -len(player_cells & opponent_control) + len(opponent_cells & player_control)
    
    # Heuristic function used to evaluate the state of the game. It returns the difference between the current player's stack and the next player's stack
    # Having more pieces in your stack is a good thing, as you can place them in the board and capture your opponent's stacks anywhere you want
    def eval_stack(self, current_player, next_player) -> int:
        return current_player.get_stack_count() - next_player.get_stack_count()
    
    # Heuristic function used to evaluate the state of the game. It returns the amount of enemy pieces are inside a player's stack
    # Having enemy pieces inside your stack is a good thing, because this way the opponent can't move them and you can use them to move your stack even further
    def eval_hidden_enemy_pieces(self, state, current_player) -> int:
        return state.board.get_enemy_pieces_in_my_control(current_player)

    # Evaluation function for the medium bot. It uses 2 heuristics, if it's a win, it returns a high value, otherwise, it uses the total pieces heuristic
    def eval_medium(self, state, depth) -> int:
        if state.verify_win():
            return 10000 + depth # 10000 plus depth, so that it always chooses the move that wins the game in the least amount of turns
        return  state.eval_total_pieces(state.get_current_player(), state.get_next_player())

    # Evaluation function for the hard bot. It uses 6 heuristics, if it's a win, it returns a high value, otherwise, it uses the total pieces, cells, controlled cells, stack, hidden enemy pieces and cells controlled by the opponent heuristics
    def eval_hard(self, state, depth) -> int:
        if state.verify_win():
            return 10000 + depth # 10000 plus depth, so that it always chooses the move that wins the game in the least amount of turns

        return (
            (5*state.eval_total_pieces(state.get_current_player(), state.get_next_player())) +
            (4*state.eval_cells(state.get_current_player(), state.get_next_player())) + 
            (1*state.eval_controlled_cells(state.get_current_player(), state.get_next_player())) +
            (1*state.eval_stack(state.get_current_player(), state.get_next_player())) +
            (4*state.eval_hidden_enemy_pieces(state, state.get_current_player())) +
            (2*state.eval_cells_controlled_by_opponent(state.get_current_player(), state.get_next_player()))
        )
    
    # Function used for the memoization of the values of the states
    def add_to_memo(self, state: 'GameState', depth: int, value: int, eval_func: str) -> None:
        current_player = state.get_current_player()
        next_player = state.get_next_player()

        board = state.board.get_board()

        key = str((board, repr(current_player), repr(next_player), eval_func, depth)) # Creates a key with the board, the current player, the next player, the evaluation function and the depth
        key_hash = hashlib.sha256(key.encode()).hexdigest() # Hashes the key for better performance 
        GameState.memo[key_hash] = value # Adds the value to the memo

        opponent_key = str((board, repr(next_player), repr(current_player), eval_func, depth)) # Swaps the current player and the next player to save the same board, but for the opponent
        opponent_key_hash = hashlib.sha256(opponent_key.encode()).hexdigest()
        GameState.memo[opponent_key_hash] = -value # Adds the negative value to the memo

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
            if alpha >= beta:
                GameState.branches_pruned_total += 1
                GameState.branches_pruned_move += 1
                break

        self.add_to_memo(state, depth, maxEval, eval_func.__name__)

        return maxEval, random.choice(best_moves)
    
    def minimax(self, state, depth, alpha, beta, maximizingPlayer, eval_func):
        if depth == 0 or state.verify_win():
            return eval_func(state, depth), None

        GameState.states_evaluated += 1
        key = str((state.board.get_board(), repr(state.get_current_player()), repr(state.get_next_player()), eval_func.__name__, depth))
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        if key_hash in GameState.memo:
            GameState.states_avoided += 1
            return GameState.memo[key_hash], None

        best_move = None

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

                eval, _ = new_state.minimax(new_state, depth-1, alpha, beta, False, eval_func)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    GameState.branches_pruned_total += 1
                    GameState.branches_pruned_move += 1
                    break
            GameState.memo[(state.board.get_board(), depth)] = maxEval
            return maxEval, best_move
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

                eval, _ = new_state.minimax(new_state, depth-1, alpha, beta, True, eval_func)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    GameState.branches_pruned_total += 1
                    GameState.branches_pruned_move += 1
                    break
            self.add_to_memo(state, depth, minEval, eval_func.__name__)
            return minEval, best_move