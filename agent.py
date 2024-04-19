#!/usr/bin/python3
#  agent.py
#  Nine-Board Tic-Tac-Toe Agent starter code
#  COMP3411/9814 Artificial Intelligence
#  CSE, UNSW

import socket
import sys
import numpy as np

# a board cell can hold:
#   0 - Empty
#   1 - I played here X
#   2 - They played here O

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
s = [".","X","O"]
curr = 0 # this is the current board to play in
maxDepth = 4
num_move = 0



# This is just ported from game.c
def print_boards_row(boards, a, b, c, i, j, k):
    print(" "+s[boards[a][i]]+" "+s[boards[a][j]]+" "+s[boards[a][k]]+" | " \
             +s[boards[b][i]]+" "+s[boards[b][j]]+" "+s[boards[b][k]]+" | " \
             +s[boards[c][i]]+" "+s[boards[c][j]]+" "+s[boards[c][k]])

# Print the entire board
# This is just ported from game.c
def print_boards(boards):
    print_boards_row(boards, 1,2,3,1,2,3)
    print_boards_row(boards, 1,2,3,4,5,6)
    print_boards_row(boards, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_boards_row(boards, 4,5,6,1,2,3)
    print_boards_row(boards, 4,5,6,4,5,6)
    print_boards_row(boards, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_boards_row(boards, 7,8,9,1,2,3)
    print_boards_row(boards, 7,8,9,4,5,6)
    print_boards_row(boards, 7,8,9,7,8,9)
    print()

class GameNode:
    def __init__(self, boards, depth,player,prev_move):
        self.boards = boards
        self.depth = depth
        self.player = player
        self.prev_move = prev_move
        return
    
    def heuristic(self):
        # checks for x win
        if self.winState(1):
            return float('inf')
        # checks for o win
        elif self.winState(2):
            return -float('inf')
        else:
            # finds the heuristic value
            heuristic = 0
            for h in range(1, 10):
                heurA = 3 * self.is_one_more_to_win(1, h) + self.possible_num_ways_win(1, h)
                heurB = -3 * self.is_one_more_to_win(2, h) - self.possible_num_ways_win(2, h)
                heuristic += heurA + heurB
            return heuristic

    def is_one_more_to_win(self, player1, i):
        currBoard = self.boards
        winCombo = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],  # rows
            [1, 4, 7], [2, 5, 8], [3, 6, 9],  # columns
            [1, 5, 9], [3, 5, 7]  # diagonals
        ]
        for combination in winCombo:
            if currBoard[i][combination[0]] == player1 and currBoard[i][combination[1]] == player1 and currBoard[i][combination[2]] == 0:
                return 1
            if currBoard[i][combination[0]] == 0 and currBoard[i][combination[1]] == player1 and currBoard[i][combination[2]] == player1:
                return 1
        return 0

    
    def possible_num_ways_win(self, player, i):
        currBoard = self.boards
        num = 0
        if player == 1:
            player2 = 2
        else:
            player2 = 1 

        if (currBoard[i][1] == player or currBoard[i][2] == player or currBoard[i][3] == player):
            if not (currBoard[i][1] == player2 or currBoard[i][2] == player2 or currBoard[i][3] == player2):
                num += 1
        if (currBoard[i][4] == player or currBoard[i][5] == player or currBoard[i][6] == player):
            if not (currBoard[i][4] == player2 or currBoard[i][5] == player2 or currBoard[i][6] == player2):
                num += 1
        if (currBoard[i][7] == player or currBoard[i][8] == player or currBoard[i][9] == player):
            if not (currBoard[i][7] == player2 or currBoard[i][8] == player2 or currBoard[i][9] == player2):
                num += 1
        if (currBoard[i][1] == player or currBoard[i][4] == player or currBoard[i][7] == player):
            if not (currBoard[i][1] == player2 or currBoard[i][4] == player2 or currBoard[i][7] == player2):
                num += 1
        if (currBoard[i][2] == player or currBoard[i][5] == player or currBoard[i][8] == player):
            if not (currBoard[i][2] == player2 or currBoard[i][5] == player2 or currBoard[i][8] == player2):
                num += 1
        if (currBoard[i][3] == player or currBoard[i][6] == player or currBoard[i][9] == player):
            if not (currBoard[i][3] == player2 or currBoard[i][6] == player2 or currBoard[i][9] == player2):
                num += 1
        if (currBoard[i][1] == player or currBoard[i][5] == player or currBoard[i][9] == player):
            if not (currBoard[i][1] == player2 or currBoard[i][5] == player2 or currBoard[i][9] == player2):
                num += 1
        if (currBoard[i][3] == player or currBoard[i][5] == player or currBoard[i][7] == player):
            if not (currBoard[i][3] == player2 or currBoard[i][5] == player2 or currBoard[i][7] == player2):
                num += 1
        return num

    #check if current state is a winning state for player
    def winState(self, player):
        currBoard = self.boards
        for i in range(1, 10):
            if (player == currBoard[i][1] == currBoard[i][2] == currBoard[i][3] or 
                player == currBoard[i][4] == currBoard[i][5] == currBoard[i][6] or
                player == currBoard[i][7] == currBoard[i][8] == currBoard[i][9] or
                player == currBoard[i][1] == currBoard[i][4] == currBoard[i][7] or
                player == currBoard[i][2] == currBoard[i][5] == currBoard[i][8] or
                player == currBoard[i][3] == currBoard[i][6] == currBoard[i][9] or
                player == currBoard[i][1] == currBoard[i][5] == currBoard[i][9] or
                player == currBoard[i][3] == currBoard[i][5] == currBoard[i][7]):
                return True
        return False

