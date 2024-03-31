from config import PIECE_BLUE, PIECE_ORANGE, PIECE_EMPTY, STACK_MASKS, STACK_MAX_SIZES
from model.Move import Move
from model.Player import Player
import random
import numpy as np

class Board:
    def __init__(self, game_state, size):
        self.game_state = game_state
        self.size = size
        self.stack_size = STACK_MAX_SIZES[size]
        self.stack_mask = STACK_MASKS[size]
        self.board = 0b0
        self.placeable_cells = []
        self.make_board()
        
        self.selected_cell = None

        # TODO: Refactor so this is inside Player.py
        self.current_possible_moves = None
    
    def update_board(self, new_board: 'Board') -> None:
        self.board = new_board

    def get_board(self) -> int:
        return self.board
    
    def get_mirror_board(self, board: int) -> int:
        new_board = 0b0
        size_total = self.size * self.size
        for i in range(size_total):
            stack = self.get_bitboard_stack(i, board)
            new_board |= stack << ((size_total - i - 1) * self.stack_size * 2)
        return new_board
    
    # TODO: Maybe implement this
    def get_transpose_board(self, board) -> int:
        pass
    
    def get_rotated_board(self, board) -> int:
        pass
    
    def get_bitboard_stack(self, bitboard_pos: int, board: int) -> int:
        return (board >> (bitboard_pos * self.stack_size * 2)) & self.stack_mask

    def get_inverse_board(self, board) -> int:
        new_board = 0b0
        for i in range(self.size * self.size):
            stack = self.get_bitboard_stack(i, board)
            if(not self.is_none_stack(stack) and not self.is_empty_stack(stack)):
                for j in range(self.stack_size):
                    piece = (stack >> (j*2)) & 0b11
                    if piece == PIECE_EMPTY:
                        new_piece = PIECE_EMPTY
                    else:
                        new_piece = PIECE_ORANGE if piece == PIECE_BLUE else PIECE_BLUE
                    new_board |= new_piece << (i * self.stack_size * 2 + j*2)
            else:
                new_board |= stack << (i * self.stack_size * 2)
        return new_board

    def get_size(self) -> int:
        return self.size
    
    def get_total_cells(self) -> int:
        return self.size * self.size
    
    def copy(self, game_state) -> 'Board':
        new_board = Board.__new__(Board)  # Create a new Board instance without calling __init__
        new_board.game_state = game_state  # Copy game_state
        new_board.size = self.size  # Copy size
        new_board.stack_size = self.stack_size  # Copy stack_size
        new_board.stack_mask = self.stack_mask  # Copy stack_mask
        new_board.board = self.board  # Copy board state
        new_board.selected_cell = self.selected_cell  # Copy selected_cell
        new_board.placeable_cells = list(self.placeable_cells) if self.placeable_cells else None  # Create a new list from placeable_cells
        new_board.current_possible_moves = list(self.current_possible_moves) if self.current_possible_moves else None  # Create a new list from current_possible_moves
        return new_board

    def get_random_cell(self) -> tuple:
        return random.choice(self.placeable_cells)

    # Checks if the cell is on the edge of the board
    def is_on_edge(self, row: int, col: int) -> bool:
        cut = int(self.size * 0.25)
        return (row == 0 or row < cut-1) or (row == self.size-1 or row > self.size-cut) or (col == 0 or col < (cut-1)) or (col == self.size-1 or col > self.size-cut)
    
    # Adds a single piece to the board
    def make_piece(self, color: int) -> None:
        self.board <<= 2
        self.board |= color

    # Adds a stack to the board
    def make_stack(self, color: int) -> None:
        for _ in range(self.stack_size - 1): # Add the pieces to the stack given the stack size
            self.make_piece(PIECE_EMPTY)
        self.make_piece(color)

    # Creates the board with the initial pieces
    def make_board(self) -> None:
        column_counter = 0
        row_counter = 0
        current_color = PIECE_ORANGE
        first = True

        for row in range(self.size):
            for col in range(self.size):
                if not self.is_on_edge(row, col): # If the cell is not on the edge of the board (where the pieces are placed)
                    self.make_stack(current_color) # Add a stack to the board
                    self.game_state.add_to_player_cells_color((self.size-row-1, self.size-col-1), current_color) # Add the cell to the player's cells for better performance
                    column_counter += 1
                    if column_counter % 2 == 0:
                        current_color = PIECE_BLUE if current_color == PIECE_ORANGE else PIECE_ORANGE
                else:
                    if(first): # If it's the first time we are adding the pieces to the board
                        self.board |= PIECE_EMPTY # Add an empty piece to the board
                        for _ in range(self.stack_size - 2):
                            self.make_piece(PIECE_EMPTY)
                        first = False
                    else:
                        self.make_stack(PIECE_EMPTY)
                self.placeable_cells.append((row, col))
            row_counter += 1
            if row_counter % 2 == 0:
                current_color = PIECE_BLUE
            else:
                current_color = PIECE_ORANGE

        self.make_hexagon()

    # Given a stack position and a new stack, substitutes the stack in the board
    def substitute_stack(self, stack_position: int, new_stack: int) -> None:
        self.board &= ~(self.stack_mask << (stack_position * self.stack_size * 2)) # Remove the stack from the board
        self.board |= (new_stack << (stack_position * self.stack_size * 2)) # Add the new stack to the board

    # Converts a row and column to a position in the bitmap (it's a bitboard but wtv) 
    def get_bitmap_position(self, row: int, col: int) -> int:
        return row * self.size + col

    # Creates the hexagon shape in the board by removing the pieces that are outside the hexagon
    def make_hexagon(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                bitmap_position = self.get_bitmap_position(i, j)
                if(self.is_outside_board((i,j))): # If the cell is outside the hexagon
                    self.substitute_stack(bitmap_position, self.stack_mask) # Remove the stack from the board by adding a NONE stack (0b11)
                    self.placeable_cells.remove((i,j)) # Remove the cell from the placeable cells

    # Checks if a cell is outside the hexagon
    def is_outside_board(self, cell: tuple) -> bool:
        cut = int(self.size * 0.25)
        (i,j) = cell
        if i < cut and j < cut - i:
            return True
        elif i < cut and j > self.size - (cut - i) - 1:
            return True
        elif i >= self.size - cut and j < cut - (self.size - i - 1):
            return True
        elif i >= self.size - cut and j > self.size - (cut - (self.size - i - 1)) - 1:
            return True

    # Takes a position and returns the stack at that position
    def get_stack(self, cell: tuple) -> int:
        row, col = cell
        bitmap_pos = self.get_bitmap_position(row, col) # Get the position in the bitmap
        return (self.board >> (bitmap_pos * self.stack_size * 2)) & self.stack_mask # Get the stack at the position

    def is_none_stack(self, stack: int) -> bool:
        return stack == self.stack_mask # A none stack is a stack filled with 0b11 aka a stack_mask
    
    def is_empty_stack(self, stack: int) -> bool:
        return (stack ^ self.stack_mask) == self.stack_mask # An empty stack is a stack filled with 0b00

    # returns the selected cell
    def get_selected_cell(self) -> tuple:
        return self.selected_cell

    # returns the selected stack
    def get_selected_stack(self) -> int:
        if self.selected_cell is not None:
            return self.get_stack(self.selected_cell)
        return None
    
    # Returns the number of pieces in a stack
    def get_stack_size(self, stack: int) -> int:
        return bin(stack).count("1") # Since Orange is 01 and Blue is 10, we can count the number of 1s to get the number of pieces
    
    def is_valid_cell(self, cell: tuple) -> bool:
        return cell in self.placeable_cells

    # Takes a cell and returns a list of possible moves from the corresponding cell
    def get_possible_moves(self, cell: tuple) -> list[tuple]:
        x, y = cell
        stack = self.get_stack(cell)
        max_move = self.get_stack_size(stack)  # The maximum number of moves is the number of pieces in the stack

        if max_move > 0:
            moves = [(x + dx, y) for dx in range(-max_move, max_move + 1) 
                    if dx != 0 and 0 <= x + dx < self.size and not self.is_outside_board((x + dx, y))]
            moves += [(x, y + dy) for dy in range(-max_move, max_move + 1) 
                    if dy != 0 and 0 <= y + dy < self.size and not self.is_outside_board((x, y + dy))]
            return moves
        return None


    def remove_from_stack(self, stack: int, num_pieces: int, stack_pieces: int) -> int:
        for i in range(num_pieces):
            stack &= ~(0b11 << ((stack_pieces-i) * 2)) # Remove n bottom pieces from the stack
        return stack & self.stack_mask # Return the new stack with the proper size

    # Returns the pieces removed from the stack
    def get_removed_from_stack(self, stack: int, num_pieces: int, stack_pieces: int) -> int:
        removed = 0b0

        for i in range(num_pieces): # For each piece removed
            piece_removed = (stack & (0b11 << ((stack_pieces-i)*2))) >> ((stack_pieces-i)*2) # Get the piece removed
            removed <<= 2 # Shift the removed pieces to the left
            removed |= piece_removed # Add the piece removed to the removed pieces
            stack &= ~(0b11 << ((stack_pieces-i)*2))  # Remove the piece from the stack
        return removed # Return the removed pieces
    
    # Adds new pieces to a given stack
    def add_pieces_to_stack(self, stack: int, removed_stack: int) -> int:
        stack_size = self.get_stack_size(stack)
        shift = stack_size * 2 # Get where to add the new pieces
        removed_stack <<= shift # Shift the removed pieces (new pieces) to the right position
        stack |= removed_stack # Add the removed pieces (new pieces) to the stack
        return stack

    # Returns the Manhattan distance between two cells
    def get_distance_between_cells(self, source: tuple, destination: tuple) -> int:
        return abs(destination[0] - source[0]) + abs(destination[1] - source[1])

    # Handles the pieces removed from a stack
    def handle_removed_pieces(self, removed_pieces: int) -> None:
        amount = self.get_stack_size(removed_pieces) # The number of pieces removed
        for i in range(amount):
            piece = removed_pieces & (0b11 << (i*2)) # Get the piece removed
            if piece == self.game_state.get_current_player().get_color_bits(): # If the piece removed is from the current player
                self.game_state.add_to_player_stack() # Add the piece to the current player's stack
            else:
                self.game_state.remove_piece(self.game_state.get_next_player())

    # Handles the stack size limit by removing the pieces that exceed the limit
    def handle_stack_size_limit(self, stack: int, bitmap_position: int) -> None:
        stack_size = self.get_stack_size(stack)

        if(stack_size > self.stack_size): # If the stack exceeds the limit
            overflow = stack_size - self.stack_size # Get the number of pieces that exceed the limit
            rest = stack & ~(self.stack_mask << overflow*2) # Get the pieces that don't exceed the limit
            stack = (stack & (self.stack_mask << overflow*2)) >> (overflow*2) # Get the pieces that exceed the limit
            self.handle_removed_pieces(rest) # Calls the function that will handle the pieces that exceed the limit by adding to the player stack or deleting them
        self.substitute_stack(bitmap_position, stack) # Update the stack in the board
        
    # Transfers the pieces from a stack to another
    def transfer_pieces(self, source: tuple, destination: tuple) -> None:
        source_pos = self.get_bitmap_position(source[0], source[1]) # Get the position of the source stack in the bitmap
        destination_pos = self.get_bitmap_position(destination[0], destination[1]) # Get the position of the destination stack in the bitmap
        distance = self.get_distance_between_cells(source, destination) # Calculates the distance between the source and destination

        source_stack = self.get_stack(source) # Get the source stack (before the move)
        destination_stack = self.get_stack(destination) # Get the destination stack (before the move)

        source_stack_size = self.get_stack_size(source_stack)-1

        new_source_stack = self.remove_from_stack(source_stack, distance, source_stack_size) # Remove the pieces from the source stack
        removed_stack = self.get_removed_from_stack(source_stack, distance, source_stack_size) # Get the pieces removed from the source stack
        new_destination_stack = self.add_pieces_to_stack(destination_stack, removed_stack) # Add the pieces removed from the source stack to the destination stack

        # Add the destination of the moving stack to the current player's cells
        self.game_state.add_to_player_cells(destination, self.game_state.get_current_player())
        
        # if the destination belonged to the opponent, remove it from the opponent's cells
        if(self.is_player_stack(destination_stack, self.game_state.get_next_player())):
            self.game_state.remove_from_player_cells(destination, self.game_state.get_next_player())

        self.substitute_stack(source_pos, new_source_stack) # Replace the source stack with the new source stack

        # if the source stack now belongs to the opponent, add it to the opponent's cells and remove it from the current player's cells
        if(self.is_player_stack(new_source_stack, self.game_state.get_next_player())):
            self.game_state.remove_from_player_cells(source, self.game_state.get_current_player())
            self.game_state.add_to_player_cells(source, self.game_state.get_next_player())
        elif(self.is_empty_stack(new_source_stack)): # if the source stack is now empty, remove it from the current player's cells
            self.game_state.remove_from_player_cells(source, self.game_state.get_current_player())

        self.handle_stack_size_limit(new_destination_stack, destination_pos) # Call the function that will handle the stack size limit and the change of the destination stack in the board

    # Places a saved piece in the board
    def place_saved_piece(self, cell: tuple, player: 'Player') -> None:
        destination_pos = self.get_bitmap_position(cell[0], cell[1]) # Get the position of the destination stack in the bitmap

        destination_stack = self.get_stack(cell) # Get the destination stack (before the move)
        new_destination_stack = self.add_pieces_to_stack(destination_stack, player.get_color_bits()) # Add the piece to the destination stack
        
        # Add the destination of the moving stack to the current player's cells
        self.game_state.add_to_player_cells(cell, self.game_state.get_current_player())
        # if the destination belonged to the opponent, remove it from the opponent's cells
        if(self.is_player_stack(destination_stack, self.game_state.get_next_player())):
            self.game_state.remove_from_player_cells(cell, self.game_state.get_next_player())

        self.handle_stack_size_limit(new_destination_stack, destination_pos) # Call the function that will handle the stack size limit and the change of the destination stack in the board

    # Makes a move in the board
    def make_move(self, pos: tuple, current_player: 'Player') -> None:
        selected_stack = self.get_stack(self.selected_cell)
        if(not self.is_empty_stack(selected_stack) and self.is_player_stack(selected_stack, current_player)):
            self.transfer_pieces(self.selected_cell, pos)

    # Given a cell, returns if it belongs to a given player
    def is_player_stack(self, stack: int, player: 'Player') -> bool:
        num_pieces = self.get_stack_size(stack)
        if num_pieces == 0: # If the stack is empty, it doesn't belong to the player
            return False
        color = player.get_color_bits()
        stack >>= (num_pieces-1)*2 # Get the top piece of the stack
        return (stack&0b11) == color # Return if the top piece of the stack is the player's color
    
    def get_valid_moves(self, player) -> np.ndarray:
        movable_cells = player.get_cells()
        player.clear_controlled_cells()

        valid_moves = [Move((None, None), cell, True) for cell in self.placeable_cells if player.has_saved_pieces()]

        # Represents moves with board piece
        board_moves = [Move(cell, move) 
               for cell in movable_cells 
               for possible_move in [self.get_possible_moves(cell)] 
               for move in possible_move if possible_move is not None]

        board_moves.sort(key=lambda move: len(self.get_possible_moves(move.get_origin())), reverse=False) # It will search through the ones with less moves first so it might prune extra moves
        valid_moves.extend(board_moves)
        player.update_controlled_cells([move.get_destination() for move in valid_moves])

        return np.array(valid_moves)
    
    def get_valid_unordered_moves(self, player) -> np.ndarray:
        movable_cells = player.get_cells()
        player.clear_controlled_cells()

        valid_moves = [Move((None, None), cell, True) for cell in self.placeable_cells if player.has_saved_pieces()]

        # Represents moves with board piece
        board_moves = [Move(cell, move) 
               for cell in movable_cells 
               for possible_move in [self.get_possible_moves(cell)] 
               for move in possible_move if possible_move is not None]

        valid_moves.extend(board_moves)
        player.update_controlled_cells([move.get_destination() for move in valid_moves])

        return np.array(valid_moves)
    
    def enemy_pieces_in_stack(self, stack: int, player: 'Player') -> int:
        num_pieces = self.get_stack_size(stack)
        enemy_pieces = 0
        for i in range(num_pieces):
            piece = (stack & (0b11 << (i*2))) >> (i*2)
            if piece != player.get_color_bits():
                enemy_pieces += 1
        return enemy_pieces

    def get_enemy_pieces_in_my_control(self, player: 'Player') -> int:
        total = 0
        for cell in player.get_cells():
            stack = self.get_stack(cell)
            total += self.enemy_pieces_in_stack(stack, player)
        return total

    def get_valid_destinations(self, player, movable_cells) -> np.ndarray:
        # Represents moves with board piece
        valid_destinations = [move
            for cell in movable_cells 
            for possible_move in [self.get_possible_moves(tuple(int(num) for num in cell))] 
            for move in possible_move if possible_move is not None]

        # Represents moves with saved pieces
        if player.has_saved_pieces():
            valid_destinations.extend(cell for cell in self.placeable_cells)

        return np.array(valid_destinations)

    def eval_board(self, player: 'Player', opponent: 'Player') -> int:
        total = 0
        opponent_cells = opponent.get_cells()
        player_cells = player.get_cells()
        opponent_destinations = self.get_valid_destinations(opponent, opponent_cells)

        for cell in player_cells:
            stack = self.get_stack(cell)
            total += self.enemy_pieces_in_stack(stack, player) # Enemy pieces in my control
            if cell in opponent_destinations: # If the opponent can move to my cell and take my pieces (bad)
                total -= 5
                if(self.get_stack_size(stack) == self.stack_size): # If the stack is full it's an even worse position
                    total -= 5
                total += 2 * self.get_stack_size(stack)

        player_destinations = self.get_valid_destinations(player, player_cells)

        for cell in opponent_cells:
            stack = self.get_stack(cell)
            total -= self.enemy_pieces_in_stack(stack, opponent)
            if cell in player_destinations: # Pieces that can see each other are bad for the player, because it will be the opponent turn and they can take the pieces
                total += 4
                if(self.get_stack_size(stack) == self.stack_size):
                    total += 4
                total -= 2 * self.get_stack_size(stack)
            
        return total
            