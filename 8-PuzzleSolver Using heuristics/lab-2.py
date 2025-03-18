import copy
import heapdict

class Node:
    def __init__(self, state=None, parent=None, g_n=0, h_n=0, f_n=0):
        # Store the node state and parent state
        self.state = state
        self.parent = parent
        self.g_n = g_n
        self.h_n = h_n
        self.__f_n = f_n

    def __str__(self):
        # Implement a method to print the state of the node
        output = ""
        for i in range(3):
            output += f"{self.state[i]}\n"
        return output

    @property
    def f_n(self):
        self.__f_n = self.g_n + self.h_n
        return self.__f_n

    @f_n.setter
    def f_n(self,val):
        self.__f_n = val

class PuzzleSolver:
    def __init__(self, start, goal):
        # Initialize the puzzle with start and goal state
        self.start = start
        self.goal = goal
        dic = dict()
        for x in range(3):
            for y in range(3):
                dic[self.goal.state[x][y]] = (x,y)
        self.map = dic

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
        n_state = copy.deepcopy(state.state)
        n_node = Node(n_state,state,state.g_n + 1)
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

    def hamming_distance(self,state):
        goal = self.goal.state
        h_n = 0
        for i in range(3):
            for j in range(3):
                if state.state[i][j] != goal[i][j]:
                    h_n += 1
        state.h_n = h_n
        return h_n

    def manhattan_distance(self,state):
        h_n = 0
        for x in range(3):
            for y in range(3):
                g_x,g_y = self.map[state.state[x][y]]
                h_n += abs(g_x - x) + abs(g_y - y)
        state.h_n = h_n
        return h_n

    def best_fit_search_hamming(self):
        # Implement the search strategy for best-fit-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = heapdict.heapdict()
        open_list[self.start] = self.hamming_distance(self.start)
        open_state = set(str(self.start.state))
        closed_list = set()
        n = 0
        # Your code goes here
        while open_list:
            n += 1
            state,i = open_list.popitem()
            open_state.discard(str(state.state))
            print(f"{state}{n},{i}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    open_list[child] = self.hamming_distance(child)
                    open_state.add(child_state_str)
        print("No Solution Found.")
        return

    def best_fit_search_manhattan(self):
        # Implement the search strategy for best-fit-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = heapdict.heapdict()
        open_list[self.start] = self.manhattan_distance(self.start)
        open_state = set(str(self.start.state))
        closed_list = set()
        n = 0
        # Your code goes here
        while open_list:
            n += 1
            state,i = open_list.popitem()
            open_state.discard(str(state.state))
            print(f"{state}{n},{i}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    open_list[child] = self.manhattan_distance(child)
                    open_state.add(child_state_str)
        print("No Solution Found")
        return

    def A_algorithm_hamming(self):
        # Implement the search strategy for best-fit-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = heapdict.heapdict()
        self.hamming_distance(self.start)
        open_list[self.start] = self.start.f_n
        open_state = set(str(self.start.state))
        closed_list = set()
        n = 0
        # Your code goes here
        while open_list:
            n += 1
            state,i = open_list.popitem()
            open_state.discard(str(state.state))
            print(f"{state}{n},{i}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    self.hamming_distance(child)
                    open_list[child] = child.f_n
                    open_state.add(child_state_str)
        print("No Solution Found")
        return

    def A_algorithm_manhattan(self):
        # Implement the search strategy for best-fit-search

        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return

        goal = self.goal.state
        open_list = heapdict.heapdict()
        self.manhattan_distance(self.start)
        open_list[self.start] = self.start.f_n
        open_state = set(str(self.start.state))
        closed_list = set()
        n = 0
        # Your code goes here
        while open_list:
            n += 1
            state,i = open_list.popitem()
            open_state.discard(str(state.state))
            print(f"{state}{n},{i}")
            if state.state == goal:
                self.disp_solution(state)
                return
            closed_list.add(str(state.state))
            children = self.generate_children(state)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in closed_list and child_state_str not in open_state:
                    self.manhattan_distance(child)
                    open_list[child] = child.f_n
                    open_state.add(child_state_str)
        print("No Solution Found")
        return

    def disp_solution(self, final_state):
        # Implement the method to display the solution path
        print("||||||||||Goal State:||||||||||")
        steps = final_state.g_n
        while final_state != None:
            print(f"{final_state}{final_state.g_n}")
            final_state = final_state.parent
        print(f"Initial State\n{steps =}")
        return

#Run this Test-Case

def main ():
    start = Node([[4, 7, 8], [3, 6, 5], [1, 2, ' ']])
    goal = Node([[1, 2, 3], [4, 5, 6], [7, 8, ' ']])
    print(f"Start State: \n{start}{start.g_n} {start.h_n} {start.f_n}")
    print(f"Goal State: \n{goal}{start.g_n} {start.h_n} {start.f_n}")
    solver = PuzzleSolver(start,goal)
#     children = solver.generate_children(start)
#     for child in children:
#         solver.hamming_distance(child)
#         print(f"{child}{child.g_n} {child.h_n} {child.f_n}")
#     solver.best_fit_search_hamming()
#     solver.best_fit_search_manhattan()
#     solver.A_algorithm_hamming()
#     solver.A_algorithm_manhattan()
main()