class AlphaBetaSearch:

    def __init__(self, boards):
        global curr
        state1 = GameNode(boards, 0,2, curr)
        self.gameState = state1
        self.game_tree = boards 
        return

    def alpha_beta_search(self, gameState):
        infinity = float('inf')
        bestVal = -infinity
        beta = infinity
        bestState = None
        children = self.getChildren(gameState)
        for state in children:
            value = self.minVal(state, bestVal, beta)
            if value > bestVal:
                bestVal = value
                bestState = state
        return bestState
    
   
    def maxVal(self, state, alpha, beta):
        global maxDepth

        if state.depth == maxDepth:
            return state.heuristic()

        infinity = float('inf')
        value = -infinity
        if state.winState(1) == True:
            return infinity
        if state.winState(2) == True:
            return -infinity

        children = self.getChildren(state)
        for child_state in children:
            eval = self.minVal(child_state, alpha, beta)
            value = max(value, eval)
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    
    def minVal(self, state, alpha, beta):
        global maxDepth
        if state.depth == maxDepth:
            return state.heuristic()

        infinity = float('inf')
        value = infinity

        if state.winState(1):
            return infinity
        if state.winState(2):
            return -infinity

        children = self.getChildren(state)
        for child_state in children:
            eval = self.maxVal(child_state, alpha, beta)
            value = min(value, eval)
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    # get child notes for current game state
    def getChildren(self, gameState):
        global curr
        curr_depth = gameState.depth
        next_depth = curr_depth + 1
        if gameState.player == 1:
            next_player = 2
        else:
            next_player = 1

        children = []
        board = gameState.prev_move
        boards = gameState.boards.copy()
        for i in range(1, 10):
            if boards[board][i] == 0:
                next_boards = boards.copy()
                next_boards[board][i] = next_player
                next_gameState = GameNode(next_boards, next_depth, next_player, i)
                children.append(next_gameState)
        
        return children

    # return true if the node has NO children
    # return false if the node has children 
    # def isTerminal(self, state):
    #     global maxDepth
    #     if():
    #         return True
    #     return False

# choose a move to play, we are playing X (1)
def play():
    global curr
    global num_move
    global maxDepth

    curr_board = boards

    next_move = 0
    alphabeta = AlphaBetaSearch(boards)
    nextState = alphabeta.alpha_beta_search(alphabeta.gameState)
    if nextState is None:
        print("I LOSE")
        for i in range(1, 10):
            if curr_board[curr][i] == 0:
                return i

    next_board = nextState.boards

    for i in range(1, 10):
        for m in range(1, 10):
            if curr_board[i][m] != next_board[i][m]:
                next_move = m
                break

    if num_move > 15:
        maxDepth = 5
    if num_move > 20:
        maxDepth = 6
    if num_move > 35:
        maxDepth = 8
    if num_move > 40:
        maxDepth = 10
    place(curr, next_move, 1)
    return next_move

# place a move in the global boards
def place(board, num, player):
    global curr
    global num_move
    curr = num
    boards[board][num] = player
    num_move = num_move+1

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []
   
    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        place(int(args[0]), int(args[1]), 1)
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()

    