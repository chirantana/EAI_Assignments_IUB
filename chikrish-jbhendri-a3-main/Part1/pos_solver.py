###################################
# CS B551 Fall 2022, Assignment #3
#
# Your names and user ids: chikrish and jbhendri
#
# (Based on skeleton code by D. Crandall)
#


import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    #E is used in place of any 0's in order to avoid any multiplication or division by 0
    E = pow(10, -50)
    trans = {}
    skip_trans = {}
    emission = {}
    forward_emission = {}
    initial = {}
    gibbs = {}
    
    # Calculate the log of the posterior probability of a given sentence
    # add 10^(-50) to avoid the case where the probability is 0
    def posterior(self, model, sentence, label):
        
        #For this one, we simply need to multiply the emissions and initial values for each word
        if model == "Simple":
            prob = 0
            for i in range(len(sentence)):
                if sentence[i] in self.emission:
                    if prob ==0:
                        prob = self.emission[sentence[i]][label[i]] * self.initial[label[i]]    
                    else:
                        prob *= self.emission[sentence[i]][label[i]] * self.initial[label[i]]   
                else:
                    if prob ==0:
                        prob = self.initial[label[i]]    
                    else:
                        prob *= self.initial[label[i]]   

            return math.log(prob + pow(10, -50))
                
        #For this one, we simply need to multiply the emissions, initial values, and transition for each word
        elif model == "HMM":
            prob = 0
            for i in range(len(sentence)):
                if sentence[i] in self.emission:
                    if prob ==0:
                        prob = self.emission[sentence[i]][label[i]] * self.initial[label[i]]    
                    else:
                        prob *= self.emission[sentence[i]][label[i]] * self.trans[label[i-1]][label[i]]
                else:
                    if prob ==0:
                        prob = self.initial[label[i]]    
                    else:
                        prob *= self.trans[label[i-1]][label[i]]

            return math.log(prob + self.E)
        
        
        elif model == "Complex":
            prob = 0

            for j in range(len(sentence)):
                if sentence[j] in self.emission:
                    
                    #Get probability for first word
                    if j == 0:
                        if (len(sentence) <= 1) | (self.forward_emission[sentence[j]][label[j]] <= pow(10, -50)):
                            prob = self.initial[label[j]] * self.emission[sentence[j]][label[j]]
                        else:
                            prob = self.initial[label[j]] * self.emission[sentence[j]][label[j]] * self.forward_emission[sentence[j]][label[j]]
    
                    #Get probability for second word
                    elif j == 1:
                        if (len(sentence) <= 2) | (self.forward_emission[sentence[j]][label[j]] <= pow(10, -50)):
                            prob *= self.emission[sentence[j]][label[j]] * self.trans[label[j-1]][label[j]]
                        else:
                            prob *= self.emission[sentence[j]][label[j]] * self.trans[label[j-1]][label[j]] * self.forward_emission[sentence[j]][label[j]]
    
                    #Get probability for final word
                    else:
                        if (j == len(sentence) - 1) | (self.forward_emission[sentence[j]][label[j]] <= pow(10, -50)):
                            prob *= self.emission[sentence[j]][label[j]] * self.trans[label[j-1]][label[j]] * self.skip_trans[label[j-2]][label[j]]
                        else:
                            prob *= self.emission[sentence[j]][label[j]] * self.trans[label[j-1]][label[j]] * self.skip_trans[label[j-2]][label[j]] * self.forward_emission[sentence[j]][label[j]]

            return math.log(prob + self.E)
        
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        
        #Get emission counts
        for sentence in data:
            prev_pos = None
            for nxt in range(len(sentence[0])):
                
                word = sentence[0][nxt]
                pos = sentence[1][nxt]

                #If this is a new word, at it to the vocab
                if word not in self.emission:
                    self.emission[word] = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E
                                           , "noun":self.E, "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E}
                    
                if word not in self.forward_emission:
                    self.forward_emission[word] = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E
                                           , "noun":self.E, "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E}
                    
                #increment the probability of the word being the specified pos
                self.emission[word][pos] += 1
                if nxt >= 1:
                    self.forward_emission[word][prev_pos] += 1
                    
                prev_pos = pos
                
        #initialze initial and transision matrices
        self.initial = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E, "noun":self.E,
                        "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E} 
        self.trans = {"adj":{}, "adv":{}, "adp":{}, "conj":{}, "det":{}, "noun":{}, "num":{}, "pron":{}, "prt":{}, "verb":{}, "x":{}, ".":{}}
        for pos in self.trans:
            self.trans[pos] = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E, "noun":self.E,
                               "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E}
        self.skip_trans = {"adj":{}, "adv":{}, "adp":{}, "conj":{}, "det":{}, "noun":{}, "num":{}, "pron":{}, "prt":{}, "verb":{}, "x":{}, ".":{}}
        for pos in self.trans:
            self.skip_trans[pos] = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E, "noun":self.E,
                               "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E}



        #Count the number of transitions and initials for each pos
        for sentence in data:
            count = 0
            previous_pos = None
            skip_pos = None
            for nxt in range(len(sentence[0])): 
                
                pos = sentence[1][nxt]
                
                if count == 0:
                    self.initial[pos] += 1
                elif count == 1:
                    self.trans[previous_pos][pos] += 1
                else:
                    self.skip_trans[skip_pos][pos] += 1
                    self.trans[previous_pos][pos] += 1
                
                if previous_pos != None:
                    skip_pos = previous_pos
                    
                previous_pos = pos
                count += 1

                
             
        #Normaize forward emission
        for t in self.forward_emission:
            tot = 0
            for val in self.forward_emission[t]:
                tot += self.forward_emission[t][val]
            for val in self.forward_emission[t]:
                self.forward_emission[t][val] = self.forward_emission[t][val] / tot

                
        #Normaize emission
        for t in self.emission:
            tot = 0
            for val in self.emission[t]:
                tot += self.emission[t][val]
            for val in self.emission[t]:
                self.emission[t][val] = self.emission[t][val] / tot
                 
        #Normalize initial
        tot = 0
        for val in self.initial:
            tot += self.initial[val]
        for val in self.initial:
            self.initial[val] = self.initial[val] / tot      
            
        #Normaize transition
        for t in self.trans:
            tot = 0
            for val in self.trans[t]:
                tot += self.trans[t][val]
            for val in self.trans[t]:
                self.trans[t][val] = self.trans[t][val] / tot
                
        #Normaize skip transition
        for t in self.skip_trans:
            tot = 0
            for val in self.skip_trans[t]:
                tot += self.skip_trans[t][val]
            for val in self.skip_trans[t]:
                self.skip_trans[t][val] = self.skip_trans[t][val] / tot
                
        self.train_gibbs(data)
                
    def train_gibbs(self, data):
        
        states = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]
        
        #Loop that controls how many samples are being used.
        for i in range(100000):
            
            #Generate new samples
            r = random.randint(1,len(data)-1)
            sample = data[r][0]
            labels = ["x"] * len(sample)
            
            #Goes through each word of the sentence
            for j in range(len(sample)):
                
                #Update label of first word
                if j == 0:
                    if len(sample) <= 1:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.initial[s] * self.emission[sample[j]][s] > best_val:
                                best_val = self.initial[s] * self.emission[sample[j]][s]
                                best_pos = s
                        labels[j] = best_pos
                    else:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.initial[s] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s] > best_val:
                                best_val = self.initial[s] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s]
                                best_pos = s
                        labels[j] = best_pos
                
                #Update label of second word
                elif j == 1:
                    
                    if len(sample) <= 2:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.trans[labels[j-1]][labels[j]] * self.emission[sample[j]][s] > best_val:
                                best_val = self.trans[labels[j-1]][labels[j]] * self.emission[sample[j]][s]
                                best_pos = s
                        labels[j] = best_pos
                        
                    else:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.trans[labels[j-1]][labels[j]] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s] > best_val:
                                best_val = self.trans[labels[j-1]][labels[j]] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s]
                                best_pos = s
                        labels[j] = best_pos
                
                #Update label of every other word
                else:
                    if j == len(sample) - 1:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.trans[labels[j-1]][labels[j]] * self.skip_trans[labels[j-2]][labels[j]] * self.emission[sample[j]][s]> best_val:
                                best_val = self.trans[labels[j-1]][labels[j]] * self.skip_trans[labels[j-2]][labels[j]] * self.emission[sample[j]][s]
                                best_pos = s
                        labels[j] = best_pos
                    else:
                        best_val = -1
                        best_pos = ''
                        for s in states:
                            if self.trans[labels[j-1]][labels[j]] * self.skip_trans[labels[j-2]][labels[j]] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s] > best_val:
                                best_val = self.trans[labels[j-1]][labels[j]] * self.skip_trans[labels[j-2]][labels[j]] * self.emission[sample[j]][s] * self.forward_emission[sample[j+1]][s]
                                best_pos = s
                        labels[j] = best_pos
                        
            #Counts the occurances of a word having a label s
            for j in range(len(sample)):
                if sample[j] not in self.gibbs:
                    self.gibbs[sample[j]] = {"adj":self.E, "adv":self.E, "adp":self.E, "conj":self.E, "det":self.E
                                           , "noun":self.E, "num":self.E, "pron":self.E, "prt":self.E, "verb":self.E, "x":self.E, ".":self.E}
                self.gibbs[sample[j]][labels[j]] += 1
        
        #Normaize gibbs samples
        for t in self.gibbs:
            tot = 0
            for val in self.gibbs[t]:
                tot += self.gibbs[t][val]
            for val in self.gibbs[t]:
                self.gibbs[t][val] = self.gibbs[t][val] / tot
            


    def simplified(self, sentence):
        
        solution = []
        for word in sentence:
            mx = 0
            pred = ""
            
            #If a word is in the emission, predict the value that comes from the max of emission and initial tables for the each label
            if word in self.emission:
                for i in self.emission[word]:
                    if i == 0:
                        if self.emission[word][i] * self.initial[i] > mx:
                            mx = self.emission[word][i] * self.initial[i]
                            pred = i
                    else:
                        if self.emission[word][i]  > mx:
                            mx = self.emission[word][i] 
                            pred = i      
            #Else, get the maximum initial prediction
            else:
                for i in self.initial:
                    if self.initial[i] > mx:
                        mx = self.initial[i]
                        pred = i
                        
            solution.append(pred)
            
        return solution

    def hmm_viterbi(self, sentence):
        
        #Initialize tables
        N = len(sentence)
        states = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]
        V_table = {"adj":[0] * N, "adv":[0] * N, "adp":[0] * N, "conj":[0] * N, "det":[0] * N, "noun":[0] * N, 
                   "num":[0] * N, "pron":[0] * N, "prt":[0] * N, "verb":[0] * N, "x":[0] * N, ".":[0] * N} 
        which_table = {"adj":[0] * N, "adv":[0] * N, "adp":[0] * N, "conj":[0] * N, "det":[0] * N, "noun":[0] * N, 
                   "num":[0] * N, "pron":[0] * N, "prt":[0] * N, "verb":[0] * N, "x":[0] * N, ".":[0] * N} 
        viterbi_seq = [""] * N
        
        #Set beginning of each table
        if sentence[0] in self.emission:
            for s in states:
                V_table[s][0] = self.initial[s] * self.emission[sentence[0]][s]
        else:
            for s in states:
                V_table[s][0] = self.initial[s]
            
        i = 0
        for i in range(1, N):
            
            for s in states:
                
                #Set emission probability if this is a known word
                #If it is not known, just use the probability of the pos occuring
                if sentence[i] in self.emission:
                    V_table[s][i] = self.emission[sentence[i]][s]
                else:
                    V_table[s][i] = self.initial[s]
                    
                #Find the valuesof each state that can be next
                mx = -1
                best_pos = ''
                for nxt in states:
                    if V_table[nxt][i-1] * self.trans[nxt][s] > mx:
                        mx = V_table[nxt][i-1] * self.trans[nxt][s]
                        best_pos = nxt
                V_table[s][i] *= mx
                which_table[s][i] = best_pos

        #Find the maximum end value and use it as th most likely ending position
        max_end = -1
        best_pos = ''
        for nxt in states:
            if V_table[nxt][i] > max_end:
                max_end = V_table[nxt][i]
                best_pos = nxt
        viterbi_seq[N-1] = best_pos    
              
        #Work backward from the end position through the table
        for i in range(N-2, -1, -1):
            viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]
            
        #Return most likely sequence
        return viterbi_seq

    def complex_mcmc(self, sentence):
        solution = []
        states = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]
        count = 0
        prev = None
        for word in sentence:
            mx = 0
            pred = ""
            
            #If a word is in the emission, predict the value that comes from the max of emission and initial tables for the each label
            if word in self.gibbs:
                for i in self.gibbs[word]:
                    if self.gibbs[word][i] > mx:
                        mx = self.gibbs[word][i]
                        pred = i      
                        
            #Else, get the maximum initial prediction
            else:
                if count == 0:
                    for i in self.initial:
                        if self.initial[i] > mx:
                            mx = self.initial[i]
                            pred = i
                else:
                    for s in states:
                        if self.trans[prev][s] > mx:
                            mx = self.trans[prev][s]
                            pred = s
            count += 1        
            prev = pred
            solution.append(pred)
            
        return solution




    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

