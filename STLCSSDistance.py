from Point import *
import datetime,time
import numpy as np
import os,re,sys
import goal_address

Distance=0.05
Time=10000
startTime1=0
startTime2=0
db = goal_address.connectdb()
num=0


def subcost(p1,p2):
    isSame = True
    for i in range(len(p1.dimension)):
        if (abs(p1.coordinate[i]-p2.coordinate[i]) > Distance):
            isSame=False

    if (abs((p1.timeLong - startTime1) - (p2.timeLong - startTime2)) > Time):
        isSame=False
    if (isSame):
        return 1
    return 0

def getSTLCSS(r, s):
    LCSSMetric=[]
    r_size=len(r)
    s_size=len(s)
    for i in range(r_size):
        LCSSMetric[i][0] = 0.0
    for i in range(s_size):
        LCSSMetric[0][i] = 0.0


    LCSSMetric[0][0] = 0

    for i in range(r_size-1):
        for j in range(s_size-1):
            if (subcost(r(i), s(j)) == 1):
                LCSSMetric[i+1][j+1] = LCSSMetric[i][j] + 1.0
            else:
                LCSSMetric[i+1][j+1] = max(LCSSMetric[i+1][j], LCSSMetric[i][j+1])


    lcss= LCSSMetric[r_size][s_size]

    distanceV=1-(lcss / min(r_size, s_size))

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

    f2=open("./time_need/"+path,'w')

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
            point=Point(getTime(time),)
            mid=[]
            mid=[getTime(time),goal]
            X1.append(mid)
        else:
            continue

    X.append(X1)
    f.close()
    f2.close()
    #os.remove("./line/" + path)



def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

X=[]

files=file_name("./file_for_time/")

for file in files:
    if(file!='.DS_Store'):
        load(file)

print(X[0])
print(X[1])
print(len(X))