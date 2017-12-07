import numpy as np
import os,re,sys
import threading
import goal_address
import linecache
np.random.seed(1337)
path='1.txt'
db = goal_address.connectdb()


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
    f = open("./line/"+path)

    f2=open("./screen_content/"+path,'w')

    state=0
    print(path)

    for line in f:

        state=0
        words=line.split(' ',1)
        now_str=''
        type_content = 0
        now_state = 0
        if(True):
            goal = goal_address.search_goal2(words[0], db)
            state = 1
            if (goal != 0):
                type_content = 1
                now_str+=str(goal)

            else:
                type_content=0
                continue
            now_words = words[1].strip('\n').rstrip().split()
            now_state=0
            for now_word in now_words:
                now_str+=' '
                now_str+=now_word
                check_now=check_exist(now_word)
                if(check_now==1):
                    now_state=1


        if(type_content==1&now_state==1):
            now_str += '\n'
            f2.write(now_str)

    f.close()
    f2.close()
    os.remove("./line/" + path)
files=file_name("./line/")



for file in files:
    if(file!='.DS_Store'):
        load(file)
        # t = threading.Thread(target=load(file), name=file)
        # t.start()
        # t.join()
