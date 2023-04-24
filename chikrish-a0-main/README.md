
Assignment 0 : Maps and Python
Part 1: Help pichu fly to the agent
Graph abstraction:
We specify the problem as a map abstraction where points are indicated by ".","x","X","p" or "@". 
P is the initial state
Successor Function: any of the 4 neighbours of p, where there is no X.
Set of states: possible states of p is positioned at any point which is "." or "@".
Goal State: Goal state is the state where pichu reaches agent "@"
Cost Function: 1 cost per movement
Solution:

The proposed solution to find the path between pichu and agent is by implementing the breadth first search on the said graph using a queue.

Part 2: Help pichus play hide and seek
We can specify the problem as a graph abstraction each state is the graph with a certain number of pichus on it.
Initial State: The one given by the user as input, it can have one pichu and one agent.
Successor Function: The successor of each state will be with another pichu on a valid position.
Set of states: Set of valid states, which is, when no two pichus can see each other.
Goal State: Goal state is the state where maximum pichus have been placed on the graph.
Cost Function: check cost is 1
Solution:
Check if there are any points not directly traversed by p location and set the next pichu on the point not in the same row, column or diagonal as original p
