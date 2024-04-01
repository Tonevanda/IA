import math
import random
import heapq

class Node:
    def __init__(self, state, parent=None) -> None:
        self.state = state
        self.parent = parent
        self.children = []      # This is a heap so we can get the child with the highest UCB score in O(1)
        self.num_children = 0
        self.untried_moves = state.get_current_player().get_cells()
        self.visits = 0
        self.value = 0
        self.hash = hash(state)

    # Used for the heap comparisons
    def __lt__(self, other) -> bool:
        return self.ucb_score() < other.ucb_score()
    
    def is_fully_expanded(self) -> bool:
        return self.num_children == len(self.untried_moves)
    
    def is_terminal(self) -> bool:
        return self.state.verify_win()

    def add_child(self, child_state) -> 'Node':
        child = Node(child_state, parent=self)
        heapq.heappush(self.children, (-child.ucb_score(), child))

        self.num_children += 1
        return child
    
    # TODO: May need to change the weight
    def ucb_score(self, scale=1 / math.sqrt(2)) -> float:
        if self.visits == 0:
            return float('inf')
        else:
            return (self.value / self.visits) + scale * math.sqrt(2 * math.log(self.parent.visits) / self.visits)
    
    def select_child(self) -> 'Node':
        _, child = heapq.heappop(self.children)
        heapq.heappush(self.children, (-child.ucb_score(), child))
        return child
    
    def update(self, value) -> None:
        self.value += value
        self.visits += 1
        if self.parent:
            self.parent.update(value)
    
class MCTS:
    def __init__(self, state) -> None:
        self.root = Node(state)
        self.transposition_table = {self.root.hash: self.root}

    def select_node_to_expand(self) -> Node:
        current = self.root
        while not current.is_terminal() and current.is_fully_expanded():
            current = current.select_child()
            if current.hash in self.transposition_table:
                current = self.transposition_table[current.hash]
        return current
    
    def expand(self, node) -> Node:
        legal_moves = node.state.board.get_valid_unordered_moves(node.state.get_current_player())
        tried_moves = {child[1].state.get_last_move() for child in node.children}
        #print("Tried moves: ", tried_moves)
        untried_moves = [move for move in legal_moves if move not in tried_moves]
        #print("Untried moves: ", untried_moves)
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

            new_child = node.add_child(new_state)
            self.transposition_table[new_child.hash] = new_child
            return new_child
        else:
            return random.choice(node.children)

    def simulate(self, node) -> int:
        #state = node.state.copy()
        last_move = node.state.get_last_move()
        while not node.state.verify_win():
            current_player = node.state.get_current_player()
            valid_moves = node.state.board.get_valid_moves(current_player)
            move = random.choice(valid_moves)
            #move = self.get_good_move(state, valid_moves)
            if(move.is_from_personal_stack()):
                node.state.select_saved_player_stack(current_player)
                node.state.place_saved_piece(move.get_destination(), current_player)
            else:
                node.state.select_cell(move.get_origin())
                node.state.make_move(move.get_destination())
            node.state.unselect_cell()

            if(node.state.verify_win()):
                break
            node.state.next_turn()

        # If the state is terminal, return who won
        node.state.last_move = last_move
        return 1 if node.state.get_current_player() == self.root.state.get_current_player() else -1
    
    def backpropagate(self, node, value) -> None:
        while node is not None:
            node.update(value)
            node = node.parent
    
    def search(self, num_iterations) -> Node:
        for _ in range(num_iterations):
            node = self.select_node_to_expand()
            leaf = self.expand(node)
            simulation_result = self.simulate(leaf)
            self.backpropagate(leaf, simulation_result)

        best_node = heapq.nlargest(1, self.root.children, key=lambda child: child[1].value / child[1].visits)[0][1]

        best_node_parent = best_node.parent

        print("Is root:" , best_node_parent == self.root)
        
        return best_node