import heapq
import time
import timeit
from memory_profiler import profile

class PriorityQueue:
    def __init__(self):
        self.__q = []
        heapq.heapify(self.__q)

    def __str__(self):
        output = "Heap Start:\n"
        for node in self.__q:
            output += f"{node}\n"
        return output

    def enqueue(self, x):
        heapq.heappush(self.__q,x)
        return

    def dequeue(self):
        node = heapq.heappop(self.__q)
        return node

    def is_empty(self):
        if len(self.__q) == 0:
            return True
        return False


class Node:
    def __init__(self, state, parent=None, h_n=0):
        self.state = state
        self.parent = parent
        #self.h = ?
        self.h_n = h_n

    def __str__ (self):
        output = ""
        for i in range(3):
            output += f"{self.state[i]}\n"
        return output

    def __lt__ (self, other):
        if self.h_n <= other.h_n:
            return True
        return False

    def hamming_heuristic(self, goal):
        h_n = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != goal[i][j]:
                    h_n += 1
        self.h_n = h_n
        return h_n

    def manhattan_heuristic(self,goal_map):
        h_n = 0
        for x in range(3):
            for y in range(3):
                g_x,g_y = goal_map[self.state[x][y]]
                h_n += abs(g_x - x) + abs(g_y - y)
        self.h_n = h_n
        return h_n

class PuzzleSolver:
    def __init__(self, start, goal):
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
        return inversions % 2 == 0

    def find_space(self, state):
        for x in range(3):
            for y in range(3):
                if state[x][y] == ' ':
                    space = (x,y)
                    break;
        return space

    def find_moves(self, pos):
        x, y = pos
        moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return moves

    def find_children(self, state):
        children = []
        space = self.find_space(state.state)
        moves = self.find_moves(space)
        for move in moves:
            if self.is_valid(move):
                child = self.play_move(state,move,space)
                children.append(child)
        return children

    def is_valid(self, move):
        x, y = move
        if x < 0 or x > 2:
           return False
        elif y < 0 or y > 2:
            return False
        else:
            return True

    def play_move(self, state, move, space):
        n_state = [row[:] for row in state.state]
        n_node = Node(n_state,state)
        x, y = move
        space_x, space_y = space
        tile = n_node.state[x][y]
        n_node.state[x][y] = n_node.state[space_x][space_y]
        n_node.state[space_x][space_y] = tile
        return n_node

    @profile
    def best_first_search_hamming(self):
        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return
        goal = self.goal.state
        pq = PriorityQueue()
        self.start.hamming_heuristic(goal)
        pq.enqueue(self.start)
        pq_state = set(str(self.start.state))
        explored = set()
        n = 0
        while not pq.is_empty():
            ###YOUR CODE GOES HERE###
            n += 1
            node = pq.dequeue()
            pq_state.discard(str(node.state))
            print(f"{node}{n}")
            if node.state == goal:
                self.print_solution(node)
                return
            explored.add(str(node.state))
            children = self.find_children(node)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in explored and child_state_str not in pq_state:
                    child.hamming_heuristic(goal)
                    pq.enqueue(child)
                    pq_state.add(str(child.state))
        print("No Solution Found.")
        return

    @profile
    def best_first_search_manhattan(self):
        if not self.is_solvable(self.start.state):
            print("State unsolvable.")
            return
        goal = self.goal.state
        pq = PriorityQueue()
        self.start.manhattan_heuristic(self.map)
        pq.enqueue(self.start)
        pq_state = set(str(self.start.state))
        explored = set()
        n = 0
        while not pq.is_empty():
            ###YOUR CODE GOES HERE###
            n += 1
            node = pq.dequeue()
            pq_state.discard(str(node.state))
            print(f"{node}{n}")
            if node.state == goal:
                self.print_solution(node)
                return
            explored.add(str(node.state))
            children = self.find_children(node)
            for child in children:
                child_state_str = str(child.state)
                if child_state_str not in explored and child_state_str not in pq_state:
                    child.manhattan_heuristic(self.map)
                    pq.enqueue(child)
                    pq_state.add(str(child.state))
        print("No Solution Found.")
        return

    def print_solution(self, node):
        print("||||||||||Goal State:||||||||||")
        steps = -1
        while node != None:
            steps += 1
            print(f"{node}{node.h_n}")
            node = node.parent
        print(f"Initial State\n{steps = }")
        return

def main():
    start = Node([[4, 7, 8], [3, 6, 5], [1, 2, ' ']])
    goal = Node([[1, 2, 3], [4, 5, 6], [7, 8, ' ']])
    print(f"Start State: \n{start} {start.h_n}")
    print(f"Goal State: \n{goal} {start.h_n}")
    solver = PuzzleSolver(start,goal)

#     Measure time for Best_First_Search_hamming
#     hamming_time = timeit.timeit(lambda: solver.best_first_search_hamming(), number=1)
#     print(f"\nExecution time for Best_first_search with Hamming heuristic: {hamming_time:.6f} seconds")

#     Measure time for Best_First_Search_manhattan
#     manhattan_time = timeit.timeit(lambda: solver.best_first_search_manhattan(), number=1)
#     print(f"Execution time for Best_first_search with Manhattan heuristic: {manhattan_time:.6f} seconds")

#     start_time = time.time()
#     solver.best_first_search_hamming()
#     end_time = time.time()
#     hamming_time = end_time - start_time
#     print(f"\nExecution time for Best_first_search with Hamming heuristic: {hamming_time:.6f} seconds")

#     start_time = time.time()
#     solver.best_first_search_manhattan()
#     end_time = time.time()
#     manhattan_time = end_time - start_time
#     print(f"\nExecution time for Best_first_search with Manhattan heuristic: {manhattan_time:.6f} seconds")

main()
