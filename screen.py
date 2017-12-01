import numpy as np
import os,re
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
def check_exist(path,i):
    count = linecache.getline("./txt/"+path, i)
    check=True
    while(check):
        if count.strip() == '':
            return 0
        else:
            x = process_line(count)
            if(x):
                if(goal_address.check_goal(x,db)):
                    if(goal_address.check_verbs(x,db)):
                        return 1

        i+=1
        count = linecache.getline(path, i)

def load(path):
    f = open("./txt/"+path)

    f2=open("./screen_content/"+path,'w')
    type = 1#0为词向量行，1为地址行
    mid = []
    type_content = 1#判断目标地址在不在数据库，0就是在
    need_check=True#判断此条微博是否需要检查
    a=0
    need_write=0
    now_state=0#是否有词有地理位置
    for line in f:
        a+=1
        #判断是不是空行
        if line.strip() == '':
            type = 1
            need_check=True
            #判断地址存不存在的
            if type_content==0:
                if now_state==1:
                    f2.write('\n')
            continue
        #是否需要检查
        if(need_check):
            need_check=False
            now_state=check_exist(path,a+1)
            if(now_state):
                need_write=1
            else:
                continue
        #是否
        elif now_state!=1:

            continue



        if type == 1:
            goal = goal_address.search_goal(line.strip('\n').rstrip(),db)
            # Y.append(line.strip('\n').rstrip())
            if(goal!=0):

                type_content = 0
                f2.write(str(goal))
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
        # t = threading.Thread(target=load(file), name=file)
        # t.start()
        # t.join()
