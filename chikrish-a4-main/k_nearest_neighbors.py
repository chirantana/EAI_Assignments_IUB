# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: Chirantana Krishnappa - chikrish
#
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

from collections import Counter
import numpy as np
from utils import euclidean_distance, manhattan_distance


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y
        #raise NotImplementedError('This function must be implemented by the student.')

    #reference: https://tomaszgolan.github.io/introduction_to_machine_learning/markdown/introduction_to_machine_learning_01_knn/introduction_to_machine_learning_01_knn/
    #reference: https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html

    def predict(self, X):
        result = []  # list to store predicted labels

        # for each input example, X[i]
        for i in range(len(X)):  
            # compute distances and indexes for each neighbor
            distances = np.linalg.norm(self._X - X[i], axis=1)
            
            # sort distances and keep only the closest neighbors
            sorted_indices = np.argsort(distances)
            closest_indices = sorted_indices[:self.n_neighbors]
            
            if self.weights == 'distance':
                # compute the unique values of the labels
                unique_values = np.unique(self._y)
                # initialize the count dictionary
                count_d = {key: 0 for key in unique_values}
                
                # for each neighbor, add its vote to the count dictionary
                for index in closest_indices:
                    if distances[index] == 0:
                        count_d[self._y[index]] += 1
                    else:
                        # use the inverse of the distance as the weight
                        count_d[self._y[index]] += 1/distances[index]
                
                # predict the label with the most votes
                result.append(max(count_d, key=count_d.get))

            else:
                # for each neighbor, add its label to the list of votes
                votes = [self._y[j] for j in closest_indices]
                # predict the most commonly occurring label
                result.append(Counter(votes).most_common(1)[0][0])
                
        return result

            #raise NotImplementedError('This function must be implemented by the student.')
