from Point import *
import datetime,time,math
import numpy as np
import os,re,sys
import goal_address

Distance=0.1#0.1，0.15，0.05，0.01
Time=86400*0.5#0.5,1,1.5,2 # bu ce le
similiarity=0.4#0.3-0.6
startTime1=0
startTime2=0
startTime=0
feature2=0.6
feature3=1-feature2

matrix_width=108#区域


db = goal_address.connectdb()
num=0
inputpath = './area_users_14/'


def eachfile(inputpath):
    pathDir = os.listdir(inputpath)
    filename_list = []
    for allDir in pathDir:
        child = allDir
        filename_list.append(child)
    return filename_list


for file_floder in eachfile(inputpath):

    if file_floder=='.DS_Store':
        continue

    path_1 = inputpath+file_floder+'/'

    def getLen(p1,p2):
    #
    # p1_len=len(p1)
    # p2_len = len(p2)

        if isinstance(p1,list):
            x = p1[1][0] - p2[1][0]
            y = p1[1][1] - p2[1][1]
            len_now = math.sqrt(x ** 2 + y ** 2)
            return len_now
        else:
            return -1


    def subcost(p1,p2):
        isSame = True
        if(abs(getLen(p1,p2))<0):
            isSame = False

        if (abs(getLen(p1,p2)) > Distance):
            isSame=False

        if (abs(p1[0]-p2[0]) > Time):
            isSame=False
        if (isSame):
            return 1
        return 0

    def getSTLCSS(r, s):

        r_size=int(len(r)/2)
        s_size=int(len(s)/2)
        LCSSMetric = [[0 for col in range(s_size+1)] for row in range(r_size+1)]
        # for i in range(s_size):
        #     LCSSMetric[0].append(0)
        # for i in range(r_size):
        #     LCSSMetric[i][0]=0
        #
        # print(LCSSMetric[0])
        # LCSSMetric[0][0] = 0
        # print(LCSSMetric[0][0])

        for i in range(1,r_size):
            for j in range(1,s_size):
                goal=subcost(r[i-1], s[j-1])
                if ( goal== 1):

                    LCSSMetric[i][j] =  LCSSMetric[i-1][j-1]+ 1

                else:
                    LCSSMetric[i][j] = max(LCSSMetric[i][j-1], LCSSMetric[i-1][j])
                #print(str(i)+'    '+str(j)+'    '+str(LCSSMetric[i][j])+'   '+str(LCSSMetric[0][1]))




        lcss= LCSSMetric[r_size-1][s_size-1]
        if min(r_size, s_size) == 0:
            return 0.0
        distanceV=lcss / min(r_size, s_size)
        if distanceV>1:
            print(str(lcss)+'  '+str(r_size)+'   '+str(s_size))
        return distanceV


    def getTimeEnd(r,s):

        goal_s=s[-1].timeLong
        goal_r=r[-1].timeLong

        if goal_s<goal_r:
            tn=goal_s
        else:
            tn=goal_r
        return tn

    def getTime(a):
        a=a.rstrip()
        b=str(datetime.datetime.strptime(a, "%b %d %Y %I:%M%p"))
        timeArray = time.strptime(b, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        return timestamp


    def load(path):
        f = open(path_1+path)
        print(path)
        X1=[]
        matrix = [path]
        for line in f:
            time_need=line.split()
            i=0
            time=''
            location=''
            for word in time_need:
                if i==4:
                    location=word
                elif i>4:
                    break
                else:
                    time += word
                    time+=' '
                i += 1
            location = location.split('。')
            location = location[0]
            goal = goal_address.search_goal(location, db)

            if (goal != 0):
                timestamp=getTime(time)
                global  startTime
                if(timestamp<startTime):
                    startTime=timestamp
                mid=[]
                mid=[getTime(time),goal]
                X1.append(mid)
            else:
                continue

        if len(X1)==0:
            return

        Path.append(path)
        X.append(X1)
        f.close()
        #f2.close()
        #os.remove("./line/" + path)



    def file_name(file_dir):
        for root, dirs, files in os.walk(file_dir):
            return files

    def search_same(x1_point,x2):
        goal=0
        minus_len=5
        #print(x2)
        for i in range(len(x2)):
            now_len=getLen(x2[i],x1_point)
            if(now_len!=-1)&(now_len<minus_len)&subcost(x1_point,x2[i]):
                minus_len=now_len
                goal=i

            return [getLen(x1_point,x2[goal]),goal]
        else:
            return [-1,0]




    X=[]
    Matrix=[]
    ReFridenship=[]
    Path=[]

    files=file_name(path_1)
    for file in files:
        if(file!='.DS_Store'):
            load(file)


    rate=[[0 for col in range(len(X))] for row in range(len(X))]



    for i in range(len(X)):
        re_mid=[i,[]]
        for num_now in range(len(X)):
            startTime1=X[i][0][0]
            startTime2=X[num_now][0][0]
            now=getSTLCSS(X[i],X[num_now])
            if (now>similiarity)&(num_now!=i):
                re_mid[1].append(num_now)
                #print(str(i) + '    ' + str(num_now) + '    ' + str(now))

            if num_now==i:
                rate[i][num_now] = 1.0
            else:
                rate[i][num_now] = now
        if len(re_mid[1]) == 0:
            os.remove(inputpath+file_floder+'/' + Path[i])
            print(inputpath+file_floder+'/' + Path[i])







