import numpy as np
import sys
import keras
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.layers import Dense, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from keras.preprocessing import sequence
from keras.utils.np_utils import to_categorical
np.random.seed(1337)
path='1.txt'
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

f = open(path)
X = []
Y = []
type=1
mid=[]
list = [0.0 for i in range(200)]

for line in f:

    if line.strip()=='':
        type=1
        for i in range(50-len(mid)):
            mid.append(list)
        X.append(mid)
        mid=[]
        continue


    if type==1:
        Y.append(line.strip('\n').rstrip())
        type=0
    else:
        x=process_line(line)
        mid.append(x)


X1=X[:int(len(X)/2)]
X2=X[int(len(X)/2)+1:]
Y1=X[:int(len(Y)/2)]
Y2=X[int(len(Y)/2)+1:]
X1 = np.array(X1)
Y1 = np.array(Y1)
X2 = np.array(X2)
Y2 = np.array(Y2)

print(len(X1[0][0]))
print(X1[1][0])
print(X1[1][48])
print(len(X1[1][48]))

X1=X1.reshape(len(X1),1)
X2=X2.reshape(len(X2),1)
Y1=Y1.reshape(len(Y1),1)
Y2=Y2.reshape(len(Y1),1)

f.close()
model = Sequential()
# kernel_size = (3,3)
# embedding_layer = Embedding(len(X1) + 1,
#                             60,
#                             input_length=1000,
#                             trainable=True)
# model.add(embedding_layer)
model.add(Dense(units=len(X1),batch_input_shape=(57,1)))
model.add(Activation('relu'))
#model.add(Flatten())
model.add(Dense(1))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
                         optimizer='sgd',
                         metrics=['accuracy'])
model.compile(loss=keras.losses.sparse_categorical_crossentropy,
                         optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))
model.summary()
model.fit(X1,Y1,epochs=1, batch_size=64)
#
loss_and_metrics=model.evaluate(X2,Y2,batch_size=64)
print(loss_and_metrics)