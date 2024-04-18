from copy import deepcopy
from sys import argv
import time
import random

board = [
[5, 3, 0, 0, 7, 0, 0, 0, 0],
[6, 0, 0, 1, 9, 5, 0, 0, 0],
[0, 9, 8, 0, 0, 0, 0, 6, 0],
[8, 0, 0, 0, 6, 0, 0, 0, 3],
[4, 0, 0, 8, 0, 3, 0, 0, 1],
[7, 0, 0, 0, 2, 0, 0, 0, 6],
[0, 6, 0, 0, 0, 0, 2, 8, 0],
[0, 0, 0, 4, 1, 9, 0, 0, 5],
[0, 0, 0, 0, 8, 0, 0, 7, 9]
]
# board = [
# [9, 0, 0, 0, 0, 0, 6, 0, 0],
# [6, 0, 1, 0, 2, 5, 3, 0, 9],
# [0, 0, 7, 0, 3, 6, 0, 8, 0],
# [0, 5, 0, 0, 0, 4, 0, 0, 0],
# [8, 0, 4, 2, 5, 0, 7, 0, 6],
# [0, 7, 0, 0, 6, 0, 4, 5, 0],
# [2, 0, 3, 5, 4, 0, 0, 9, 0],
# [0, 0, 9, 0, 7, 8, 2, 0, 3],
# [0, 0, 0, 0, 0, 0, 1, 0, 0]
# ]

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
                
            if j == 8: # at the end of row
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None

def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False

# Function for BFS solution
def solveBFS(board):
    # search for the first empty cell
    find = find_empty(board)

    if (not find):
        # if not have empty cells, then the sudoku is solved
        return True
    else:
        # if have a empty cell, get the row and column index
        row, col = find

    # create a array of possible board solutions
    solutions = []

    # loop to test all possible values 1 to 9
    for i in range(1,10):
        # verify if is a valid number, considering sudoku rules
        if (valid(board, i , (row,col))):
            # copy the actual board to a new one
            newList = deepcopy(board)

            # insert the new valid value to the new board
            newList[row][col] = i

            # append board to the list
            solutions.append(newList)

    # loop to test all possibilities for the last validation
    for i in range(len(solutions)):
        # call recursive solveBFS to continue the actual solution board
        # if the result is true, the sudoku has been solved
        # if not, continue to next possible board
        if (solveBFS(solutions[i])):
            return True

    return False

# Function for DFS solution
def solveDFS(board):
    # search for the first empty cell
    find = find_empty(board)

    if not find:
        # if not have empty cells, then the sudoku is solved
        return True
    else:
        # if have a empty cell, get the row and column index
        row, col = find

    # loop to test all possible values 1 to 9
    for i in range(1,10):
        # verify if is a valid number, considering sudoku rules
        if (valid(board, i , (row,col))):
            # insert the valid value to board
            board[row][col] = i

            # call solveDFS recursive to continue this board
            # if the result is true, the sudoku has been solved
            if (solveDFS(board)):
                return True
            # if not, change the actual valid value to 0 and continue testing next value
            board[row][col] = 0

    return False

# Function for AStar solution
def solveAStar(board):
    # create a array of possible board solutions
    solutions = []

    # loop to run in all board
    for i in range(9):
        for j in range(9):
            # create a list with all posibilities
            x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            # check if cell is empty
            if (board[i][j] == 0):
                # loop to verify and remove incorrect numbers from row, column and quadrant
                for k in range(9):
                    if (board[i][k] != 0 and board[i][k] in x):
                        x.remove(board[i][k])
                    if (board[k][j] != 0 and board[k][j] in x):
                        x.remove(board[k][j])
                quad_x = j // 3 #used integer division to get the integer value from positions
                quad_y = i // 3
                for m in range(quad_y * 3, quad_y * 3 + 3):
                    for n in range(quad_x * 3, quad_x * 3 + 3):
                        if (board[m][n] != 0 and board[m][n] in x and (m, n) != (i,j)):
                            x.remove(board[m][n])
                tmp = []
                tmp.append(i)
                tmp.append(j)
                tmp.append(len(x))
                tmp.append(x)

                # insert ordered, lowest first
                index = 0
                for k in range(len(solutions)):
                    if (solutions[k][2] > tmp[2] and tmp[2] > 0):
                        index = k
                        break
                    else:
                        index+=1
                solutions.insert(index, tmp)

    if (len(solutions) > 0):
        row = solutions[0][0]
        col = solutions[0][1]

        # loop in array of solutions of current recursion
        for i in solutions[0][3]:
            # insert the valid value to board
            board[row][col] = i

            # if not find empty cell print result or call recursive to next cell
            if (not find_empty(board)):
                return True
            elif solveAStar(board):
                return True
            # if not, change the actual valid value to 0 and continue testing next value
            board[row][col] = 0

        return False
    
print_board(board)
startTime = time.time()
solveAStar(board)
print("Solved:")
elapsedTime = time.time() - startTime
print("Elapsed time(s): " + str(elapsedTime))
print_board(board)