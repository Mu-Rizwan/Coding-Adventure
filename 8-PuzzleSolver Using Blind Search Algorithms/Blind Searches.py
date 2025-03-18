import time
import timeit
from memory_profiler import profile


class Node:
    def __init__(self, state=None, parent=None):
        # Store the node state and parent state
        self.state = state
        self.parent = parent

    def __str__(self):
        # Implement a method to print the state of the node
        output = ""
        for i in range(3):
            output += f"{self.state[i]}\n"
        return output

class PuzzleSolver:
    def __init__(self, start, goal):
        # Initialize the puzzle with start and goal state
        self.start = start
        self.goal = goal

    def is_solvable (self, state):
        # Check if the puzzle state is solvable
        inversions = 0
        flatten_state = [x for sublist in state for x in sublist if x != ' ']
        for i in range(7):
            for j in range(i+1,8):
                if flatten_state[i] > flatten_state[j]:
                   inversions += 1
        if inversions%2 == 0:
            return True
        else:
            return False

    def find_space(self, state):
        # Implement the method to find the position (x, y) of the empty space (' ')
        for x in range(3):
            for y in range(3):
                if state[x][y] == ' ':
                    space = (x,y)
                    break;
        return space

    def find_moves(self, pos):
        # Implement the method to generate valid moves for the empty space
        x, y = pos
        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return moves

    def is_valid(self, move):
        # Implement the method to check if a move is within bounds of the puzzle
        x, y = move
        if x < 0 or x > 2:
           return False
        elif y < 0 or y > 2:
            return False
        else:
            return True

    def play_move(self, state, move, space):
        # Implement the method to generate a new state after making the move
        n_state = [row[:] for row in state.state]
        n_node = Node(n_state,state)
        x, y = move
        space_x, space_y = space
        tile = n_node.state[x][y]
        n_node.state[x][y] = n_node.state[space_x][space_y]
        n_node.state[space_x][space_y] = tile
        return n_node

    def generate_children(self, state):
        # Implement the method to generate all valid children from a state
        children = []
        space = self.find_space(state.state)
        moves = self.find_moves(space)

        for move in moves:
            if self.is_valid(move):
                child = self.play_move(state,move,space)
                children.append(child)
        return children

    @profile
    def solve_puzzle_backtracking(self):
        # Implement the search strategy for simple backtracking
        def backtrack(node):
            state_list = [node]
            new_state_list = [node]
            new_state_str = set(str(node.state))
            dead_list = set()
            #current_state = ??
            cs = node
            goal = self.goal.state
            # Your code goes here
            n = 0
            while new_state_list:
                n += 1
                print(f"{cs}{n}")
                if cs.state == goal:
                    return cs
                children = []
                for child in self.generate_children(cs):
                    child_state_str = str(child.state)
                    if child_state_str not in dead_list and child_state_str not in new_state_str:
                        children.append(child)
                if not children:
                    while state_list and cs.state == state_list[-1].state:
                        dead_list.add(str(cs.state))
                        dead = new_state_list.pop()
                        new_state_str.discard(str(dead.state))
                        state_list.pop()
                        if new_state_list:
                            cs = new_state_list[-1]
                        else:
                            Print("No Solution Found.")
                            return
                    state_list.append(cs)
                else:
                    new_state_list.extend(children)
                    for child in children:
                        new_state_str.add(str(child.state))
                    cs = new_state_list[-1]
                    state_list.append(cs)
            print("No Solution Found.")
            return

        final_state = backtrack(self.start)
        # Call disp_solution method
        self.disp_solution(final_state)
        return

    @profile
    def solve_puzzle_dfs(self):
        # Implement the search strategy for simple depth-first-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = [self.start]
        open_state = set(str(self.start.state))
        closed_list = set()
        # Your code goes here
        n = 0
        while open_list:
            n += 1
            state = open_list.pop()
            open_state.discard(str(state.state))
            print(f"{state}{n}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    open_list.append(child)
                    open_state.add(child_state_str)

        print("No Solution Found.")
        return

    @profile
    def solve_puzzle_bfs(self):
        # Implement the search strategy for breadth-first-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = [self.start]
        open_state = set(str(self.start.state))
        closed_list = set()
        n = 0
        # Your code goes here
        while open_list:
            n += 1
            state = open_list.pop(0)
            open_state.discard(str(state.state))
            print(f"{state}{n}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    open_list.append(child)
                    open_state.add(child_state_str)
        print("No Solution Found.")
        return

    @profile
    def solve_puzzle_dfid(self):
        # Implement the search strategy for depth-first-search with iterative deepening

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return
        goal = self.goal.state
        def dls (node, depth, closed_list, open_list):
            # Your code goes here
            open_list.discard(str(node.state))
            nonlocal n
            n += 1
            print(f"{node}{n}")
            if node.state == goal:
                self.disp_solution(node)
                return True
            if depth == 0:
                return
            closed_list.add(str(node.state))
            children = self.generate_children(node)
            for child in children:
                str_child_state = str(child.state)
                if str_child_state not in closed_list and str_child_state not in open_list:
                    open_list.add(str_child_state)
                    if dls(child,depth-1,closed_list,open_list):
                        return True
            closed_list.remove(str(node.state))
            return False

        # Call dls function iteratively and search
        for i in range(18,0,-1):
            n =0
            open_list = set(str(self.start))
            closed_list = set()
            if dls(self.start, i, closed_list, open_list):
               return

        print("No Solution Found.")
        return

    def disp_solution(self, final_state):
        # Implement the method to display the solution path
        print("|||||Goal State:|||||")
        steps = -1
        while final_state != None:
            steps += 1
            print(final_state)
            final_state = final_state.parent
        print(f"Initial State\n{steps = }")
        return

#Run this Test-Case

def main ():
    start = Node([[' ', 1, 3], [2, 6, 8], [4, 5, 7]])
    goal = Node([[1, 2, 3], [4, 5, 6], [7, 8, ' ']])
    print(f"Start State: \n{start}")
    print(f"Goal State: \n{goal}")
    solver = PuzzleSolver(start,goal)

#     Measure time for Backtracking Algorithm
#     Backtracking_time = timeit.timeit(lambda: solver.solve_puzzle_backtracking(), number=1)
#     print(f"\nExecution time for Backtracking Algorithm: {Backtracking_time:.6f} seconds")

#     Measure time for DFS
#     DFS_time = timeit.timeit(lambda: solver.solve_puzzle_dfs(), number=1)
#     print(f"Execution time for DFS: {DFS_time:.6f} seconds")

#     Measure time for BFS
#     BFS_time = timeit.timeit(lambda: solver.solve_puzzle_bfs(), number=1)
#     print(f"\nExecution time for BFS: {BFS_time:.6f} seconds")

#     Measure time for DFID
#     DFID_time = timeit.timeit(lambda: solver.solve_puzzle_dfid(), number=1)
#     print(f"Execution time for DFID: {DFID_time:.6f} seconds")

#     start_time = time.time()
#     solver.solve_puzzle_backtracking()
#     end_time = time.time()
#     Backtracking_time = end_time - start_time
#     print(f"\nExecution time for Backtracking Algorithm: {Backtracking_time:.6f} seconds")

#     start_time = time.time()
#     solver.solve_puzzle_dfs()
#     end_time = time.time()
#     DFS_time = end_time - start_time
#     print(f"\nExecution time for DFS: {DFS_time:.6f} seconds")

#     start_time = time.time()
#     solver.solve_puzzle_bfs()
#     end_time = time.time()
#     BFS_time = end_time - start_time
#     print(f"\nExecution time for BFS: {BFS_time:.6f} seconds")

#     start_time = time.time()
#     solver.solve_puzzle_dfid()
#     end_time = time.time()
#     DFID_time = end_time - start_time
#     print(f"\nExecution time for DFID: {DFID_time:.6f} seconds")

main()
