# -*- coding: utf-8 -*-
import numpy as np
import os, string, re
import theano
import sys
import keras
from keras.layers.core import Reshape, RepeatVector, Dropout
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping

# import goal_address
np.random.seed(1337)
path = '/home/liwenjie/liurong/wordvec/data/10km.txt'
# db = goal_address.connectdb()

pattern = re.compile('P')
category=33

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def process_line(line):
    tmp = line.strip('\n').rstrip().split(',')
    return tmp
    sys.exit()
    lineSpilt = line.split(' ', 1)
    str1 = "[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
    str2 = ""
    string = re.sub(str1, str2, lineSpilt[0])

    if (line != ''):

        goalLine = line
        tmp = [float(val) for val in goalLine.strip('\n').rstrip().split(' ')]
        x = np.array(tmp[0:])
        for i in (range(100 - len(x))):
            x.append(0)

        # sys.exit()
        return tmp
    else:
        return 0


X = []
Y = []


def load(path):
    f = open(path)
    type = 1
    mid = []
    list = [0.0 for i in range(60)]
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
            if (x != 0):
                mid.append(x)
    f.close()


# files = file_name("data/")
files = [path]
for file in files:
    if (file != '.DS_Store'):
        load(file)

X1 = X[:int(len(X) * 0.8)]
X2 = X[int(len(X) * 0.8):]
Y1 = Y[:int(len(Y) * 0.8)]
Y2 = Y[int(len(Y) * 0.8):]
X1 = np.array(X1)
X2 = np.array(X2)

X1 = X1.reshape(len(X1), 100, 60)
X2 = X2.reshape(len(X2), 100, 60)
Y1 = keras.utils.to_categorical(Y1, category)
Y2 = keras.utils.to_categorical(Y2, category)

nb_words = min(7000, len(X1))
embedding_matrix = np.zeros((nb_words + 1, 60))
embedding_layer = Embedding(nb_words + 1,
                            60,
                            input_shape=(100, 60),
                            weights=[embedding_matrix],
                            trainable=True)
print('Training model.')

model = Sequential()
# model.add(Dense(units=200, input_shape=(100, 60)))
model.add(Conv1D(60,
                 3,
                 padding='same',
                 activation='tanh',
                 input_shape=(100, 60)
                 ))
model.add(MaxPooling1D(pool_size=2))  # 池化层
model.add(Dropout(0.25))
model.add(Conv1D(60,
                 2,
                 padding='same',
                 activation='tanh',
                 ))
model.add(MaxPooling1D(pool_size=2))  # 池化层
model.add(Activation('relu'))  # 激活层
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(category, activation='softmax'))  # 全连接层2
model.summary()
sgd = keras.optimizers.SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
early_stopping = EarlyStopping(monitor='val_loss', patience=2)

tbCallBack = keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

model.fit(X1, Y1, epochs=50, batch_size=32, callbacks=[tbCallBack])

loss, accuracy = model.evaluate(X2, Y2)
classes = model.predict_classes(X2, batch_size=32) #5预测模型
proba = model.predict_proba(X2, batch_size=32)
print('\ntest loss: ', loss)
print('\ntest accuracy: ', accuracy)
