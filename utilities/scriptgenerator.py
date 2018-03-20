#Code for LSTM
#Created by Shantanu Mantri on 3/20/2018
import sys
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
class ScriptGenerator:

    def __init__(self, filename):
        raw_text = open(filename, 'r').read()
        raw_text.strip()
        raw_text = raw_text.split(" ")
        vocab = sorted(list(set(raw_text)))
        char_to_int = dict((c, i) for i, c in enumerate(vocab))
        int_to_char = dict((i, c) for i, c in enumerate(vocab))
        num_chars = len(raw_text)
        num_vocab = len(vocab)

        #what size you want
        seq_length = 200
        dataX = []
        dataY = []
        for i in range(0, num_chars - seq_length, 1):
            seq_in = raw_text[i:i + seq_length]
            seq_out = raw_text[i + seq_length]
            dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
        n_patterns = len(dataX)
      
        # reshape X to be [samples, time steps, features]
        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        # normalize
        X = X / float(num_vocab)
        # one hot encode the output variable
        y = np_utils.to_categorical(dataY)

        # define the LSTM model
        model = Sequential()
        model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(256))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        # load the network weights
        filename = "weights-improvement-47-1.2219-bigger.hdf5"
        model.load_weights(filename)
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        # pick a random seed
        start = numpy.random.randint(0, len(dataX)-1)
        pattern = dataX[start]

        # generate characters
        for i in range(1000):
            print("hi")
            x = numpy.reshape(pattern, (1, len(pattern), 1))
            x = x / float(num_vocab)
            prediction = model.predict(x, verbose=0)
            index = numpy.argmax(prediction)
            result = int_to_char[index] + " "
            seq_in = [int_to_char[value] for value in pattern]
            sys.stdout.write(result)
            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        print("DONE")

s = ScriptGenerator("test.txt")