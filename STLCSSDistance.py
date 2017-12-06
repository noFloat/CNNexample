from Point import *
import datetime,time,math
import numpy as np
import os,re,sys
import goal_address

Distance=0.1
Time=86400*2
startTime1=0
startTime2=0
db = goal_address.connectdb()
num=0

def getLen(p1,p2):
    x=p1[1][0]-p2[1][0]
    y = p1[1][1] - p2[1][1]
    len=math.sqrt(x**2+y**2)
    return len

def subcost(p1,p2):
    isSame = True


    if (abs(getLen(p1,p2)) > Distance):
        isSame=False

    if (abs((p1[0] - startTime1) - (p2[0] - startTime2)) > Time):
        isSame=False
    if (isSame):
        return 1
    return 0

def getSTLCSS(r, s):

    r_size=len(r)
    s_size=len(s)
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
    distanceV=lcss / min(r_size, s_size)
    if distanceV>1:
        print(str(lcss)+'  '+str(r_size)+'   '+str(s_size))
    return distanceV
def getDistance( r, s):

        Time = getTimeEnd(r, s)
        startTime1 = r[0].timeLong
        startTime2 = s[0].timeLong
        return getSTLCSS(r, s)

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
    f = open("./file_for_time/"+path)

    X1=[]

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

        goal = goal_address.search_goal(location, db)

        if (goal != 0):
            timestamp=getTime(time)
            global  startTime
            if(timestamp<startTime):
                startTime=timestamp
            point=Point(timestamp,)
            mid=[]
            mid=[getTime(time),goal]
            X1.append(mid)
        else:
            continue

    if len(X1)==0:
        return
    X.append(X1)
    f.close()
    f2.close()
    #os.remove("./line/" + path)



def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files



X=[]

files=file_name("./file_for_time/")
startTime=13502661600
for file in files:
    if(file!='.DS_Store'):
        print(file)
        load(file)


rate=[[0 for col in range(len(X))] for row in range(len(X))]



for i in range(len(X)):

    for num_now in range(i+1,len(X)):
        startTime1=X[i][0][0]
        startTime2=X[num_now][0][0]
        now=getSTLCSS(X[i],X[num_now])
        print(str(i) + '    ' + str(num_now)+'    '+str(now))
        rate[i][num_now]=now



