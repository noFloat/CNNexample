from Point import *
import datetime,time,math
import numpy as np
import os,re,sys
import goal_address

Distance=0.1#0.1，0.15，0.05，0.01
Time=86400*0.5#0.5,1,1.5,2
similiarity=0.3#0.3-0.6
startTime1=0
startTime2=0
feature2=0.6
feature3=1-feature2

matrix_width=630#区域数

db = goal_address.connectdb()
num=0

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
    f = open("./file_for_time/"+path)
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

#预测feature2
def predict2(i):
    x1 = X[i]

    x_re = ReFridenship[i][1]
    x1_now = x1[int(len(x1) / 2):]  # 测试集

    len_x1 = int(len(x1_now))
    friend_num = len(x_re)

    rate_weibo = []
    rate_best = []
    for j in range(len_x1):
        l_pre = x1[int(len(x1) / 2) - 1 + j]  # 前一点
        point_now = [x1_now[j][0], [l_pre[1][0], l_pre[1][1]]]
        rate_each_weibo = []
        distance_each_weibo = []  # 每个微博的好友对应距离
        # 计算相似度
        for f in range(friend_num):
            x2_no = x_re[f]
            x2 = X[x2_no]
            len_x2 = len(x2)

            goal_x2 = search_same(point_now, x2)

            distance_each_weibo.append(goal_x2)



        sum_dist = 0
        for g in range(len(distance_each_weibo)):
            if distance_each_weibo[g][0] > 0:
                sum_dist += distance_each_weibo[g][0]
        max_rate_weibo = 0
        max_rate_weibo_id = -1

        for e in range(friend_num):

            if sum_dist == 0:
                rate_each_weibo.append(0)
            elif distance_each_weibo[e][0] == -1:
                rate_each_weibo.append(0)
            else:
                # if((1-distance_each_weibo[i][0]/sum_dist)*rate[x_re[i]][0]>0):
                now_ce_rate=(1 - distance_each_weibo[e][0] / sum_dist) * rate[i][x_re[e]]
                if  now_ce_rate > max_rate_weibo:

                    max_rate_weibo = now_ce_rate
                    max_rate_weibo_id = distance_each_weibo[e][1]


                rate_each_weibo.append(now_ce_rate)


        # 自己的第几条微博，相似度，谁的微博X的索引号，地区

        if len(rate_each_weibo) == 0:
            rate_best.append([])
            rate_weibo.append([])
        else:

            weibo_host = x_re[rate_each_weibo.index(max(rate_each_weibo))]
            if (max_rate_weibo_id == -1):
                area = -1
            else:
                area = X[weibo_host][max_rate_weibo_id][1][2]



            rate_best.append([int(len(x1) / 2) - 1 + j, max(rate_each_weibo), weibo_host, area])
            rate_weibo.append(rate_each_weibo)

    count = 0

    # 计算概率

    for m in range(len(x1_now)):

        if (len(rate_best[m]) == 0):
            continue
        if (x1_now[m][1][2] == rate_best[m][3]):

            count += 1

    return count / len(x1_now)

#预测第三个模块
def predict3(i):
    x1 = X[i]
    count=0
    x_re = ReFridenship[i][1]
    x1_now = x1[int(len(x1) / 2):]

    for j in range(len(x1_now)):
        l_pre = x1[int(len(x1) / 2) - 1+j]
        max_rate=max(Matrix[i][1][int(l_pre[1][2])])
        area=Matrix[i][1][int(l_pre[1][2])].index(max_rate)
        if(len(x1_now)==0):
            return 0.0
        if(x1_now[j][1][2]==area):
            count+=1

    return count / len(x1_now)

#预测feature2_3
def predict2_3(i):
    x1 = X[i]

    x_re = ReFridenship[i][1]
    x1_now = x1[int(len(x1) / 2):]  # 测试集

    len_x1 = int(len(x1_now))
    friend_num = len(x_re)
    rate_weibo = []
    rate_best = []
    for j in range(len_x1):
        l_pre = x1[int(len(x1) / 2) - 1 + j]  # 前一点
        point_now = [x1_now[j][0], [l_pre[1][0], l_pre[1][1]]]
        rate_each_weibo = []
        distance_each_weibo = []  # 每个微博的好友对应距离
        # 计算相似度
        for f in range(friend_num):
            x2_no = x_re[f]
            x2 = X[x2_no]
            len_x2 = len(x2)

            goal_x2 = search_same(point_now, x2)

            distance_each_weibo.append(goal_x2)



        sum_dist = 0
        for g in range(len(distance_each_weibo)):
            if distance_each_weibo[g][0] > 0:
                sum_dist += distance_each_weibo[g][0]
        max_rate_weibo = 0
        max_rate_weibo_id = -1

        for e in range(friend_num):

            if sum_dist == 0:
                rate_each_weibo.append([0,0])
            elif distance_each_weibo[e][0] == -1:
                rate_each_weibo.append([0,0])
            else:
                # if((1-distance_each_weibo[i][0]/sum_dist)*rate[x_re[i]][0]>0):
                now_ce_rate=(1 - distance_each_weibo[e][0] / sum_dist) * rate[i][x_re[e]]
                if  now_ce_rate > max_rate_weibo:

                    max_rate_weibo = now_ce_rate
                    max_rate_weibo_id = distance_each_weibo[e][1]

                now_weibo_host=x_re[e]

                rate_each_weibo.append([X[now_weibo_host][distance_each_weibo[e][1]][1][2],now_ce_rate])



        if len(rate_each_weibo) == 0:
            rate_weibo.append([])
        else:
            rate_weibo.append(rate_each_weibo)

    count = 0

    if (len(rate_each_weibo) == 0):
        return predict3(i)

    for j in range(len(x1_now)):
        matrix_now = Matrix

        l_pre = x1[int(len(x1) / 2) - 1 + j]
        for web_id in range(len(rate_weibo[0])):
            if rate_weibo[j][web_id][0]!=0:
                area_now_id=rate_weibo[j][web_id][0]
                origin_matrix_point=matrix_now[i][1][int(l_pre[1][2])][area_now_id]
                matrix_now[i][1][int(l_pre[1][2])][area_now_id]=rate_weibo[j][web_id][1]*feature2+origin_matrix_point*feature3

        max_rate=max(matrix_now[i][1][int(l_pre[1][2])])
        area=matrix_now[i][1][int(l_pre[1][2])].index(max_rate)

        if(x1_now[j][1][2]==area):
            count+=1

    return count / len(x1_now)


X=[]
Matrix=[]
ReFridenship=[]
Path=[]

files=file_name("./file_for_time/")
startTime=13502661600
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
    if len(re_mid[1])==0:
        os.remove("./file_for_time/" + Path[i])
    else:
        print(re_mid)
    #ReFridenship.append(re_mid)







