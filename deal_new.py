import numpy as np
import os
import theano
import sys
import keras
import goal_address
np.random.seed(1337)
path='1.txt'
db = goal_address.connectdb()


def file_name(file_dir):
         for root, dirs, files in os.walk(file_dir):
             return files

def load(path):
    f = open("./txt/"+path)

    f2=open("./new_content/"+path,'w')
    type = 1
    mid = []
    list = [0.0 for i in range(200)]
    type_content = 0
    for line in f:

        if line.strip() == '':
            type = 1

            if type_content==0:
                f2.write('\n')
            continue

        if type == 1:
            goal = goal_address.search_goal(line.strip('\n').rstrip(),db)
            # Y.append(line.strip('\n').rstrip())
            if(goal!=0):

                type_content = 0
                f2.write(goal)
                f2.write('\n')
            else:
                type_content = 1
            type = 0

        elif type_content==0:
            f2.write(line)
    f.close()
    f2.close()
files=file_name("./txt/")
for file in files:
    if(file!='.DS_Store'):
        load(file)
