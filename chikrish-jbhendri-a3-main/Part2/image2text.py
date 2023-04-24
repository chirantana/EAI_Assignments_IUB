#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: chikrish and jbhendri
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

class Vision:
    E = pow(10, -50)
    trans = {}
    initial = {}
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    emission = []

    def train(self, data, train_letter):

        for let in self.TRAIN_LETTERS:
            self.initial[let] = self.E
            self.trans[let] = {}
            for let2 in self.TRAIN_LETTERS:
                self.trans[let][let2] = self.E
        
        #Learn the relationship between each letter in the sentenece
        for sentence in data:
            count = 0
            prev_letter = None
            for letter in sentence:
                
                if count == 0:
                    if letter in self.initial:
                        self.initial[letter] += 1
                        self.initial[letter.upper()] += 1
                
                if count > 0:
                    if (letter in self.trans) & (prev_letter in self.trans):
                        self.trans[prev_letter][letter] += 1
                        self.trans[prev_letter.upper()][letter.upper()] += 1
                        self.trans[prev_letter.upper()][letter] += 1
                        self.trans[prev_letter][letter.upper()] += 1

                prev_letter = letter
                count += 1

        #Normalize initial
        mnv = min(self.initial.values())
        mxv = max(self.initial.values())
        for val in self.initial:
            self.initial[val] = (((self.initial[val] - mnv) / (mxv - mnv + self.E)) * 0.05) + 0.5

        #Normaize transition
        for t in self.trans:
            mnv = min(self.trans[t].values())
            mxv = max(self.trans[t].values())
            for val in self.trans[t]:
                self.trans[t][val] = (((self.trans[t][val] - mnv) / (mxv - mnv + self.E)) * 0.05) + 0.5

        self.emission = train_letter


    def simplified(self, image):
        
        solution = ""
        count = 0
        for letter in image:
            mx = 0
            pred = ""

            letter_prob = self.get_emissions(letter)

            #predict the value that comes from the max of emission and initial tables for each label
            for letter in self.TRAIN_LETTERS:
                if count == 0:
                    
                    if letter_prob[letter] * self.initial[letter] > mx:
                        mx = letter_prob[letter] * self.initial[letter]
                        pred = letter
                else:
                    if letter_prob[letter]  > mx:
                        mx = letter_prob[letter] 
                        pred = letter
                        
            solution += pred
            count += 1
            
        return solution

    def hmm_viterbi(self, image):
        
        #Initialize tables
        N = len(image)

        V_table = {}
        for let in self.TRAIN_LETTERS:
            V_table[let] = [0] * N

        which_table = {}
        for let in self.TRAIN_LETTERS:
            which_table[let] = [0] * N

        viterbi_seq = [""] * N
        

        #Set beginning of each table
        letter = image[0]
        letter_prob = self.get_emissions(letter)
        for sample in self.emission:
            V_table[sample][0] = self.initial[sample] * letter_prob[sample]
            
        #Use viterbi to fill out the rest of the tables
        k = 0
        count = 0
        for k in range(1,N):
            letter = image[k]
            letter_prob = self.get_emissions(letter)

            
            for letter in self.TRAIN_LETTERS:
                V_table[letter][k] = letter_prob[letter]

                #Find the valuesof each state that can be next
                mx = -1
                best_pos = ''
                for nxt in self.TRAIN_LETTERS:
                    if V_table[nxt][k-1] * self.trans[nxt][letter] > mx:
                        mx = V_table[nxt][k-1] * self.trans[nxt][letter]
                        best_pos = nxt
                V_table[letter][k] *= mx
                which_table[letter][k] = best_pos

        #Find the maximum end value and use it as th most likely ending position
        max_end = -1
        best_pos = ''
        for nxt in self.TRAIN_LETTERS:
            if V_table[nxt][k] > max_end:
                max_end = V_table[nxt][k]
                best_pos = nxt
        viterbi_seq[N-1] = best_pos    
              
        #Work backward from the end position through the table
        for i in range(N-2, -1, -1):
            viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]
            
        # #Return most likely sequence
        solution = ''
        for vit in viterbi_seq:
            solution += vit
        return solution

    #Get the emission values by using a Naive Bayes Classifyer to handle comparisons
    def get_emissions(self, letter):
        letter_prob = {}
        for let in self.TRAIN_LETTERS:
            letter_prob[let] = 0

        for sample in self.emission:
            total = 0
            score = 0
            for i in range(len(letter)):
                for j in range(len(letter[0])):
                    total += 1
                    if (letter[i][j] == self.emission[sample][i][j]) & (letter[i][j] == '*'):
                        score +=1
                    elif (letter[i][j] == self.emission[sample][i][j]) & (letter[i][j] == ' '):
                        score +=0.2
            letter_prob[sample] = score / total
        return letter_prob

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

# Read in training or test data file
#
def read_data(fname = 'bc.train'):
    exemplars = []
    file = open(fname, 'r');
    count = 0
    all_data = []
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [ (data[0::2], data[1::2]), ]

        sentence = ''
        for word in exemplars[count][0]:
            sentence += word + " "

        all_data.append(sentence)
        count += 1
    return all_data

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)


#Call the function and the class that are written above
data = read_data()

vision = Vision()
vision.train(data, train_letters)

simple_pred = vision.simplified(test_letters)
hmm_pred = vision.hmm_viterbi(test_letters)


# The final two lines of your output should look something like this:
print("Simple: " + simple_pred)
print("   HMM: " + hmm_pred) 


