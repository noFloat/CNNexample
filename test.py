from __future__ import print_function
import os
import numpy as np

np.random.seed(1337)

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Input, Flatten
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras.optimizers import *
from keras.models import Sequential
from keras.layers.merge import add
import sys


MAX_SEQUENCE_LENGTH = 200  # 每个文本的最长选取长度，较短的文本可以设短些
MAX_NB_WORDS = 20000  # 整体词库字典中，词的多少，可以略微调大或调小



VALIDATION_SPLIT = 0.4  # 这里用作是测试集的比例，单词本身的意思是验证集

# first, build index mapping words in the embeddings set
# to their embedding vector  这段话是指建立一个词到词向量之间的索引，比如 peking 对应的词向量可能是（0.1,0,32,...0.35,0.5)等等。

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


x_train=X[:int(len(X)/2)]
x_val=X[int(len(X)/2)+1:]
y_train =X[:int(len(Y)/2)]
y_val=X[int(len(Y)/2)+1:]
f.close()


nb_words = min(MAX_NB_WORDS, len(x_train))
embedding_matrix = np.zeros((nb_words + 1, 60))
embedding_layer = Embedding(nb_words + 1,
                            60,
                            input_length=MAX_SEQUENCE_LENGTH,
                            weights=[embedding_matrix],
                            trainable=True)

print('Training model.')

# train a 1D convnet with global maxpoolinnb_wordsg

# left model 第一块神经网络，卷积窗口是5*50（50是词向量维度）
model_left = Sequential()
# model.add(Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32'))
model_left.add(embedding_layer)
model_left.add(Conv1D(128, 5, activation='tanh'))
model_left.add(MaxPooling1D(5))
model_left.add(Conv1D(128, 5, activation='tanh'))
model_left.add(MaxPooling1D(5))
model_left.add(Conv1D(128, 5, activation='tanh'))
model_left.add(MaxPooling1D(35))
model_left.add(Flatten())

# right model <span style="font-family: Arial, Helvetica, sans-serif;">第二块神经网络，卷积窗口是4*50</span>

model_right = Sequential()
model_right.add(embedding_layer)
model_right.add(Conv1D(128, 4, activation='tanh'))
model_right.add(MaxPooling1D(4))
model_right.add(Conv1D(128, 4, activation='tanh'))
model_right.add(MaxPooling1D(4))
model_right.add(Conv1D(128, 4, activation='tanh'))
model_right.add(MaxPooling1D(28))
model_right.add(Flatten())

model_3 = Sequential()
model_3.add(embedding_layer)
model_3.add(Conv1D(128, 6, activation='tanh'))
model_3.add(MaxPooling1D(3))
model_3.add(Conv1D(128, 6, activation='tanh'))
model_3.add(MaxPooling1D(3))
model_3.add(Conv1D(128, 6, activation='tanh'))
model_3.add(MaxPooling1D(30))
model_3.add(Flatten())

#merged = add([model_left, model_right, model_3], mode='concat')

model = Sequential()
model.add(model_left)  # add merge
model.add(Dense(128, activation='tanh'))  # 全连接层
model.add(Dense( units=len(x_train),activation='softmax'))  # softmax，输出文本属于20种类别中每个类别的概率

# 优化器我这里用了adadelta，也可以使用其他方法
model.compile(loss='categorical_crossentropy',
              optimizer='Adadelta',
              metrics=['accuracy'])
model.summary()
print(len(y_train))
model.fit(x_train, y_train, epochs=3)

score = model.evaluate(x_train, y_train, verbose=0)
print('train score:', score[0])
print('train accuracy:', score[1])
score = model.evaluate(x_val, y_val, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])