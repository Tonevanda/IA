from config import PIECE_BLUE, PIECE_ORANGE, PIECE_EMPTY, PIECE_NONE, STACK_MASK
import numpy as np

class Board:
    def __init__(self, game_state, size):
        self.game_state = game_state
        self.size = size
        self.board = 0b0
        self.make_board()
        
        self.selected_cell = None
        self.current_possible_moves = None
    
    def get_board(self):
        return self.board

    def get_size(self):
        return self.size
    
    def get_total_cells(self):
        return self.size * self.size

    # Checks if the cell is on the edge of the board
    def is_on_edge(self, row, col):
        return row == 0 or row == self.size-1 or col == 0 or col == self.size-1
    
    def make_piece(self, color):
        self.board <<= 2
        self.board |= color

    def make_stack(self, color):
        self.make_piece(PIECE_EMPTY)
        self.make_piece(PIECE_EMPTY)
        self.make_piece(PIECE_EMPTY)
        self.make_piece(PIECE_EMPTY)
        self.make_piece(color)

    def make_board(self):
        column_counter = 0
        row_counter = 0
        current_color = PIECE_ORANGE
        first = True

        for row in range(self.size):
            for col in range(self.size):
                if not self.is_on_edge(row, col):
                    self.make_stack(current_color)
                    column_counter += 1
                    if column_counter % 2 == 0:
                        current_color = PIECE_BLUE if current_color == PIECE_ORANGE else PIECE_ORANGE
                else:
                    if(first):
                        self.board |= PIECE_EMPTY
                        self.make_piece(PIECE_EMPTY)
                        self.make_piece(PIECE_EMPTY)
                        self.make_piece(PIECE_EMPTY)
                        self.make_piece(PIECE_EMPTY)
                        first = False
                    else:
                        self.make_stack(PIECE_EMPTY)

            row_counter += 1
            if row_counter % 2 == 0:
                current_color = PIECE_BLUE
            else:
                current_color = PIECE_ORANGE

        self.make_hexagon()

    def substitute_stack(self, stack_position, new_stack):
        self.board &= ~(STACK_MASK << (stack_position * 10))
        self.board |= (new_stack << (stack_position * 10))

    def get_bitmap_position(self, row, col):
        return row * self.size + col

    def is_outside_board(self, cell):
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

    def make_hexagon(self):
        
        none_stack = STACK_MASK

        for i in range(self.size):
            for j in range(self.size):
                bitmap_position = self.get_bitmap_position(i, j)
                if(self.is_outside_board((i,j))):
                    self.substitute_stack(bitmap_position, none_stack)

    # Takes a position and returns the stack at that position
    def get_stack(self, cell):
        row, col = cell
        bitmap_pos = self.get_bitmap_position(row, col)
        return (self.board >> (bitmap_pos * 10)) & STACK_MASK

    def is_none_stack(self, stack):
        return stack == STACK_MASK
    
    def is_empty_stack(self, stack):
        return (stack ^ STACK_MASK) == STACK_MASK

    def get_selected_cell(self):
        return self.selected_cell

    def get_selected_stack(self):
        if self.selected_cell is not None:
            return self.get_stack(self.selected_cell)
        return None
    
    def get_stack_size(self, stack):
        return bin(stack).count("1")
    
    # Takes a cell and returns a list of possible moves in the corresponding cell
    def get_possible_moves(self, cell):
        x,y = cell
        stack = self.get_stack(cell)
        max_move = self.get_stack_size(stack)

        if max_move > 0:
            moves = []
            for distance in range(1, max_move + 1):
                if 0 <= x - distance < self.size:
                    if(not self.is_outside_board((x - distance, y))):
                        moves.append((x - distance, y))
                if(0 <= x + distance < self.size):
                    if(not self.is_outside_board((x + distance, y))):
                        moves.append((x + distance, y))
                if(0 <= y - distance < self.size):
                    if(not self.is_outside_board((x, y - distance))):
                        moves.append((x, y - distance))
                if(0 <= y + distance < self.size):
                    if(not self.is_outside_board((x, y + distance))):
                        moves.append((x, y + distance))
            return moves
        return None

    def remove_from_stack(self, stack, num_pieces):
        stack_pieces = self.get_stack_size(stack)-1
        for i in range(num_pieces):
            stack &= ~(0b11 << ((stack_pieces-i) * 2))
        return stack & STACK_MASK

    def get_removed_from_stack(self, stack, num_pieces):
        removed = 0b0
        stack_pieces = self.get_stack_size(stack)-1
        for i in range(num_pieces):
            piece_removed = (stack & (0b11 << ((stack_pieces-i)*2))) >> ((stack_pieces-i)*2)
            removed <<= 2
            removed |= piece_removed
            stack &= ~(0b11 << ((stack_pieces-i)*2)) 
        return removed
        
    def add_pieces_to_stack(self, stack, removed_stack):
        shift = self.get_stack_size(stack) * 2
        removed_stack <<= shift
        stack |= removed_stack
        return stack
    
    def get_distance_between_cells(self, source, destination):
        return abs(destination[0] - source[0]) + abs(destination[1] - source[1])

    def handle_removed_pieces(self, removed_pieces):
        amount = self.get_stack_size(removed_pieces)
        for i in range(amount):
            piece = removed_pieces & (0b11 << (i*2))
            if piece == self.game_state.get_current_player().get_color_bits():
                self.game_state.add_to_player_stack()

    def handle_stack_size_limit(self, stack, bitmap_position):
        if(self.get_stack_size(stack) > 5):
            overflow = self.get_stack_size(stack) - 5
            rest = stack & ~(STACK_MASK << overflow*2)
            stack = (stack & (STACK_MASK << overflow*2)) >> (overflow*2)
            self.handle_removed_pieces(rest)
        self.substitute_stack(bitmap_position, stack)
        

    def transfer_pieces(self, source, destination):
        source_pos = self.get_bitmap_position(source[0], source[1])
        destination_pos = self.get_bitmap_position(destination[0], destination[1])
        distance = self.get_distance_between_cells(source, destination)

        source_stack = self.get_stack(source)
        destination_stack = self.get_stack(destination)

        new_source_stack = self.remove_from_stack(source_stack, distance)
        removed_stack = self.get_removed_from_stack(source_stack, distance)
        new_destination_stack = self.add_pieces_to_stack(destination_stack, removed_stack)

        self.substitute_stack(source_pos, new_source_stack)
        self.handle_stack_size_limit(new_destination_stack, destination_pos)

    def place_saved_piece(self, cell, player):
        destination_pos = self.get_bitmap_position(cell[0], cell[1])
        print("place saved piece")

        destination_stack = self.get_stack(cell)
        new_destination_stack = self.add_pieces_to_stack(destination_stack, player.get_color_bits())
        
        self.handle_stack_size_limit(new_destination_stack, destination_pos)

    def make_move(self, pos, current_player):
        selected_stack = self.get_stack(self.selected_cell)
        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        if(not self.is_empty_stack(selected_stack) and self.is_player_stack(self.selected_cell, current_player)):
            self.transfer_pieces(self.selected_cell, pos)

    # Given a cell, returns if it belongs to a given player
    def is_player_stack(self, cell, player):
        stack = self.get_stack(cell)
        color = player.get_color_bits()
        num_pieces = self.get_stack_size(stack)
        if num_pieces == 0:
            return False
        stack >>= (num_pieces-1)*2
        return (stack&0b11) == color

    # Checks if the board has any pieces of a given player
    # TODO: before this, make "winnable move function" that verifies if the last move was a capture and didn't reveal a new opponent piece
    # TODO: Do this also with bit operations
    def verify_lost(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if self.is_player_stack((i, j), player):
                    return False
        return True