class Move:
    def __init__(self, piece: tuple, destination: tuple, from_personal_stack: bool = False) -> None:
        self.piece = piece
        self.destination = destination
        self.from_personal_stack = from_personal_stack

    def get_origin(self) -> tuple:
        return self.piece
    
    def get_destination(self) -> tuple:
        return self.destination
    
    def is_from_personal_stack(self) -> bool:
        return self.from_personal_stack

    def __str__(self) -> str:
        return f"({self.piece}, {self.destination}, {self.from_personal_stack})"
    
    __repr__ = __str__