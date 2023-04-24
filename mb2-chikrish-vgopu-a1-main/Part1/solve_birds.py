#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: Matt Brown (mb2), Chirantana Krishnappa (chikrish), and Venkata Dinesh Gopu (vgopu)
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys

N=5

#####
# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# Given a state, return a list of successor states
def successors(state):
    # Get all the possible successors for a given state
    possible_successors = [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

    # Order the list of all possible successors using the heuristic function
    ordered_successors = h(state, possible_successors)

    return ordered_successors

# Heuristic function:
# Evalutes the list of successors and orders them by which successors provided the greatest benefit.
def h(state, successors):
    swapped = []

    # For each successor in the list, identify which values were swapped to create that successor
    # Then calculate the difference of those two values. This is the cost/benefit for making the swap
    # Then create a tuple and store the successor state and calculated difference in the tuple
    # Then add the tuple to a list
    for s in successors:
        for i in range(0, len(state) - 1):
            if state[i] != s[i]:
                swapped.append((s, state[i] - state[i+1]))
                break

    # Order the tuple list of possible successors but the calculated difference values.
    # The code for ordering was borrowed from here
    # https://bobbyhadz.com/blog/python-sort-list-of-tuples-by-second-element
    swapped = sorted(swapped, key=lambda t: t[1])

    # Remove the successors from the tuple to return just a list of the successors
    ordered_successors = []
    for swap in swapped:
        ordered_successors.append(swap[0])

    return ordered_successors

#########
#
# THE ALGORITHM:
#
# This is a generic solver using BFS.
#
def solve(initial_state):
    fringe = []
    explored = []

    fringe += [(initial_state, []),]

    while len(fringe) > 0:
        (state, path) = fringe.pop(0)

        if is_goal(state):
            return path+[state,]

        for s in successors(state):
            if s in explored:
                # Don't explore a state that was previously explored
                continue
            else:
                explored.append(s)
                fringe.append((s, path+[state,]))

    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))



