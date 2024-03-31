from config import PIECE_BLUE, PIECE_ORANGE
from model.Move import Move
import numpy as np

class Player:
    def __init__(self, color, player_type):
        self.color = color
        self.stack_pieces = 0
        self.player_type = player_type
        self.stack_selected = False
        self.cells = set()
        self.controlled_cells = set()
        self.hint = None
        self.total_pieces = 0

    # Get the cells that the player has pieces on
    def get_cells(self) -> set:
        return self.cells
    
    # Get the cells that the player has pieces on as a list of tuples
    def get_tuple_cells(self) -> list[tuple[int, int]]:
        return [(tuple(int(num) for num in cell)) for cell in self.cells]
    
    # Add a cell to the player's cells
    def add_cell(self, cell: tuple) -> None:
        self.cells.add(cell)  # Add the cell to the player's cells

    def remove_cell(self, cell: tuple) -> None:
        self.cells.discard(cell)  # Remove the cell from the player's cells using the discard method

    def get_controlled_cells(self) -> set:
        return self.controlled_cells
    
    def add_controlled_cell(self, cell: tuple) -> None:
        self.controlled_cells.add(cell)

    def update_controlled_cells(self, cells) -> None:
        self.controlled_cells = set(cells)

    def clear_controlled_cells(self) -> None:
        self.controlled_cells.clear()

    # Get the player type
    def get_player_type(self) -> str:
        return self.player_type
    
    # Get the player's color
    def get_color(self) -> str:
        return self.color
    
    # Get the player's color as it's bit representation
    def get_color_bits(self) -> int:
        return PIECE_ORANGE if self.color == 'Orange' else PIECE_BLUE

    # Get the amount of pieces the player has in their saved stack
    def get_stack_count(self) -> int:
        return self.stack_pieces
    
    # Check if the player has any pieces in their saved stack
    def has_saved_pieces(self) -> bool:
        return self.stack_pieces > 0
    
    # Add a piece to the player's saved stack
    def add_stack_piece(self) -> None:
        self.stack_pieces += 1

    # Remove a piece from the player's saved stack
    def remove_stack_piece(self) -> None:
        self.stack_pieces -= 1

    # Selects the player's saved piece's stack
    def select_stack(self) -> None:
        self.stack_selected = True
    
    # Unselects the player's saved piece's stack
    def unselect_stack(self) -> None:
        self.stack_selected = False

    # Check if the player's a bot
    def is_bot(self) -> bool:
        return self.player_type == 'Easy Bot' or self.player_type == 'Hard Bot' or self.player_type == 'Medium Bot' or self.player_type == 'MCTS Bot'

    # Check if the player's an easy bot
    def is_easy_bot(self) -> bool:
        return self.player_type == 'Easy Bot'

    # Check if the player's a medium bot
    def is_medium_bot(self) -> bool:
        return self.player_type == 'Medium Bot'
    
    # Check if the player's a hard bot
    def is_hard_bot(self) -> bool:
        return self.player_type == 'Hard Bot'
    
    def is_mcts_bot(self) -> bool:
        return self.player_type == 'MCTS Bot'
    
    def get_hint(self) -> 'Move':
        return self.hint
    
    def set_hint(self, hint: 'Move') -> None:
        self.hint = hint

    def clear_hint(self) -> None:
        self.hint = None

    def get_total_pieces(self) -> int:
        return self.total_pieces
    
    def add_piece(self) -> None:
        self.total_pieces += 1
    
    def remove_piece(self) -> None:
        self.total_pieces -= 1

    # Defines the string representation of the player when printed
    def __str__(self) -> str:
        return self.color + ' ' + self.player_type
    
    def __repr__(self) -> str:
        return self.color + ' stack: ' + str(self.stack_pieces)