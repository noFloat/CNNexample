import numpy as np
import os
import theano
import sys
import keras
from keras.layers.core import  Reshape,RepeatVector,Dropout
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import *
from keras.layers.merge import add,Add
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.utils.np_utils import to_categorical
import goal_address
np.random.seed(1337)
path='1.txt'
db = goal_address.connectdb()


def file_name(file_dir):
         for root, dirs, files in os.walk(file_dir):
             return files

def process_line(line):
    lineSpilt = line.split(' ',1)
    goalLine=lineSpilt[1]
    tmp = [float(val) for val in goalLine.strip('\n').rstrip().split(' ')]
    x = np.array(tmp[0:])
    for i in(range(100-len(x))):
        x.append(0)
    # print(x)
    #sys.exit()
    return tmp
X = []
Y = []



def load(path):
    f = open("./new_content/"+path)
    type = 1
    mid = []
    list = [0.0 for i in range(200)]

    for line in f:

        if line.strip() == '':
            type = 1
            for i in range(100 - len(mid)):
                mid.append(list)
            X.append(mid)
            mid = []
            continue

        if type == 1:
            Y.append(line.strip('\n').rstrip())
            type = 0
        else:
            x = process_line(line)
            mid.append(x)

    f.close()

files=file_name("./new_content/")
for file in files:
    if(file!='.DS_Store'):
        load(file)
X1=X[:int(len(X)/2)]

X2=X[int(len(X)/2)+1:]
Y1=X[:int(len(Y)/2)]
Y2=X[int(len(Y)/2)+1:]
X1 = np.array(X1)
Y1 = np.array(Y1)
X2 = np.array(X2)
Y2 = np.array(Y2)



X1=X1.reshape(len(X1),100,200)
X2=X2.reshape(len(X2),100,200)

model = Sequential()

batch_size = 128
nb_classes = 10
epochs = 12
# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 200
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size

model.add(Dense(units=200,batch_input_shape=(32,100,200)))
model.add(Conv1D(200,
                 2,
                 padding='same',
                 activation='relu',
                 input_shape=(57,100)))


# model.add(Conv1D(200, 2,
#                         padding='causal',
#                  input_shape=(2,100,200))) # 卷积层1
model.add(Activation('relu')) #激活层

model.add(MaxPooling1D(pool_size=1)) #池化层
model.add(Dropout(0.25))
model.add(Flatten()) #拉成一维数据
model.summary()
model.add(Reshape((100, 200)))
#model.add(Dense(1)) #全连接层1
model.add(Activation('relu')) #激活层
model.add(Dropout(0.5))
model.add(Dense(200)) #全连接层2
model.add(Activation('softmax'))

# model.add(Dense(units=200,batch_input_shape=(57,100,200)))
#
model.summary()
#
#
#
# model.add(Activation('linear'))
# #
# model.add(Flatten())
# #
# model.add(Reshape((100, 200)))
# #model.add(Dense(1))
# model.add(Activation('linear'))

model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])

# model.compile(loss='mean_squared_error',
#                           optimizer=keras.optimizers.Adadelta())
model.fit(X1,Y1,epochs=1, batch_size=32)
#
loss, accuracy = model.evaluate(X2, Y2)

print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)