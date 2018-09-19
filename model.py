import csv
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
import sys
import re
import numpy
import pandas

# By Aditya Parmar

data = pandas.read_csv('lyricsData.csv')

giantLyricsList = ""

for index, row in data['lyrics'].iteritems():
    giantLyricsList = giantLyricsList + str(row).lower()
    
uniqueList = list(set(giantLyricsList))
uniqueList = sorted(uniqueList)

ctiDict = dict((c,i) for i,c in enumerate(uniqueList))
itcDict = dict((i,c) for i,c in enumerate(uniqueList))


seqLength = 30

sequences = []
predicted = []

textLen = len(giantLyricsList)

for i in range(0, textLen - seqLength, 1):
    sequences.append(giantLyricsList[i:i+seqLength])
    predicted.append(giantLyricsList[i+seqLength])


x = numpy.zeros((len(sequences), seqLength, len(uniqueList)), dtype=numpy.bool)
y = numpy.zeros((len(sequences), len(uniqueList)), dtype=numpy.bool)

for s, sequence in enumerate(sequences):
    for c, char, in enumerate(sequence):
        x[s, c, ctiDict[char]] =1 
    y[s,ctiDict[predicted[s]]] = 1

# THE MODEL

model = Sequential()

model.add(LSTM(128, input_shape=(seqLength,len(uniqueList))))
model.add(Dense(len(uniqueList)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop')

model.summary()


saved_model = model.fit(x,y,batch_size=128,epochs=10)


looper = "yes"
while looper == "yes":
    u_input = input("Hi there. Write your 30 letter seed, and use quotes: ")

    seed = u_input.lower()
    res = seed

    sys.stdout.write("\n Here goes: \n\n")

    sys.stdout.write(seed)

    for i in range(360):

        xPredicted = numpy.zeros((1,seqLength,len(uniqueList)))
        for c, char in enumerate(seed):
            if char != '0':
                xPredicted[0, c, ctiDict[char]] = 1
        
        preds = model.predict(xPredicted, verbose=0)[0]
        # nextInd 
        preds = numpy.asarray(preds).astype('float64')
        preds = numpy.log(preds) / 0.2
        preds = numpy.exp(preds) / numpy.sum(numpy.exp(preds))
        probabilities = numpy.random.multinomial(1, preds, 1)
        nextInd = numpy.argmax(probabilities)

        nextChar = itcDict[nextInd]
        res = res + nextChar
        seed = seed[1:] + nextChar

        sys.stdout.write(nextChar)
        sys.stdout.flush()
    print()
    looper = input("print yes if you want to keep going")


