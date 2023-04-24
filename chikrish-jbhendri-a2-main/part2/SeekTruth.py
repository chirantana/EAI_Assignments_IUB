# SeekTruth.py : Classify data objects into two categories
#
# chikrish - jbhendri
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import re
import math
from math import log


def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(pre_process(parsed[1] if len(parsed)>1 else ""))

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

def pre_process(data):
    data = re.sub('[^a-zA-Z\s]+', '', data)
    data = re.sub(' +', ' ', data)
    data = data.lower()
    data = data.split()
    data = ' '.join(data)
    return data

# classifier : Train and apply a bayes net classifier
def classifier(train_data, test_data):

    test_label_result = []
    vocab = {}
    class1_size = 0
    class2_size = 0

    #Classes for make the code dynamic
    class1 = train_data["classes"][0]
    class2 = train_data["classes"][1]

    # Calculated the length of Class1 and Class2 entries.
    for value in train_data["labels"]:
        if value == class1:
            class1_size += 1
        else:
            class2_size += 1

    # Calculated prior probabilities.
    class1_prob = class1_size/len(train_data["objects"])
    class2_prob = class2_size/len(train_data["objects"])

    # Made a list of all the words belonging to each class.
    class1_objects = []
    class2_objects = []
    for i in range(len(train_data["objects"])):
        if train_data["labels"][i] == class1:
            class1_objects.append(train_data["objects"][i])
        elif train_data["labels"][i] == class2:
            class2_objects.append(train_data["objects"][i])  

    # Created a dictionary of all the unique Class1 words and storing their likelihood probabilities.
    for sentence in class1_objects:
        sentence = sentence.split(" ")
        visited = []
        for word in sentence:
            if (word not in vocab) & (word not in visited):
                vocab[word] = [1, 0]
                visited.append(word)
            elif word not in visited:
                vocab[word][0] += 1
                visited.append(word)

    # Created a dictionary of all the unique Class2 words
    for sentence in class2_objects:
        sentence = sentence.split(" ")
        visited = []
        for word in sentence:
            if (word not in vocab) & (word not in visited):
                vocab[word] = [0,1]
                visited.append(word)
            elif (word not in visited):
                vocab[word][1] += 1
                visited.append(word)

    #Get probabilities for each class per word
    for word in vocab:
        vocab[word][0] = (vocab[word][0] + 1) / (class1_size)
        vocab[word][1] = (vocab[word][1] + 1)/ (class2_size)

    # Took log sum instead of product to improve the calculation and avoid making the operands smaller.
    # Initialized the log sum of the classes to the prior probabilities of the classes.
    sentences = test_data["objects"]
    for sentence in sentences:
        sentence = sentence.split(" ")
        log_sum_class1 = math.log(class1_prob)
        log_sum_class2 = math.log(class2_prob)
        for word in sentence:
            
            if (word in vocab):
                log_sum_class1 += math.log(vocab[word][0])
                log_sum_class2 += math.log(vocab[word][1])

        test_label_result.append(class1 if log_sum_class1 > log_sum_class2 else class2)

    return test_label_result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))