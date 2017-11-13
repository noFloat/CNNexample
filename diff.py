import MySQLdb
import configparser
import sys
import linecache

def connectdb():
    conf = configparser.ConfigParser()
    conf.read("./mysql.conf")
    name = conf.get("mysql", "name")
    password = conf.get("mysql", "password")
    dbname = conf.get("mysql", "dbname")
    db = MySQLdb.connect("localhost",name,password,dbname )
    db.set_character_set('utf8')
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
        print(line.name)
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

f = open(path)

db = connectdb()
for  i in range(1,284537):
    line = linecache.getline(path,i )
    lineSpilt = line.split(',')
    lineSpilt[3].isdigit()
    check=is_number(lineSpilt[3])
    check2 = is_number(lineSpilt[4])
    if(check&check2):
        insertdb(db, 'address_copy', Line(lineSpilt[3], lineSpilt[4], lineSpilt[1]))
    #print(lineSpilt[3],lineSpilt[4],lineSpilt[1])
    #sys.exit()

errDate(db)