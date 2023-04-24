#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Chirantana Krishnappa [chikrish@iu.edu]
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
            
#Up down left right definition for the movement of pichu
#if the next x position is negative from the current position its an Up move
#if the next y position is negative from the current position its a Left move
#Similarly other moves would be increments from current position
def pathfinder(pos_x, pos_y, move):
        if (pos_y-1 == move[1]):
                return "L"
        elif (pos_y+1 == move[1]):
                return "R"
        elif (pos_x-1 == move[0]):
                return "U"
        elif (pos_x+1 == move[0]):
                return "D"
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        #Checking Bottom, Top, Left and Right positions of the current node
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] == "." or map[move[0]][move[1]] == "@") ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        #find My_loc for goal
        My_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]


        
        #Fringe stores the current location, number of steps taken to arrive and the path string that was taken to get there
        #using dummy string '-' to append path value to string
        fringe=[(pichu_loc,0,'-')]
        
        #using fringe to keep track of the visited moves
        while fringe:
                #Assign the values of fringe to the parameters for the pathfinder
                (curr_move, numStep, path)=fringe.pop(0)
                row = curr_move[0]
                column = curr_move[1]
                for move in moves(house_map, row, column):
                    #if the goal position "@" is reached return the path followed and number of steps
                        if house_map[move[0]][move[1]]=="@":
                                return (numStep+1, path[1:]+pathfinder(row, column, move))       
                        else:
                               #checking the move from moves is what direction
                                jump = pathfinder(row, column, move)
                                 
                                #Compare the last element of path and current Jump values
                                if ((path[-1] == "L" and jump == "R") or (path[-1] == "R" and jump == "L") or (path[-1] == "U" and jump == "D") or (path[-1] == "D" and jump == "U")):
                                    continue
                                else:
                                        fringe.append((move,numStep+1,path+pathfinder(row, column, move)))
# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        search(house_map)
        solution = search(house_map)
        #see if search function is returning a value that is count and path
        if(solution == None):
                print("-1, No path found")
                
        else:
                print("Here's the solution I found:")
                print(str(solution[0]) + " " + solution[1])
