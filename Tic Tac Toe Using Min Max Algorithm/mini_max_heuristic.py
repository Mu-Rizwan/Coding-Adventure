import math
# Initialize a 3x3 Tic-Tac-Toe board with empty spaces.

nodes_visited = 0
def print_board(board):
    """prints current state of board """
    for row in board:
        print(row)
    print()

def is_winner(board, player):
    """checks the given player has won or not ., return true , false """

    # For Rows
    for x in range(3):
        if board[x][0] == player and board[x][1] == player and board[x][2] == player:
            return True

    # For Columns
    for y in range(3):
        if board[0][y] == player and board[1][y] == player and board[2][y] == player:
            return True

    # Principal Diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    # Secondary Diagonal
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def is_full(board):
    """returns True if the board is full else false"""
    for x in range(3):
        for y in range(3):
            if board[x][y] == ' ':
                return False
    return True

def heuristic(board,player):
    score = 0

    if player == "X":
        opponent = "O"
    else:
        opponent = "X"

    # For Rows
    for x in range(3):
        if board[x][0] == opponent or board[x][1] == opponent or board[x][2] == opponent:
            pass
        else:
            score += 1

    # For Columns
    for y in range(3):
        if board[0][y] == opponent or board[1][y] == opponent and board[2][y] == opponent:
            pass
        else:
            score += 1

    # Principal Diagonal
    if board[0][0] == opponent and board[1][1] == opponent and board[2][2] == opponent:
        pass
    else:
        score += 1

    # Secondary Diagonal
    if board[0][2] == opponent and board[1][1] == opponent and board[2][0] == opponent:
        pass
    else:
        score += 1

    return score


def minimax(board, depth, is_maximizing):
    """ Minimax algorithm to evaluate board positions two option ,set depth level heuristic ,or
    continue till game end ,return best score  """

    global nodes_visited

    if is_winner(board,"X"):
        return math.inf

    if is_winner(board,"O"):
        return -math.inf

    if is_full(board):
        return 0

    if depth <= 0:
        max_score = heuristic(board,"X")
        min_score = heuristic(board,"O")
        return max_score - min_score

    if is_maximizing:
        best_score = -math.inf
    else:
        best_score = math.inf
    for x in range(3):
        for y in range(3):
            if board[x][y] == ' ':
                if is_maximizing:
                    board[x][y] = "X"
                    nodes_visited += 1
                    score = minimax(board,depth-1,False)
                    board[x][y] = ' '
                    if score > best_score:
                        best_score = score
                else:
                    board[x][y] = "O"
                    nodes_visited += 1
                    score = minimax(board,depth-1,True)
                    board[x][y] = ' '
                    if score < best_score:
                        best_score = score
    return best_score

def best_move(board):
    """finds and returns the best move for the AI using the minimax function."""
    global nodes_visited
    # set score negative infinty
    best_score = -math.inf
    move = None
    for x in range(3):
        for y in range(3):
            if board[x][y] == ' ':
                board[x][y] = "X"
                nodes_visited += 1
                score = minimax(board,1,False)
                board[x][y] = " "
                if score > best_score:
                    best_score = score
                    move = (x,y)
    if move:
        board[move[0]][move[1]] = "X"

def main():
    """Main game loop."""
    board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
    ]
    while True:
        # print board
        print_board(board)
        print(nodes_visited)
        # take input , user move
        n = int(input("Enter the index for the move:"))
        while n < 1 or n > 9:
            n = int(input("Invalid Index try again!:"))
        x = (n-1) // 3
        y = (n-1) % 3
        board[x][y] = "O"
        print_board(board)
        # check
        if is_winner(board,"O"):
            print(f"MIN is the Winner.")
            break

        if is_full(board):
            print("The Game Ended in a Draw")
            break
        # ai move by minimax
        best_move(board)
        # check
        if is_winner(board,"X"):
            print_board(board)
            print(f"MAX is the Winner.")
            break
        # again
if __name__ == "__main__":
    main()
