#
# raichu.py : Play the game of Raichu
#
# chikrish - jbhendri
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import numpy as np
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

#Converts from a string into a N by N matrix for easier calculation
def string_to_board(board, N):
    row = []
    mat = []
    #Create the board matrix
    for i in range(len(board)):
        if (i % N == 0) & (i != 0):
            mat.append(row)
            row = []
        row.append(board[i])  
    mat.append(row)
    return np.array(mat)

def to_string(board):
    flat_board = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            flat_board += board[i][j]
    return flat_board
    
#Get the location of all the peices
#This will save computation time later at the cost of O(N) space
def get_pieces(board):
    
    #Initialize all storage for this space
    wpichu = []
    wpikachu = []
    wraichu = []
    bpichu = []
    bpikachu = []
    braichu = []
    
    #Mark the positionof every type of peice
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'w':
                wpichu.append([i, j])
            elif board[i][j] == 'W':
                wpikachu.append([i, j])
            elif board[i][j] == '@':
                wraichu.append([i, j])
            elif board[i][j] == 'b':
                bpichu.append([i, j])
            elif board[i][j] == 'B':
                bpikachu.append([i, j])
            elif board[i][j] == '$':
                braichu.append([i, j])

    return wpichu, wpikachu, wraichu, bpichu, bpikachu, braichu


#*************************NOTE: All of this following chunk of code is helper functions for the successor function***************************
#Find all moves for the white pichu peices
#Note that this will return #pichus * 2 maximum moves   
def white_pichu_moves(board, wpichu):
    moves = []
    for pic in wpichu:
        
        move = np.array(board)
        
        #Move to the left
        if (pic[1] >= 1) & (pic[0] < len(board) - 1):
            
            #Move to an empty square if it is there
            if (move[pic[0] + 1][pic[1] - 1] == '.'):
                move[pic[0]][pic[1]] = '.'
                
                if pic[0] == len(board) - 2:
                    move[pic[0] + 1][pic[1] - 1] = '@'
                else:
                    move[pic[0] + 1][pic[1] - 1] = 'w'
                moves.append(move)
                
            #Else, check to see if we can jump a black pichu
            elif (pic[1] >= 2) & (pic[0] < len(board) - 2):
                if (move[pic[0] + 1][pic[1] - 1] == 'b') & (move[pic[0] + 2][pic[1] - 2] == '.'):
                    move[pic[0]][pic[1]] = '.'
                    move[pic[0] + 1][pic[1] - 1] = '.'
                    
                    if pic[0] == len(board) - 3:
                        move[pic[0] + 2][pic[1] - 2] = '@'
                    else:
                        move[pic[0] + 2][pic[1] - 2] = 'w'
                    
                    moves.append(move)
                
        #Move to the right
        move = np.array(board)
        if (pic[1] < len(board) - 1) & (pic[0] < len(board) - 1):
            if (move[pic[0] + 1][pic[1] + 1] == '.'):
                move[pic[0]][pic[1]] = '.'
                
                if pic[0] == len(board) - 2:
                    move[pic[0] + 1][pic[1] + 1] = '@'
                else:
                    move[pic[0] + 1][pic[1] + 1] = 'w'
            
                moves.append(move)
            
            #Else, check to see if we can jump a black pichu
            elif (pic[1] < len(board) - 2) & (pic[0] < len(board) - 2):
                if (move[pic[0] + 1][pic[1] + 1] == 'b') & (move[pic[0] + 2][pic[1] + 2] == '.'):
                    move[pic[0]][pic[1]] = '.'
                    move[pic[0] + 1][pic[1] + 1] = '.'
                    
                    if pic[0] == len(board) - 3:
                        move[pic[0] + 2][pic[1] + 2] = '@'
                    else:
                        move[pic[0] + 2][pic[1] + 2] = 'w'
                    
                    moves.append(move)

    return moves

