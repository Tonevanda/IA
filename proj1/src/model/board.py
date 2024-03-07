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

    def make_hexagon(self):
        cut = int(self.size * 0.25)
        none_stack = STACK_MASK

        for i in range(self.size):
            for j in range(self.size):
                bitmap_position = self.get_bitmap_position(i, j)
                if i < cut and j < cut - i:
                    self.substitute_stack(bitmap_position, none_stack)
                elif i < cut and j > self.size - (cut - i) - 1:
                    self.substitute_stack(bitmap_position, none_stack)
                elif i >= self.size - cut and j < cut - (self.size - i - 1):
                    self.substitute_stack(bitmap_position, none_stack)
                elif i >= self.size - cut and j > self.size - (cut - (self.size - i - 1)) - 1:
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
    # TODO: Better way using bit operations?
    def possible_moves(self, cell):
        x, y = cell
        #you can only move as many pieces as the height of the stack
        stack = self.get_stack(cell)
        if stack is not None:
            max=self.get_stack_size(stack)
            # i and j are the offsets from the current position. They vary between -max and max+1
            # the condition 0<=x+i<self.size and 0<=y+j<self.size ensures that the move is within the board
            # the condition abs(j)<=max-abs(i) ensures that that diagonal moves aren't used (because they can't)
            # the condition self.board[y+j][x+i] != None ensures that the move is inside the hexagon
            return [(x+i,y+j) for i in range(-max,max+1) for j in range(-max,max+1) if (i,j)!=(0,0) and 0<=x+i<self.size and 0<=y+j<self.size and abs(j)<=max-abs(i) and not self.is_none_stack(self.get_stack((y+j, x+i)))]

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
        source_pos = self.get_bitmap_position(source[1], source[0])
        destination_pos = self.get_bitmap_position(destination[1], destination[0])
        distance = self.get_distance_between_cells(source, destination)

        source_stack = self.get_stack((source[1], source[0]))
        destination_stack = self.get_stack((destination[1], destination[0]))

        new_source_stack = self.remove_from_stack(source_stack, distance)
        removed_stack = self.get_removed_from_stack(source_stack, distance)
        new_destination_stack = self.add_pieces_to_stack(destination_stack, removed_stack)

        self.substitute_stack(source_pos, new_source_stack)
        self.handle_stack_size_limit(new_destination_stack, destination_pos)
        self.verify_end()


    def make_move(self, pos, board):
        x, y = pos
        xs, ys = self.selected_cell
        current_player = self.game_state.get_current_player()
        selected_stack = self.get_stack(self.selected_cell)

        if (self.selected_cell == (0,0)): # Selected from own stack
            self.board[y][x].append(current_player)
            self.game_state.remove_from_player_stack()
            self.stack_handling(board, x, y)

        #if the move is valid, the pieces are moved and the turn changes
        #the move is valid if the stack at the current position is not empty, the top piece is the current player's color, and the destination is in the list of possible moves
        elif(not self.is_empty_stack(selected_stack), self.is_player_piece(self.selected_cell, current_player), pos in self.current_possible_moves):
            self.transfer_pieces(self.selected_cell, pos)

        """elif(board.board[ys][xs]!= [] and board.board[ys][xs][-1]==self.game_state.get_current_player().get_color() and pos in self.current_possible_moves):
            board.board[y][x].extend(board.board[ys][xs])
            board.board[ys][xs] = []
            self.stack_handling(board, x, y)"""

    def verify_end(self):
        if(not self.game_state.did_win()):
            self.game_state.next_turn()  

    # Given a cell, returns if it belongs to a given player
    def is_player_piece(self, cell, player):
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
                if self.is_player_piece((i, j), player):
                    return False
        return True