from config import PIECE_BLUE, PIECE_ORANGE
import numpy as np

class Player:
    def __init__(self, color, player_type):
        self.color = color
        self.stack_pieces = 0
        self.player_type = player_type
        self.stack_selected = False
        self.cells = np.empty((0, 2), int)

    # Get the cells that the player has pieces on
    # TODO: Why when calling this, the cells don't work like they should
    def get_cells(self) -> np.ndarray:
        return self.cells
    
    # Get the cells that the player has pieces on as a list of tuples
    def get_tuple_cells(self) -> list[tuple[int, int]]:
        return [(tuple(int(num) for num in cell)) for cell in self.cells]
    
    # Add a cell to the player's cells
    def add_cell(self, cell: tuple) -> None:
        print("Received cell: ", cell)
        cell = np.array(cell)  # Convert cell to a numpy array (i.e. (1,2) -> [1 2])
        print("Converted cell: ", cell)
        if not any(np.array_equal(cell, existing_cell) for existing_cell in self.cells): # If the cell is not already in the player's cells
            self.cells = np.append(self.cells, [cell], axis=0) # Add the cell to the player's cells
            print("Added cell: ", cell)
        print("")

    def remove_cell(self, cell: tuple) -> None:
        cell = np.array(cell) # Convert cell to a numpy array (i.e. (1,2) -> [1 2])
        self.cells = np.array([existing_cell for existing_cell in self.cells if not np.array_equal(cell, existing_cell)]) # Remove the cell from the player's cells
        if(self.cells.size == 0):
            self.cells = np.empty((0, 2), int)

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
        return self.player_type == 'Easy Bot' or self.player_type == 'Hard Bot' or self.player_type == 'Medium Bot'

    # Check if the player's an easy bot
    def is_easy_bot(self) -> bool:
        return self.player_type == 'Easy Bot'

    # Check if the player's a medium bot
    def is_medium_bot(self) -> bool:
        return self.player_type == 'Medium Bot'
    
    # Check if the player's a hard bot
    def is_hard_bot(self) -> bool:
        return self.player_type == 'Hard Bot'

    # Defines the string representation of the player when printed
    def __str__(self) -> str:
        return self.color + ' ' + self.player_type