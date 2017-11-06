import numpy as np
import sys
import keras
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam

path='1.txt'
def process_line(line):
    lineSpilt = line.split(' ',1)
    goalLine=lineSpilt[1]
    tmp = [float(val) for val in goalLine.strip('\n').rstrip().split(' ')]
    x = np.array(tmp[0:])
    # print(x)
    # sys.exit()
    return tmp

f = open(path)
X = []
Y = []
type=1
for line in f:

    if line.strip()=='':
        type=1
        continue


    if type==1:
        Y.append(line.strip('\n').rstrip())
        type=0
    else:
        x=process_line(line)
        X.append(x)



f.close()
model = Sequential()

model.add(Dense(units=len(X), input_dim=115))
model.add(Activation('relu'))
#model.add(Dense(units=115,input_dim=1))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
                         optimizer='sgd',
                         metrics=['accuracy'])
model.compile(loss=keras.losses.categorical_crossentropy,
                         optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))

# model.fit(X,Y,epochs=1252,batch_size=200)
#
# loss_and_metrics=model.evaluate(X,Y,batch_size=128)