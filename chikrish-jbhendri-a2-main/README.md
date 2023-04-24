# a2-release

All of the code in this repo was extensively tested on our own personal devices as well as the SICE Linux servers.

# Part 1

For this problem, we noticed that since this was a game similar in style to Chess, we could solve it by using the Minimax algorithms. Thus, we first needed to make successor functions to get each new move, and an evaluation function to return the estimated value of a given game state. 

The successor function took (by far) the most amount of time for this problem. Each color needed to have their own successor functions since their pieces needed to move in different directions. We also needed to get every possible move from the Pichus, Pikachus, and Raichus since the algorithm would need to evaluate all possible moves to find the best one. This all resulted in a significant amount of the work on the problem going into making sure that these functions return the results in the fastest and most accurate manner possible. 

Once that was working, we set out to get a good evaluation function. We opted to go for a relatively simple function that just takes the sum of the values of the maximizing pieces minus the sum of the values of the minimzing pieces. The specific weights that we gave the pieces were 1 for pichus, 3 for pikachus, and 10 for riachus. This was inspired by the values given to the pieces in a Chess game.

Finally, we implemented the Minimax algorithm with our successor and evaluation functions. This didn't take too much time since we were able to use the pseudocode given in the lectures slides for alpha-beta pruning. During the white pieces turn, the white successor function gets called, and during the black pieces team, the black successor function gets called. So the program works by alternating between turns of the maximizing player and the minimizing player by calling their respective successor functions at each step and evaluating the states found at the leafs.

To deal with the time constraint in the problem, we set up a timer with maximum time of the input. The algoriithm will give several suggested moves during that time where each new move recommended comes from the Minimax algorithm going one move deeper. This means that the first move that gets yeilded is from a Minimax with depth 1, the second move recommended is found from using a minimax tree of depth 2, and so on. We found that, depending on the board state, our algorihtm can get to a depth of anywhere between 3 and 6 moves. 

Before our algorithm goes deeper, it will check if the time has run out, and will return if it went over time. This means it will continue to run after the time limit if it is not stopped externally. However, if it gets terminated, it will just stay with recommending the move gained from the minimax depth that it last finished.

Overall, there were no major issues that we ran into here. However, we did have some discussion of methods that can be used to speed up our minimax algorithm. However, we could not come up with any good ways that produced a faster algorithm, so we just chose to leave it as it is. 

# Part 2

This part was pretty straight forward. We knew going into it that we needed to find the prior probabilities of classs 1 and 2, as well as the probabilities of each word with respect to both classes by using the training set. Once we were able to get these trained parameters, we found the probabilities of each word of the sentences in the testing data, as well as the probabilites of each class, and plugged the results into the Naive Bayes formula to get a prediction for each individual sentence.

The prior probabilities were just the number of sentences labeled with a given class divided by the total number of sentences in the training data. The conditional probabilities of each word were found by summing how many sentences the word occured in, from each class. We then added one to each of these sums to avoid probabilities of zero occuring, and divided them by the total number of word in each class. All of these probabilities were stored in a a dictionary for easy access later. We used all of these probabilites as the parameters on the test data.

Now, we went through each sentence of the testing data individually. We used our learned dictionary of probabilites to find the proabbility that each word belonged to both classes. Then, instead of multiplying them, we took the sum of logs of the probabilites. This gives the same reults as multiplication since the logs only scale the data proportionally. However, it makes it so that the numbers are much more manageable and do not get too small to deal with on the more complex sentences. Then, we set the prediction of the sentence to class 1 if the log likelihood of class 1 is greater than the log likelihood of class 2, and we predict class 2 otherwise. We append all of these predictions for every sentence into an array and return the result.

After some optimization, we found that we are getting an accuracy of 84.25%

Since Naive Bayes is a pretty simple algorithm, we did not run into any major issues in this part. Once we ironed out the bugs, it seems to work optimally.


