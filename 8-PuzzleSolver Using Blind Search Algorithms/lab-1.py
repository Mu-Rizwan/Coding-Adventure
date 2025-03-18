class Node:
    def __init__(self, state, parent):
        # Store the node state and parent state
        pass
    
    def __str__(self):
        # Implement a method to print the state of the node
        pass

class PuzzleSolver:
    def __init__(self, start, goal):
        # Initialize the puzzle with start and goal state
        pass
    
    def is_solvable (self, state):
        # Check if the puzzle state is solvable
        pass

    def find_space(self, state):
        # Implement the method to find the position (x, y) of the empty space (' ')
        pass

    def find_moves(self, pos):
        # Implement the method to generate valid moves for the empty space
        x, y = pos
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    def is_valid(self, move):
        # Implement the method to check if a move is within bounds of the puzzle
        pass

    def play_move(self, state, move, space):
        # Implement the method to generate a new state after making the move
        pass

    def generate_children(self, state):
        # Implement the method to generate all valid children from a state
        children = []
        # space = call find_space method
        # moves = call find_moves method

        # for move in moves:
        #     if self.is_valid(move):
        #         #child = call play_move method
        #         children.append(child)
        return children

    def solve_puzzle_backtracking(self):
        # Implement the search strategy for simple backtracking
        def backtrack(node):
            state_list = []
            new_state_list = []
            dead_list = []
            #current_state = ??

            # Your code goes here
            pass

        final_state = backtrack(self.start)

        # Call disp_solution method 

    def solve_puzzle_dfs(self):
        # Implement the search strategy for simple depth-first-search
        open_list = []
        closed_list = []

        # Your code goes here

        return
    
    def solve_puzzle_bfs(self):
        # Implement the search strategy for breadth-first-search
        open_list = []
        closed_list = []

        # Your code goes here

        return
    
    def solve_puzzle_dfid(self):
        # Implement the search strategy for depth-first-search with iterative deepening
        def dls (self, node, depth):
            # Your code goes here
            pass
        # Call dls function iteratively and search
        pass

    def disp_solution(self, final_state):
        # Implement the method to display the solution path
        pass

#Run this Test-Case

# def main ():
#     start = Node([[4, 7, 8], [3, 6, 5], [1, 2, ' ']])
#     solver = PuzzleSolver(start=start)
#     solver.solve_puzzle_backtracking()
#     solver.solve_puzzle_dfs()
#     solver.solve_puzzle_bfs()
#     solver.solve_puzzle_dfid()
# main()