#Find all moves for the white pikachu peices
#Note that this will return #pikachus * 6 maximum moves   
def white_pikachu_moves(board, wpikachu):
    moves = []
    for pik in wpikachu:
        
        move = np.array(board)
        
        #Move to the left
        if (pik[1] >= 1):
            
            #Add the move of one left to the list if possible
            if (move[pik[0]][pik[1] - 1] == '.'):
                move[pik[0]][pik[1]] = '.'
                move[pik[0]][pik[1] - 1] = 'W'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[1] >= 2:
                    #Add the move of two left to the list
                    if (move[pik[0]][pik[1] - 2] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] - 2] = 'W'
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0]][pik[1] - 2] == 'b') | (move[pik[0]][pik[1] - 2] == 'B')) & (pik[1] >= 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] - 2] = '.'
                        move[pik[0]][pik[1] - 3] = 'W'
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0]][pik[1] - 1] == 'b') | (move[pik[0]][pik[1] - 1] == 'B')) & (pik[1] >= 2):
                #Add the move of jump two left to the list if possible
                if (move[pik[0]][pik[1] - 2] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0]][pik[1] - 1] = '.'
                    move[pik[0]][pik[1] - 2] = 'W'
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[1] >= 3:
                        if (move[pik[0]][pik[1] - 3] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0]][pik[1] - 1] = '.'
                            move[pik[0]][pik[1] - 3] = 'W'
                            moves.append(move)
                            move = np.array(board)
                        
                        
        #Move to the right
        if (pik[1] < len(board) - 1):
            
            #Add the move of one right to the list if possible
            if (move[pik[0]][pik[1] + 1] == '.'):
                move[pik[0]][pik[1]] = '.'
                move[pik[0]][pik[1] + 1] = 'W'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[1] < len(board) - 2:
                    #Add the move of two right to the list
                    if (move[pik[0]][pik[1] + 2] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] + 2] = 'W'
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0]][pik[1] + 2] == 'b') | (move[pik[0]][pik[1] + 2] == 'B')) & (pik[1] < len(board) - 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] + 2] = '.'
                        move[pik[0]][pik[1] + 3] = 'W'
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0]][pik[1] + 1] == 'b') | (move[pik[0]][pik[1] + 1] == 'B')) & (pik[1] < len(board) - 2):
                #Add the move of jump two right to the list if possible
                if (move[pik[0]][pik[1] + 2] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0]][pik[1] + 1] = '.'
                    move[pik[0]][pik[1] + 2] = 'W'
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[1] < len(board) - 3:
                        if (move[pik[0]][pik[1] + 3] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0]][pik[1] + 1] = '.'
                            move[pik[0]][pik[1] + 3] = 'W'
                            moves.append(move)
                            move = np.array(board)
                            
                            
        #Move forward
        if (pik[0] < len(board) - 1):
            
            #Add the move of one right to the list if possible
            if (move[pik[0] + 1][pik[1]] == '.'):
                move[pik[0]][pik[1]] = '.'
                
                if pik[0] == len(board) - 2:
                    move[pik[0] + 1][pik[1]] = '@'
                else:
                    move[pik[0] + 1][pik[1]] = 'W'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[0] < len(board) - 2:
                    #Add the move of two right to the list
                    if (move[pik[0] + 2][pik[1]] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        
                        if pik[0] == len(board) - 3:
                            move[pik[0] + 2][pik[1]] = '@'
                        else:
                            move[pik[0] + 2][pik[1]] = 'W'
                            
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0] + 2][pik[1]] == 'b') | (move[pik[0] + 2][pik[1]] == 'B')) & (pik[0] < len(board) - 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0] + 2][pik[1]] = '.'
                        
                        if pik[0] == len(board) - 4:
                            move[pik[0] + 3][pik[1]] = '@'
                        else:
                            move[pik[0] + 3][pik[1]] = 'W'
                            
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0] + 1][pik[1]] == 'b') | (move[pik[0] + 1][pik[1]] == 'B')) & (pik[0] < len(board) - 2):
                #Add the move of jump two right to the list if possible
                if (move[pik[0] + 2][pik[1]] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0] + 1][pik[1]] = '.'
                    
                    if pik[0] == len(board) - 3:
                        move[pik[0] + 2][pik[1]] = '@'
                    else:
                        move[pik[0] + 2][pik[1]] = 'W'
                        
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[0] < len(board) - 3:
                        if (move[pik[0] + 3][pik[1]] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0] + 1][pik[1]] = '.'
                            
                            if pik[0] == len(board) - 4:
                                move[pik[0] + 3][pik[1]] = '@'
                            else:
                                move[pik[0] + 3][pik[1]] = 'W'
                                
                            moves.append(move)
                            move = np.array(board)
    return moves
    
    
