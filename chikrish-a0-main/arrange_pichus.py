#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Chirantana Krishnappa [chikrish@iu.edu]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

def courseColumns(house_map):
    rowsX=len(house_map)
    ColsY=len(house_map[0])
    columns=[[] for c in range(ColsY)]
    for i in range(ColsY):
        for j in range(rowsX):
            columns[i].append(house_map[j][i])
    return columns

def courseRows(house_map):
    rowsX=len(house_map)
    ColsY=len(house_map[0])
    rows=[[] for r in range(rowsX)]
    for i in range(ColsY):
        for j in range(rowsX):
            rows[j].append(house_map[j][i])
    return rows


def validation(new_map):
    
    for r in new_map:
        pichuAt=[]
        a = len(r)
        for x in range(0,a):
            if r[x]=='p':
                pichuAt.append(x)
        for y in pichuAt:
            for z in range(y+1,a):
                if r[z]=='p':
                    return False
                elif r[z]=='X' or r[z]=='@':
                    break
    pichuAt=[]
    
    for c in courseColumns(new_map):
        pichuAt=[]
        b=len(c)
        for z in range(0,b):
            if c[z] == 'p':
                pichuAt.append(z)
        for k in pichuAt:
            for i in range(k+1,b):
                if c[i] == 'p':
                    return False
                elif c[i]== "X" or c[i]=='@':
                    break
        pichuAt = []

    return True

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k and validation(house_map)
    

# Arrange agents on the map
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    if is_goal(initial_house_map,k):
        return(initial_house_map,True)

    while len(fringe) > 0:
        for new_map in successors(fringe.pop()):
            if is_goal(new_map,k):
                return(new_map,True)
            else:
                if validation(new_map):
                    fringe.append(new_map)
    return(house_map,False)


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    if (k > 0):
        solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


