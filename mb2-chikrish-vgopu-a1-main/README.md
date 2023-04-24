# mb2-chikrish-vgopu-a1
Contains code for Fall 2022 CSCI-B 551 assignment 1.

Part 1:
This problem consisted of writing a program that could put the numbers 1-5 in order (the goal state). The numbers were stored in a list, [N1, N2, N3, N4, N5], with the order unknown (presumably) The numbers could be moved to reach the correct order by swapping adjacent numbers. For example the swaps for the above list would be N1 & N2, N2 & N3, N3 & N4, and N4 & N5. Only one swap could be performed at a time. The program would also report the exact path of swaps to get from a given starting state to the goal state.

With the four possible swaps, for a given parent state there could be four possible child states. While BFS approach could find a solution, it would be slow (take the worst case example where numbers are in exactly reverse order). An A* approach was taken, implementing a heuristic and priority que, to improve the speed of the search. The heuristic (h(s)) was calculated by taking the difference of the two values that were swapped to create a particular child state. For example, N1 - N2 would be the heuristic value for a given state. This heuristic is admissible because it never over estimates the number of moves to reach a goal state. For example, if the starting state was [5, 1, 2, 3, 4] then calculating the swap value for swapping 5 and 1 would result in the value 4. In this example 5 is the only number out of place but it will take 4 swaps to get it into place.

The child states were then ordered by f(s) = g(s) + h(s). The cost of each swap was decided to be the same because regardless of which swap was chosen, a swap would consist of moving one number forward and one number backward. Therefor, the g(s) term was ignored. The child states where then ordered only by h(s). The ordered list of child states became the priority cue for the search.


Part 2: The 2022 Solver for 25 tile puzzle.
When given a mixed board, the question asks you to correctly organize a 5x5 puzzle. The A* algorithm has been our method of choice for solving this puzzle. To address this issue, a number of factors and actions have been considered, including the following:
The state space is created by arranging all 25 tiles on the board without using the same tile twice.
Initial state: The jumbled tiles that make up the board's initial state must rotate in all directions in order to move toward the desired state.
Goal state: In this puzzle, the goal state is a fully solved puzzle with every tile numbered from 1 to 25 in its proper position.
All 24 potential states are produced by moving a row left or right, moving a culumn up or down, as well as rotating the inner and outer elements of the elements in both clockwise and counter-clockwise directions.
Successor Function: This Function generates all the possible boards from the initial board by doing the 24 types of board manipulations {'R1','R2','R3','R4','R5','L1','L2','L3','L4','L5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Ic','Occ','Icc'}. We found that all 24 successor states could be gnerated by the helper functions found in the 'test-a1_2022_puzzle.py' file.
After generation of successor boards, we calculate the heuristic value and store it as a list
Referred this website for proper understanding of Cost and A*:
[https://dhruvs.space/posts/understanding-the-a-star-algorithm/#the-a-star-algorithm]
Cost Function: The cost function in this case is H(s) + G(s), where G(s) is the cost of the cheapest path to s so far, Cost per move is taken to be 1, and H(s) is the heuristic function. 
Heuristic: The Manhattan distance is the heuristic function that we have employed. The heuristic in this case yields the total Manhattan distance between each tile in the current position and the board's desired goal state. Another heuristic considered was how far a value was from its correct spot in the number line. Both of these heuristics are admissible because they do not overestimate the cost but the Manhattan distance was found to be a better estimate of the cost.
Algorithm: Instead of using a priority queue, we have implemented the frontier using a heapq data structure. The root node is maintained with the minimum heuristic value at the priority to pop and append to the visited nodes list whenever we go through each successor.
Each popped board is checked if it’s the goal state until the fringe is empty.
The successors are chosen using the cost function which takes the number of movements needed to arrive at a state, and its manhattan distance together. The most valued successor node is chosen for the next iteration of boards.
1.	In this problem, what is the branching factor of the search tree?
Answer: Here the branching factor is 24 for the search tree.
2.	If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine.	
Answer: If the same is implemented with BFS, the tree would expand for each successor until we find the solution which is ‘s’. The depth of such a tree would be with the branching factor of 24 for each successor.
If the solution can be reached in 7 moves, the number of states that we would need to explore before we find ‘s’ would be 24^7

Part 3:
To solve this problem the following cost functions could be used in addition to a heuristic, f(s) = g(s) + h(s).
The cost function, g(s), would vary depending on the cost-function selected when the program is run. For the segments the cost function, g(s) would equal the number of segments traveled from the starting location to the current successor state. For the distance cost function, g(s) would equal the miles traveled from the starting location to the current successor state. For the time cost function, g(s) would equal the distance multipled by the speed for each segment traveled from the starting location to the current successor.
A heuristic function, h(s) for this problem might be the straight line distance from a successor to the goal state using the GPS coordinates. This would be an admissible heuristic because it would never overestimate the distance to a goal state, given that the shortest distance between two points is a straight line. 

 A* search will be implemented to minimize the cost that depends upon the cost type. For every cost type the minimized of g(s) + h(s) will be found, where the g(s) is the cost till that point and h(s) will be the heuristic cost, that is the goal. One will be the minimum number of segments required to traverse to the goal, if the current state isn't the goal state because the heuristic is admissible.
 Euclidean distance will be used to get the minimum distance that is calculated from one point to the other point. The h(s) can be the euclidean distance from the point 1 which is the current state to the other point, which can be the goal state.
 
 We are using the maximum speed to calculate the minimum time that is required to move from the start point to the destination. Edge weight can be the estimated delivery time that is given by the time taken for the segment plus the probability of the extra time required, this gives us an approximate delivery time.
 In the successor function, we compare all the nodes that are present in the fringe, when we compare the nodes we pick the one that gives us the minimum cost based upon the comparison. We pick the minimum cost from all the nodes. During the execution we compare all the nodes that are the neighbors of the current/Present node and then append them into the fringe.