def white_raichu_moves(board, wraichu):
    
    #Set the direction
    UP = (-1, 0)
    UPRIGHT = (-1, 1)
    UPLEFT = (-1, -1)
    DOWN = (1, 0)
    DOWNRIGHT = (1, 1)
    DOWNLEFT = (1, -1)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    directions = (UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT, UPLEFT)
    
    moves = []
    
    #Loop through each riachu and each direction that it can go
    for rai in wraichu:
        for direc in directions:
            jumped = (False, 0, 0)
            move = np.array(board)
            
            #Go as far as possible in a direction before it cannot go any farther
            for i in range(1, len(board) - 1):
                if (rai[0] + direc[0] * i <= len(board) - 1) & (rai[0] + direc[0] * i >= 0) & (rai[1] + direc[1] * i <= len(board) - 1) & (rai[1] + direc[1] * i >= 0):
                    next_move = move[rai[0] + direc[0] * i][rai[1] + direc[1] * i]
                    
                    #If we can go to an empty space, do it
                    if next_move == '.':
                        move[rai[0]][rai[1]] = '.'
                        move[rai[0] + direc[0] * i][rai[1] + direc[1] * i] = '@'
                        moves.append(move)
                        move = np.array(board)
                        
                        if jumped[0] == True:
                            move[jumped[1]][jumped[2]] = '.'
                    
                    #If there is a black, jump it if possible
                    elif next_move in ['b', 'B', '$']:
                        if jumped[0] == False:
                            jumped = (True, rai[0] + direc[0] * i, rai[1] + direc[1] * i)
                            if (rai[0] + direc[0] * (i + 1) <= len(board) - 1) & (rai[0] + direc[0] * (i + 1) >= 0) & (rai[1] + direc[1] * (i + 1) <= len(board) - 1) & (rai[1] + direc[1] * (i + 1) >= 0):
                                if move[rai[0] + direc[0] * (i + 1)][rai[1] + direc[1] * (i + 1)] == '.':
                                    move[rai[0] + direc[0] * i][rai[1] + direc[1] * i] = '.'
                                
                                else:
                                    break
                            
                        #If we run into a second black, break out of the loop
                        elif jumped[0] == True:
                            break
                        
                    #If we run into a white, break out of the loop
                    elif next_move in ['w', 'W', '@']:
                        break
    return moves


#Find all moves for the black pichu peices
#Note that this will return #pichus * 2 maximum moves   
def black_pichu_moves(board, bpichu):
    moves = []
    for pic in bpichu:
        
        move = np.array(board)
        
        #Move to the left
        if (pic[1] >= 1) & (pic[0] >= 1):
            
            #Move to an empty square if it is there
            if (move[pic[0] - 1][pic[1] - 1] == '.'):
                move[pic[0]][pic[1]] = '.'
                
                if pic[0] == 1:
                    move[pic[0] - 1][pic[1] - 1] = '$'
                else:
                    move[pic[0] - 1][pic[1] - 1] = 'b'
                moves.append(move)
                
            #Else, check to see if we can jump a white pichu
            elif (pic[1] >= 2) & (pic[0] >= 2):
                if (move[pic[0] - 1][pic[1] - 1] == 'w') & (move[pic[0] - 2][pic[1] - 2] == '.'):
                    move[pic[0]][pic[1]] = '.'
                    move[pic[0] - 1][pic[1] - 1] = '.'
                    
                    if pic[0] == 2:
                        move[pic[0] - 2][pic[1] - 2] = '$'
                    else:
                        move[pic[0] - 2][pic[1] - 2] = 'b'
                    
                    moves.append(move)
                
        #Move to the right
        move = np.array(board)
        if (pic[1] < len(board) - 1) & (pic[0] >= 1):
            if (move[pic[0] - 1][pic[1] + 1] == '.'):
                move[pic[0]][pic[1]] = '.'
                
                if pic[0] == 1:
                    move[pic[0] - 1][pic[1] + 1] = '$'
                else:
                    move[pic[0] - 1][pic[1] + 1] = 'b'
            
                moves.append(move)
            
            #Else, check to see if we can jump a white pichu
            elif (pic[1] < len(board) - 2) & (pic[0] >= 2):
                if (move[pic[0] - 1][pic[1] + 1] == 'w') & (move[pic[0] - 2][pic[1] + 2] == '.'):
                    move[pic[0]][pic[1]] = '.'
                    move[pic[0] - 1][pic[1] + 1] = '.'
                    
                    if pic[0] == 2:
                        move[pic[0] - 2][pic[1] + 2] = '$'
                    else:
                        move[pic[0] - 2][pic[1] + 2] = 'b'
                    
                    moves.append(move)

    return moves

