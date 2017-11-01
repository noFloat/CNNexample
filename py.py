import numpy as np
import sys
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





