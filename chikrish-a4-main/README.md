# a4-release

# Part-1

The K-nearest neighbor (KNN) algorithm is a simple and effective method for classification. It works by finding the K nearest training examples to the test sample and predicting the label based on the labels of these neighbors. In the modified version of the algorithm, the weight assigned to each neighbor is inversely proportional to its distance from the test sample, rather than being directly proportional to the distance. This can be useful in cases where the distances are not evenly distributed, and the inverse distance gives a more accurate representation of the similarity between the test and training samples.

To apply the KNN algorithm, we first need to compute the distance between the test and training samples. This can be done using either the Euclidean or Manhattan distance measures. Once the distances are calculated, we can sort the training samples in ascending order of their distance to the test sample, and select the K nearest neighbors. The predicted label for the test sample is then determined by the majority label of these neighbors, with the weights being inversely proportional to the distances.

In my implementation of the K-Nearest neighbour method, The function takes a list of input examples, X, and uses them to make predictions.
* For each input example, the function first computes the distances between that example and all of the examples in the training set (stored in self._X). It then sorts these distances and keeps only the indices of the self.n_neighbors closest examples.
* If the weights parameter is set to distance, the method then computes the unique values of the labels, self._y, and creates a count dictionary with each unique label as a key. 
* For each neighbor, it then adds its vote to the count dictionary. If the distance is 0, it simply increments the vote by 1. Otherwise, it adds the inverse of the distance as the weight. The label with the most votes is predicted for the input example.
* If self.weights is not set to 'distance', the function uses a simple majority voting scheme. It collects the labels of the closest neighbors and returns the most commonly occurring label.

To evaluate the accuracy of our implementation, we can compare it to the accuracy of the KNN algorithm implemented in the scikit-learn library. In general, we should expect the accuracy of our implementation to be similar to that of the scikit-learn library, as both algorithms use the same underlying principles. This can be observed in the 2 html files that are output when the knn function is called.

# Part-2

I was unable to work on the script for Part-2 much due to time constraints and complexity.

But I was able to understand that in neural networks, the fitting process involves randomly initializing weights for the hidden and output layers, and then adjusting these weights through forward and backward propagation. The activation functions applied to the hidden and output layers can vary, such as sigmoid, tanh, identity, or ReLU. The updated weights are then used to predict the target class for input data.

The code first defines the MultilayerPerceptron class, which has several attributes and methods. In the __init__ method, the class initializes several parameters, such as the number of hidden neurons and the number of training iterations, and sets up the model by creating and initializing the hidden and output layer weights. The "fit" method should train the model by performing forward and backward propagation, where the forward propagation calculates the output of the model for a given input and the backward propagation calculates the gradients of the model's error with respect to its weights, using which the weights are updated to reduce the error. The "predict" method should use the trained model to predict the class of a given input sample.