#Find all moves for the black pikachu peices
#Note that this will return #pikachus * 6 maximum moves   
def black_pikachu_moves(board, bpikachu):
    moves = []
    for pik in bpikachu:
        
        move = np.array(board)
        
        #Move to the left
        if (pik[1] >= 1):
            
            #Add the move of one left to the list if possible
            if (move[pik[0]][pik[1] - 1] == '.'):
                move[pik[0]][pik[1]] = '.'
                move[pik[0]][pik[1] - 1] = 'B'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[1] >= 2:
                    #Add the move of two left to the list
                    if (move[pik[0]][pik[1] - 2] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] - 2] = 'B'
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0]][pik[1] - 2] == 'w') | (move[pik[0]][pik[1] - 2] == 'W')) & (pik[1] >= 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] - 2] = '.'
                        move[pik[0]][pik[1] - 3] = 'B'
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0]][pik[1] - 1] == 'w') | (move[pik[0]][pik[1] - 1] == 'W')) & (pik[1] >= 2):
                #Add the move of jump two left to the list if possible
                if (move[pik[0]][pik[1] - 2] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0]][pik[1] - 1] = '.'
                    move[pik[0]][pik[1] - 2] = 'B'
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[1] >= 3:
                        if (move[pik[0]][pik[1] - 3] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0]][pik[1] - 1] = '.'
                            move[pik[0]][pik[1] - 3] = 'B'
                            moves.append(move)
                            move = np.array(board)
                        
                        
        #Move to the right
        if (pik[1] < len(board) - 1):
            
            #Add the move of one right to the list if possible
            if (move[pik[0]][pik[1] + 1] == '.'):
                move[pik[0]][pik[1]] = '.'
                move[pik[0]][pik[1] + 1] = 'B'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[1] < len(board) - 2:
                    #Add the move of two right to the list
                    if (move[pik[0]][pik[1] + 2] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] + 2] = 'B'
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0]][pik[1] + 2] == 'w') | (move[pik[0]][pik[1] + 2] == 'W')) & (pik[1] < len(board) - 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0]][pik[1] + 2] = '.'
                        move[pik[0]][pik[1] + 3] = 'B'
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0]][pik[1] + 1] == 'w') | (move[pik[0]][pik[1] + 1] == 'W')) & (pik[1] < len(board) - 2):
                #Add the move of jump two right to the list if possible
                if (move[pik[0]][pik[1] + 2] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0]][pik[1] + 1] = '.'
                    move[pik[0]][pik[1] + 2] = 'B'
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[1] < len(board) - 3:
                        if (move[pik[0]][pik[1] + 3] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0]][pik[1] + 1] = '.'
                            move[pik[0]][pik[1] + 3] = 'B'
                            moves.append(move)
                            move = np.array(board)
                            
                            
        #Move forward
        if (pik[0] >= 1):
            
            #Add the move of one right to the list if possible
            if (move[pik[0] - 1][pik[1]] == '.'):
                move[pik[0]][pik[1]] = '.'
                
                if pik[0] == 1:
                    move[pik[0] - 1][pik[1]] = '$'
                else:
                    move[pik[0] - 1][pik[1]] = 'B'
                moves.append(move)
                move = np.array(board)
                
                #Check if we can then move 2
                if pik[0] >= 2:
                    #Add the move of two right to the list
                    if (move[pik[0] - 2][pik[1]] == '.'):
                        move[pik[0]][pik[1]] = '.'
                        
                        if pik[0] == 2:
                            move[pik[0] - 2][pik[1]] = '$'
                        else:
                            move[pik[0] - 2][pik[1]] = 'B'
                            
                        moves.append(move)
                        move = np.array(board)
                    
                    #Check if we can jump a black peice at 2 distance
                    elif ((move[pik[0] - 2][pik[1]] == 'w') | (move[pik[0] - 2][pik[1]] == 'W')) & (pik[0] >= 3):
                        move[pik[0]][pik[1]] = '.'
                        move[pik[0] - 2][pik[1]] = '.'
                        
                        if pik[0] == 3:
                            move[pik[0] - 3][pik[1]] = '$'
                        else:
                            move[pik[0] - 3][pik[1]] = 'B'
                            
                        moves.append(move)
                        move = np.array(board)
                        
            #Else see if we can hop over a peice the is next to our pikachu
            elif ((move[pik[0] - 1][pik[1]] == 'w') | (move[pik[0] - 1][pik[1]] == 'W')) & (pik[0] >= 2):
                #Add the move of jump two right to the list if possible
                if (move[pik[0] - 2][pik[1]] == '.'):
                    move[pik[0]][pik[1]] = '.'
                    move[pik[0] - 1][pik[1]] = '.'
                    
                    if pik[0] == 2:
                        move[pik[0] - 2][pik[1]] = '$'
                    else:
                        move[pik[0] - 2][pik[1]] = 'B'
                        
                    moves.append(move)
                    move = np.array(board)
                    
                    #Jump 3 as well if possible
                    if pik[0] >= 3:
                        if (move[pik[0] - 3][pik[1]] == '.'):
                            move[pik[0]][pik[1]] = '.'
                            move[pik[0] - 1][pik[1]] = '.'
                            
                            if pik[0] == 3:
                                move[pik[0] - 3][pik[1]] = '$'
                            else:
                                move[pik[0] - 3][pik[1]] = 'B'
                                
                            moves.append(move)
                            move = np.array(board)
    return moves


