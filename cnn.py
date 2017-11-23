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


nb_words = min(7000, len(X1))
embedding_matrix = np.zeros((nb_words + 1, 200))

# embedding_layer = Embedding(nb_words+1,
#                             200,
#                             input_length=920,
#                             weights=[embedding_matrix],
#                             trainable=True)

embedding_layer = Embedding(nb_words+1,
                            200,
                            input_shape=(100,200),
                            weights=[embedding_matrix],
                            trainable=True)
model_left = Sequential()
# model.add(Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32'))

# model_left.add(embedding_layer)
# model_left.add(Conv1D(200,12, activation='tanh'))
# model_left.add(MaxPooling1D(4))
# model_left.add(Conv1D(200, 28, activation='tanh'))
# model_left.add(MaxPooling1D(2))

# model_left.add(Conv1D(200, 5, activation='tanh'))
# model_left.add(MaxPooling1D(35))
#model_left.add(Flatten())
model_left.summary()

# model_right = Sequential()
# model_right.add(embedding_layer)
# model_right.add(Conv1D(128, 4, activation='tanh'))
# model_right.add(MaxPooling1D(4))
# model_right.add(Conv1D(128, 4, activation='tanh'))
# model_right.add(MaxPooling1D(4))
# model_right.add(Conv1D(128, 4, activation='tanh'))
# model_right.add(MaxPooling1D(28))
#model_right.add(Flatten())

# model_3 = Sequential()
# model_3.add(embedding_layer)
# model_3.add(Conv1D(200, 6, activation='tanh'))
# model_3.add(MaxPooling1D(3))
# model_3.add(Conv1D(200, 6, activation='tanh'))
# model_3.add(MaxPooling1D(3))
model_3 = Sequential()
model_3.add(embedding_layer)
model_3.add(Conv2D(200, 6, activation='tanh'))
model_3.add(MaxPooling2D(3))
model_3.add(Conv2D(200, 6, activation='tanh'))
model_3.add(MaxPooling2D(3))
# model_3.add(Conv1D(200, 6, activation='tanh'))
# model_3.add(MaxPooling1D(30))
model_3.add(Flatten())

model_3.summary()

# model_3 = Sequential()
# model_3.add(Conv1D(200, 3, activation='tanh',input_shape=(100,200)))
# model_3.add(MaxPooling1D(3))
# model_3.add(Conv1D(200, 3, activation='tanh'))
# model_3.add(MaxPooling1D(3))
# model_3.summary()

#merged = Merge([model_left,model_3],concat_axis=1)


#model.add(Dense(units=200,batch_input_shape=(32,100,200)))

model.add(model_3)

# model.add(Conv1D(200,
#                  2,
#                  padding='same',
#                  activation='relu',
#                  input_shape=(57,100)))


# model.add(Conv1D(200, 2,
#                         padding='causal',
#                  input_shape=(2,100,200))) # 卷积层1
#model.add(Activation('relu')) #激活层

#model.add(MaxPooling1D(pool_size=1)) #池化层
#model.add(Dropout(0.25))
#model.add(Flatten()) #拉成一维数据


#model.add(Reshape((100, 200)))
#model.add(Dense(1)) #全连接层1
model.add(Activation('relu')) #激活层
model.add(Dropout(0.5))
model.add(Dense(20000)) #全连接层2
model.add(Reshape((100, 200)))
model.add(Activation('softmax'))

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