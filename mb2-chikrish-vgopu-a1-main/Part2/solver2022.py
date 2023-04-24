#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Matt Brown (mb2), Chirantana Krishnappa (chikrish), and Venkata Dinesh Gopu (vgopu)
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022


import sys
import copy
from copy import deepcopy
import numpy as np
import heapq as hp
import math


#Set the rows, columns and the required goal_state
ROWS=5
COLS=5
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

#movement functions derived from test_a1_puzzle.py
def move_right(board, row):
  """Move the given row to one position right"""
  new_board = deepcopy(board)
  new_board[row] = new_board[row][-1:] + new_board[row][:-1]
  return new_board

def move_left(board, row):
  """Move the given row to one position left"""
  new_board = deepcopy(board)
  new_board[row] = new_board[row][1:] + new_board[row][:1]
  return new_board

#outer rotate helper
def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

#Move the board's outer columns and rows, clockwise
def outer_clockwise(board):
    new_board=deepcopy(board)
    new_board[0]=[new_board[1][0]]+new_board[0]
    residual=new_board[0].pop()
    new_board=transpose_board(new_board)
    residual=rotate_right(new_board,-1,residual)
    new_board=transpose_board(new_board)
    residual=rotate_left(new_board,-1,residual)
    new_board=transpose_board(new_board)
    residual=rotate_left(new_board,0,residual)
    new_board=transpose_board(new_board)
    return new_board

#Move the board's outer columns and rows, counter clockwise
def outer_counterclockwise(board):
    new_board=deepcopy(board)
    new_board[0]=new_board[0]+[new_board[1][-1]]
    residual=new_board[0].pop(0)
    new_board=transpose_board(new_board)
    residual=rotate_right(new_board,0,residual)
    new_board=transpose_board(new_board)
    residual=rotate_right(new_board,-1,residual)
    new_board=transpose_board(new_board)
    residual=rotate_left(new_board,-1,residual)
    new_board=transpose_board(new_board)
    return new_board

#Inner rotate helper
def inner_rotate_right(board,row,residual):
    board[row] = board[row][:2] + [residual] + board[row][2:]
    residual=board[row].pop(-2)
    return residual

def inner_rotate_left(board,row,residual):
    board[row] = board[row][:3] + [residual] + board[row][3:]
    residual=board[row].pop(1)
    return residual

#moves the inner columns and rows clockwise
def inner_clockwise(board):
    new_board=deepcopy(board)
    new_board[1]=[new_board[1][0]]+[new_board[2][1]]+new_board[1][1:]
    residual=new_board[1].pop(4)
    new_board=transpose_board(new_board)
    residual=inner_rotate_right(new_board,-2,residual)
    new_board=transpose_board(new_board)
    residual=inner_rotate_left(new_board,-2,residual)
    new_board=transpose_board(new_board)
    residual=inner_rotate_left(new_board,1,residual)
    new_board=transpose_board(new_board)
    return new_board

#moves the outer columns and rows counter clockwise
def inner_counterclockwise(board):
    new_board=deepcopy(board)
    new_board[1]=new_board[1][0:-1]+[new_board[2][-2]]+[new_board[1][-1]]
    residual=new_board[1].pop(1)
    new_board=transpose_board(new_board)
    residual=inner_rotate_right(new_board,1,residual)
    new_board=transpose_board(new_board)
    residual=inner_rotate_right(new_board,-2,residual)
    new_board=transpose_board(new_board)
    residual=inner_rotate_left(new_board,-2,residual)
    new_board=transpose_board(new_board)
    return new_board

#turns rows into columns and columns into rows
def transpose_board(board):
  """Transpose the board --> change row to column"""
  new_board = deepcopy(board)
  return [list(col) for col in zip(*new_board)]



def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#hueristic to find the manhattan distance between the chosen state and the goal
def heuristic(state):
    brd = dict() #the board
    distance = 0 #manhattan distance
    var = 1 #init a var to start from 1
    for t in range(0,ROWS):
        for s in range(0,COLS):
            brd[var] = (t,s)
            var = var+1    
    for i in range(0,ROWS):        
        for j in range(0,COLS):
            val = brd[state[i][j]]
            row_val, col_val = val
            #Return a distance with the difference between the goal state position and the current state position of the cols and rows
            distance = distance + (abs(i-row_val) + abs(j-col_val))
    return distance

# Derived from function path_finder found in test_a1_puzzle.py
# return a list of 24 possible successor states, with each state consisting of one round of rotation of each row and column upwards and downwards
def successors(state):
    succsr_node,old_board=[],[]
    for i in range(0,(ROWS*COLS),ROWS):
        #Converts the board into lists of 5x5
        old_board.append(list(state[i:i+ROWS]))
    cboard = deepcopy(old_board)
    valid_moves_set={'R1','R2','R3','R4','R5','L1','L2','L3','L4','L5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Ic','Occ','Icc'}
    for direction in valid_moves_set:
        move = deepcopy(direction)
        if set(direction).intersection(set(['R','L','U','D'])):
            direction,index=direction
            index=int(index)-1
        if direction == "R":
            successor_board = move_right(cboard, index)
        elif direction == "L":
            successor_board = move_left(cboard, index)
        elif direction == "U":
            successor_board = transpose_board(move_left(transpose_board(cboard), index))
        elif direction == "D":
            successor_board = transpose_board(move_right(transpose_board(cboard), index))
        elif direction == 'Oc':
            successor_board = outer_clockwise(cboard)
        elif direction == 'Occ':
            successor_board = outer_counterclockwise(cboard)
        elif direction == 'Ic':
            successor_board = inner_clockwise(cboard)
        elif direction == 'Icc':
            successor_board = inner_counterclockwise(cboard)
        #Find the manhattan distance of each successor board and store it
        m_distance = heuristic(successor_board)
        AllSuccessors = [item for row in successor_board for item in row]
        #store all the successor nodes with the manhattan_distance and the move used to arrive at the state
        succsr_node.append([m_distance,AllSuccessors,move])
    return succsr_node

# check if we've reached the goal
def is_goal(state):
    #if the current state is not equal to the goal state
    if state == goal_state:
        return True
    return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    visited_nodes=[]
    current_initial_board = list(initial_board)
    fringe=[[0,current_initial_board,[]]]
    #heapify the fringe to emulate a priority queue
    hp.heapify(fringe)
    while fringe:
        #iterate until the fringe is empty
        node = hp.heappop(fringe)
        #Check whether the initial node in the fringe heap is the goal state
        if is_goal(node[1]):
            break

        #Maintain the visited nodes as each root gets popped from the heap
        visited_nodes.append(node[1])
        for movement in successors(node[1]):
            is_visited = False
            #cost function that has the total movements that takes to reach a node
            cost = len(node[2])+movement[0]+1
            for item in fringe:
                #check if a successor is already been visited, set the visited flag to true
                    if movement[0] == item[1]:
                        is_visited = True
                        break
            #if the successor is not in visited nodes and not flagged
            if movement[1] not in visited_nodes and not is_visited:
                #append the fringe queue with the total cost, and the rotations and the board as details
                    hp.heappush(fringe,(cost,movement[1],node[2][0:]+[movement[2]]))
            for succsr in fringe:
                #if there is a successor with less cost than the root successor, we switch to that node to get next set of successors
                if movement[1] == succsr[1] and cost < succsr[0]:
                    succsr = movement
                    break
    return node[2]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))