def black_raichu_moves(board, braichu):
    
    #Set the direction
    UP = (-1, 0)
    UPRIGHT = (-1, 1)
    UPLEFT = (-1, -1)
    DOWN = (1, 0)
    DOWNRIGHT = (1, 1)
    DOWNLEFT = (1, -1)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    directions = (UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT, LEFT, UPLEFT)
    
    moves = []
    
    #Loop through each riachu and each direction that it can go
    for rai in braichu:
        for direc in directions:
            jumped = (False, 0, 0)
            move = np.array(board)
            
            #Go as far as possible in a direction before it cannot go any farther
            for i in range(1, len(board) - 1):
                if (rai[0] + direc[0] * i <= len(board) - 1) & (rai[0] + direc[0] * i >= 0) & (rai[1] + direc[1] * i <= len(board) - 1) & (rai[1] + direc[1] * i >= 0):
                    next_move = move[rai[0] + direc[0] * i][rai[1] + direc[1] * i]
                    
                    #If we can go to an empty space, do it
                    if next_move == '.':
                        move[rai[0]][rai[1]] = '.'
                        move[rai[0] + direc[0] * i][rai[1] + direc[1] * i] = '$'
                        moves.append(move)
                        move = np.array(board)
                        
                        if jumped[0] == True:
                            move[jumped[1]][jumped[2]] = '.'
                    
                    #If there is a white, jump it if possible
                    elif next_move in ['w', 'W', '@']:
                        if jumped[0] == False:
                            jumped = (True, rai[0] + direc[0] * i, rai[1] + direc[1] * i)
                            if (rai[0] + direc[0] * (i + 1) <= len(board) - 1) & (rai[0] + direc[0] * (i + 1) >= 0) & (rai[1] + direc[1] * (i + 1) <= len(board) - 1) & (rai[1] + direc[1] * (i + 1) >= 0):
                                if move[rai[0] + direc[0] * (i + 1)][rai[1] + direc[1] * (i + 1)] == '.':
                                    move[rai[0] + direc[0] * i][rai[1] + direc[1] * i] = '.'
                                
                                else:
                                    break
                            
                        #If we run into a second black, break out of the loop
                        elif jumped[0] == True:
                            break
                        
                    #If we run into a white, break out of the loop
                    elif next_move in ['b', 'B', '$']:
                        break
    return moves

