import os
import numpy as np

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