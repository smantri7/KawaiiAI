#Code for LSTM
#Created by Shantanu Mantri on 3/20/2018
import sys
import numpy as np
import types
import tempfile
import keras.models
import random
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import TimeDistributed
from keras.layers import Activation
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import pickle
import csv
import re
import os

# Black Lagoon
# Angel Beats
# Devil May Cry
# FMA Brotherhood
# The Girl who leapt through time
# Gurren Lagann
# Hyouka
# K-On
# School Rumble
# Your lie in April
# The world god only knows
# Aiko

class ScriptGenerator:

    def __init__(self):
        name = "Nagisa"

    def train_model(self, filename, how, train=True, ep=1):
        self.train = train
        self.epochs = ep
        self.characters = set([])
        data = ""
        if how == "csv":
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=" ")
                next(reader, None)
                for row in reader:
                    if len(row) > 0:
                        data += row[2]
        elif how == "classic":
            f = open(filename, 'r', encoding='utf-8')
            raw_data = f.read()
            regex = re.compile("[A-Z]*[a-z]*:")
            for s in raw_data.splitlines():
                if s and regex.match(s):
                    #check if regex match for name
                    info = s.split(":")
                    data += info[-1]
                    self.characters.add(info[0])
                elif s:
                    data += s

        self.characters = list(self.characters)
            #data = os.linesep.join([s for s in data.splitlines() if s])

        chars = list(set(data))
        VOCAB_SIZE = len(chars)

        #easier to input numbers rather than text
        idx_to_char = {idx:char for idx,char in enumerate(chars)}
        char_to_idx = {char:idx for idx,char in enumerate(chars)}

        SEQ_LENGTH = 50

        #prepare input and output training
        X = np.zeros((int((len(data))/SEQ_LENGTH), SEQ_LENGTH, VOCAB_SIZE))
        y = np.zeros((int((len(data))/SEQ_LENGTH), SEQ_LENGTH, VOCAB_SIZE))

        for i in range(0, int(len(data)/SEQ_LENGTH)):
            X_sequence = data[i*SEQ_LENGTH:(i+1)*SEQ_LENGTH]
            X_sequence_idx = [char_to_idx[value] for value in X_sequence]
            input_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
            for j in range(SEQ_LENGTH):
                input_sequence[j][X_sequence_idx[j]] = 1
            X[i] = input_sequence

            y_sequence = data[i*SEQ_LENGTH+1:(i+1)*SEQ_LENGTH+1]
            y_sequence_idx = [char_to_idx[value] for value in y_sequence]
            target_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
            for j in range(SEQ_LENGTH):
                target_sequence[j][y_sequence_idx[j]] = 1
            y[i] = target_sequence

        #define and compile model
        HIDDEN_DIM = 700
        LAYER_NUM = 3

        if self.train:

            model = Sequential()
            model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True, dropout=0.24))
            for i in range(LAYER_NUM - 1):
                model.add(LSTM(HIDDEN_DIM, return_sequences=True))
            model.add(TimeDistributed(Dense(VOCAB_SIZE)))
            model.add(Activation('softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

            #train the model
            current = 1
            while current < self.epochs:
                model.fit(X, y, batch_size=50, verbose=1, epochs=1)
                current += 1
                #self.generate_text(150, idx_to_char, VOCAB_SIZE, model)
            #model.save_weights('weights/checkpoint_{}_epoch{}.hdf5'.format(HIDDEN_DIM, nb_epoch))
                if current % 5 == 0:
                    model.save("final" + "_" + str(current) + ".hdf5")

        #we want to save the following
        self.idx_to_char = idx_to_char
        self.char_to_idx = char_to_idx
        self.VOCAB_SIZE = VOCAB_SIZE
        self.HIDDEN_DIM = HIDDEN_DIM
        self.LAYER_NUM = LAYER_NUM
        self.SEQ_LENGTH = SEQ_LENGTH
        self.chars = chars


    def regenerate_model(self, filename):
        model = load_model(filename)
        return model

    def generate_text(self, length, idx_to_char, VOCAB_SIZE, model, X=None):
        idx = [np.random.randint(VOCAB_SIZE)]
        y_char = [idx_to_char[idx[-1]]]
        if X is None:
            X = np.zeros((1, length, VOCAB_SIZE))
        for i in range(length):
            X[0, i, :][idx[-1]] = 1
            print(idx_to_char[idx[-1]], end="")
            idx = np.argmax(model.predict(X[:, :i+1,:])[0], 1)
            y_char.append(idx_to_char[idx[-1]])
        return ('').join(y_char)

    def generate_script(self, lengths, idx_to_char, char_to_idx, VOCAB_SIZE, model, characters, size):
        f = open("script.txt", 'w', encoding='utf-8')
        for i in range(size):
            idx = [np.random.randint(VOCAB_SIZE)]
            y_char = [idx_to_char[idx[-1]]]
            length = np.random.randint(lengths[0], lengths[1])
            X = np.zeros((1, length , VOCAB_SIZE))
    
            for p in range(length):
                X[0, p, :][idx[-1]] = 1
                #print(idx_to_char[idx[-1]], end="")
                idx = np.argmax(model.predict(X[:, :p+1,:])[0], 1)
                y_char.append(idx_to_char[idx[-1]])

            sentence = ('').join(y_char)
            chop = max([sentence.rfind('.'), sentence.rfind("!"), sentence.rfind(",")])
            sentence = sentence[0:chop+1]
            character = random.choice(characters)
            complete = character + ": " + sentence
            f.write(complete + "\n\n")
        print("Completed Script!")


def save_generator(gen):
    pickle.dump(gen, open("gen.pkl", 'wb'))

def load_generator(filename):
    return pickle.load(open(filename, 'rb'))

#s = ScriptGenerator()
s = load_generator("gen.pkl")
print("loaded generator...")
model = s.regenerate_model("models/final_120.hdf5")
print("loaded model...")
s.generate_script([30, 200], s.idx_to_char, s.char_to_idx, s.VOCAB_SIZE, model, [random.choice(s.characters) for i in range(5)], 40)
#s.train_model("anime.txt", how="classic", train=True, ep=120)
#text = s.generate_text(150, s.idx_to_char, s.VOCAB_SIZE, model)
#save_generator(s)
