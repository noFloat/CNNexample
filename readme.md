#CNN初探-待续

##坐标差距
在经线上，纬度每差1度,实地距离大约为111千米；
在纬线上，经度每差1度,实际距离为111×cosθ千米
上海市地处东经120度51分至122度12分，北纬30度40分至31度53分之间
所以取31度 范围500m 所以纬度差约为0.005 经度 0.004
数据处理按此划分
清理非法数据后 y范围22.58287029-49.2678 x 范围 129.436712-104.07772
##
最小x 120.229161 最大x 129.436712
最小y 29.15216  最大y 45.828799

##配置
    mysql.conf.copy换成mysql.conf并配置数据库账号密码
    get_content只替换地址
    screen替换地址和动词

##说明
* goal_address.py有处理方法(包括数据库处理)goal_address.search_goal2 返回位置 search_goal 返回x,y,location
* getContent.py获取文件

#getStlccsdistance
    使用不同范围的时候要把goal_address.py的search_goal()方法里的163行表名换成对应的表，同时全局变量matrix_width换成对应表的行数(区域数)