#*******************************************************************************************************************************************



#Get all of the successor functions for the white peices
def white_successor(board):
    
    succ = []
    wpichu, wpikachu, wraichu, bpichu, bpikachu, braichu = get_pieces(board)
    
    succ += white_pichu_moves(board, wpichu)
    succ += white_pikachu_moves(board, wpikachu)
    succ += white_raichu_moves(board, wraichu)
    
    return succ



#Get all of the successor functions for the black peices
def black_successor(board):
    
    succ = []
    wpichu, wpikachu, wraichu, bpichu, bpikachu, braichu = get_pieces(board)
    
    succ += black_pichu_moves(board, bpichu)
    succ += black_pikachu_moves(board, bpikachu)
    succ += black_raichu_moves(board, braichu)
    
    return succ
     


#The function to evaluate a state
#Currently, it just counts how many peices are on the board for each team
#1 point for pichus, 3 points for pikachus, and 10 points for raichus
def evaluation(board, max_player):
    wpichu, wpikachu, wraichu, bpichu, bpikachu, braichu = get_pieces(board)
    value = (len(wpichu) + 3*len(wpikachu) + 10*len(wraichu))*max_player - (len(bpichu) + 3*len(bpikachu) + 10*len(braichu))*max_player
    w_count = wpichu + wpikachu + wraichu
    b_count = bpichu + bpikachu + braichu
    return value, w_count, b_count
    


#Find the successor function and the maximizing player
def successors(state, player):
    if player == 'w':
        max_player = 1
        succ = white_successor(state)
    elif player == 'b':
        max_player = -1
        succ = black_successor(state)
    return succ, max_player



#The main function for this program
#We run minimax from here and return the best state
def find_best_move(board, N, player, timelimit):
    
    #Get the successors for the initial board
    state = string_to_board(board, N)
    succ, max_player = successors(state, player)
    
    #Keep track of time to stop after the timelimit
    start_time = time.time()
    
    depth = 0
    while (time.time() - start_time < timelimit):

        #Get all of the MIN_Value functions for each state
        state_values = []
        depth += 1
        for s in succ:
            state_values.append(MIN_Value(s, -math.inf, math.inf, depth, max_player, player))

        #If no moves are found
        if len(state_values) == 0:
            return board

        #Get best value and return it
        best = succ[np.argmax(state_values)]
        yield to_string(best)



#The maximization function
#It ends when the depth remaining is 0 or when one player wins
def MAX_Value(state, alpha, beta, depth, max_player, current_player):
    
    #Handle base case
    state_worth, w_count, b_count = evaluation(state, max_player)
    if (depth == 0) | (w_count == 0) | (b_count == 0):
        return state_worth
    
    #Get all successors for the state after switching the current player's turn
    if current_player == 'w':
        current_player = 'b'
    else:
        current_player = 'w'
    succ, _ = successors(state, current_player)
    
    #Call the MIN_Value function to get the next level of states
    for s in succ:
        alpha = max(alpha, (MIN_Value(s, alpha, beta, depth - 1, max_player, current_player)))
        if alpha >= beta:
            return alpha
        
    return alpha



#The minimzation function
#It ends when the depth remaining is 0 or when one player wins
def MIN_Value(state, alpha, beta, depth, max_player, current_player):
    
    #Handle base case
    state_worth, w_count, b_count = evaluation(state, max_player)
    if (depth == 0) | (w_count == 0) | (b_count == 0):
        return state_worth
    
    #Get all successors for the state after switching the current player's turn
    if current_player == 'w':
        current_player = 'b'
    else:
        current_player = 'w'
    succ, _ = successors(state, current_player)
    
    #Call the MAX_Value function to get the next level of states
    for s in succ:
        beta = min(beta, MAX_Value(s, alpha, beta, depth - 1, max_player, current_player))
        if alpha >= beta:
            return beta
    
    return beta



if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")
    
    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
