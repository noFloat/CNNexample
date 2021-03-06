import pymysql
import configparser
import sys
import linecache

def connectdb():
    conf = configparser.ConfigParser()
    conf.read("./mysql.conf")
    name = conf.get("mysql", "name")
    password = conf.get("mysql", "password")
    dbname = conf.get("mysql", "dbname")
    db = pymysql.connect(host="127.0.0.1", port=3306, user=name, passwd=password, db=dbname, charset='utf8mb4')
    #db.set_character_set('utf8mb4')
    return db
def connectdb2():
    conf = configparser.ConfigParser()
    conf.read("../mysql.conf")
    name = conf.get("mysql", "name")
    password = conf.get("mysql", "password")
    dbname = conf.get("mysql", "dbname")
    db = pymysql.connect(host="127.0.0.1", port=3306, user=name, passwd=password, db=dbname, charset='utf8mb4')
    return db
def insertdb(db,table,line):
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO "+ table +" (x,y,address_name) VALUES ('"+line.x+"', '"+line.y+"', '"+line.name+"');"

    try:
        # 执行sql语句
        cursor.execute(sql)
        db.commit()
    except ZeroDivisionError as e:
        print('except:', e)
        db.rollback()

def errDate(db):
    cursor = db.cursor()
    sql = "select  * from address_all_test where x<1;"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id=row[0]
            deletedb(db,id)
    except ZeroDivisionError as e:
        print('except:', e)
        db.rollback()

def deletedb(db,id):
    cursor = db.cursor()

    # SQL 插入语句
    sql = "delete   from address_all_test where id="+id+";"

    try:
        # 执行sql语句
        cursor.execute(sql)
        db.commit()
    except ZeroDivisionError as e:
        print('except:', e)
        db.rollback()

class Line(object):
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
path='shanghai.csv'


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def search_data(param,low,max,db):
    cursor = db.cursor()

    # SQL 插入语句
    sql = "select  *   from address_ where "+param+">" + low + "and"+ param+"<"+max+";"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id=row[0]
            deletedb(db,id)
    except ZeroDivisionError as e:
        print('except:', e)
        db.rollback()

#模糊判断地名是否存在
def check_goal(name,db):
    cursor = db.cursor()
    param = name.replace("'", "")
    #sql = "select  *   from address_last where  address_name like '%" + param + "%';"
    sql = "select  *   from address_last where  address_name = '" + param + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        if (len(results) != 0):
            return True

        else:
            return False
    except ZeroDivisionError as e:
        print('except:', e)
        print(results)





def search_goal(param,db):
    cursor = db.cursor()
    param = param.replace("'","")
    sql = "select  *   from address_last where  address_name ='" + param + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        if(len(results)!=0):
            result1 = str(results[0][1])
            result2 = str(results[0][2])
            sql2="select  *   from location_14 where  x1 < " + result1 + " and x2 > "+result1+"  and y1 < "+result2+" and y2 > "+result2+";"
            cursor.execute(sql2)
            results2 = cursor.fetchall()
            try:

                if(len(results2)!=0):
                    result=(results[0][1],results[0][2],results2[0][0])
                    return result
                else:
                    return 0
            except ZeroDivisionError as e:
                print('except:', e)

        else:
            return 0

    except ZeroDivisionError as e:
        print('except:', e)
        print(results)

    # 文档名字替换
def search_goal2(param, db):
    cursor = db.cursor()
    param = param.replace("'", "")
    sql = "select  *   from address_last where  address_name ='" + param + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        if (len(results) != 0):
            result1 = str(results[0][1])
            result2 = str(results[0][2])
            sql2 = "select  *   from location_14 where  x1 < " + result1 + " and x2 > " + result1 + "  and y1 < " + result2 + " and y2 > " + result2 + ";"
            cursor.execute(sql2)
            results2 = cursor.fetchall()

            try:

                if (len(results2) != 0):
                    return results2[0][0]
                else:
                    return 0
            except ZeroDivisionError as e:
                print('except:', e)

        else:
            return 0

    except ZeroDivisionError as e:
        print('except:', e)
#判断是不是动词
def check_verbs(name,db):
    cursor = db.cursor()
    param = name.replace("'", "")
    sql = "select  *   from verbs where  content = '" + name + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()

        if (len(results) != 0):
            return False

        else:
            return True
    except ZeroDivisionError as e:
        print('except:', e)
