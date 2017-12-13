import numpy as np
import os,re,sys
import threading
import goal_address
import linecache
np.random.seed(1337)
path='1.txt'
db = goal_address.connectdb2()


def file_name(file_dir):
         for root, dirs, files in os.walk(file_dir):
             return files

def process_line(line):
    lineSpilt = line.split(' ',1)


    str1="[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+"
    str2=""
    string = re.sub(str1, str2, lineSpilt[0])


    if(string!=''):
        return lineSpilt[0]
        goalLine=lineSpilt[1]
        tmp = [float(val) for val in goalLine.strip('\n').rstrip().split(' ')]
        x = np.array(tmp[0:])
        for i in(range(100-len(x))):
            x.append(0)

        #sys.exit()
        return tmp
    else:
        return False

#判断是否需要爬取
def check_exist(count):
    check=True
    if count.strip() == '':
        return 0
    else:
        if(goal_address.check_goal(count,db)):
            if(goal_address.check_verbs(count,db)):
                return 1


def load(path):
    f = open("../screen_content/"+path)



    state=0
    print(path)

    for line in f:


        state=0
        words=line.split(' ',1)
        f2 = open("../data_dividedby_area/" + words[0]+'.txt', 'a')

        now_str=path+'||| '+words[1]
        f2.write(now_str)
        f2.close()

    f.close()

    os.remove("../screen_content/" + path)

files=file_name("../screen_content/")



for file in files:
    if(file!='.DS_Store'):
        load(file)
        # t = threading.Thread(target=load(file), name=file)
        # t.start()
        # t.join()
