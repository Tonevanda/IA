import math
import random

class Node:
    def __init__(self, state, parent=None) -> None:
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self) -> bool:
        return len(self.children) == len(self.state.get_current_player().get_tuple_cells())
    
    def is_terminal(self) -> bool:
        return self.state.verify_win()

    def add_child(self, child_state) -> 'Node':
        child = Node(child_state, parent=self)
        self.children.append(child)
        return child
    
    # TODO: May need to change the weight
    def ucb_score(self, scale=1 / math.sqrt(2)) -> float:
        if self.visits == 0:
            return float('inf')
        else:
            return (self.value / self.visits) + scale * math.sqrt(2 * math.log(self.parent.visits) / self.visits)
    
    def select_child(self) -> 'Node':
        return max(self.children, key=lambda child: child.ucb_score())
    
    def update(self, value) -> None:
        self.visits += 1
        self.value += value
        # TODO: May not be needed??
        if self.parent:
            self.parent.update(value)
    
class MCTS:
    def __init__(self, state) -> None:
        self.root = Node(state)

    def select_node_to_expand(self) -> Node:
        current = self.root
        while not current.is_terminal() and current.is_fully_expanded():
            current = current.select_child()
        return current
    
    def expand(self, node) -> None:
        legal_moves = node.state.board.get_valid_unordered_moves(node.state.get_current_player())
        untried_moves = [move for move in legal_moves if move not in [child.state.get_last_move() for child in node.children]]
        if untried_moves:
            move = random.choice(untried_moves)
            new_state = node.state.copy()
            current_player = new_state.get_current_player()
            if(move.is_from_personal_stack()):
                new_state.select_saved_player_stack(current_player)
                new_state.place_saved_piece(move.get_destination(), current_player)
            else:
                new_state.select_cell(move.get_origin())
                new_state.make_move(move.get_destination())
            new_state.unselect_cell()
            return node.add_child(new_state)
        else:
            return random.choice(node.children)

    def simulate(self, node) -> int:
        state = node.state.copy()
        while not state.verify_win():
            current_player = state.get_current_player()
            valid_moves = state.board.get_valid_moves(current_player)
            move = random.choice(valid_moves)
            if(move.is_from_personal_stack()):
                state.select_saved_player_stack(current_player)
                state.place_saved_piece(move.get_destination(), current_player)
            else:
                state.select_cell(move.get_origin())
                state.make_move(move.get_destination())
            state.unselect_cell()

            if(state.verify_win()):
                break
            state.next_turn()

        # If the state is terminal, return who won
        return 1 if state.get_current_player() == self.root.state.get_current_player() else -1
    
    def backpropagate(self, node, value) -> None:
        while node is not None:
            node.update(value)
            node = node.parent
    
    def search(self, num_iterations=1000) -> Node:
        for _ in range(num_iterations):
            node = self.select_node_to_expand()
            leaf = self.expand(node)
            simulation_result = self.simulate(leaf)
            self.backpropagate(leaf, simulation_result)
        return max(self.root.children, key=lambda child: child.value / child.visits)