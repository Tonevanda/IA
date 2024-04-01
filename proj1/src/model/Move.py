class Move:
    def __init__(self, piece: tuple, destination: tuple, from_personal_stack: bool = False) -> None:
        self.piece = piece # Origin of the move
        self.destination = destination # Destination of the move
        self.from_personal_stack = from_personal_stack # If the move is from the personal stack

    # Returns the origin of the move
    def get_origin(self) -> tuple:
        return self.piece
    
    # Returns the destination of the move
    def get_destination(self) -> tuple:
        return self.destination
    
    # Returns if the move is from the personal stack
    def is_from_personal_stack(self) -> bool:
        return self.from_personal_stack

    # String representation of the move
    def __str__(self) -> str:
        return f"({self.piece}, {self.destination}, {self.from_personal_stack})"
    
    __repr__ = __str__