# -*- coding: utf-8 -*-
'''
# Created on Feb-06-20 16:56
# util.py
# @author: ss
# 说明：这里主要后台对数据库的调用
'''

import pymysql,hashlib
import re 

def md5(s, salt='Database2020!$%@#+'):
    '''
    这是一个md5哈希函数，主要是对文本进行哈希加密
    返回一个32位的十六进制加密字符串
    '''
    s = (str(s) + salt).encode()
    m = hashlib.md5(s) #加密
    return m.hexdigest()

class Database:
    """
    Tables used in the database:
    department: did; name
    student: sid; name; gender; did; password
    teacher: tid; name; gender; did; password
    course: cid; name; credit; tid; did; time
    selection: cid; sid; score
    """
    def __init__(self, mysql_info):
        self._connection = pymysql.connect(**mysql_info)

    def __del__(self):
        self._connection.close()
    
    def _execute(self, query):
        '''
        返回执行结果
        '''
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            s = query.split()[0]

            res = None
            if s == 'update' or s == 'insert' or s == 'delete':
                self._connection.commit()
                cursor.close()
            elif s == 'select':
                res = cursor.fetchall()
                cursor.close()
            return (True, res)
        except Exception as e:
            self._connection.rollback()
            return (False, e)

mysql_info = {
            'host': 'localhost', # 数据库地址
            'user': 'root', # 数据库用户身份
            'password': 'Zss0815+', # 数据库用户对应的密码密码
            'db': 'school', # 数据库的名字
            'charset': 'utf8', # 数据库编码方式
            'autocommit': True}
db = Database(mysql_info)

def op_mysql(sql:str):
    '''
    输入sql命令操作数据库返回对应结果
    '''
    return db._execute(query=sql)

def search(ser, tablename, jud, jres):
    sql = 'select ' + ser + ' from ' + tablename
    if jud and jres:
        sql = (sql + ' where ' + jud) % jres
    flag, res = op_mysql(sql)
    if flag:
        return res
    else:
        return None


def register(usr, pwd, cpwd, isstu=True):
    '''
    注册函数
    返回int类型代表各种情况
    -2 数据库端程序错误
    -1 输入字段存在空
    0 成功注册
    1 输入两次密码不一致
    2 用户名已经存在数据库之中
    3 用户不在对应数据表之中
    '''
    if usr and pwd and cpwd:
        if pwd != cpwd:
            return 1 #两次输入密码不一致
        
        query = ""
        if isstu:
            query = "select xh from s where xh = '%s'" % (usr)
        else:
            query = "select gh from t where gh = '%s'" % (usr)

        flag, res = op_mysql(query)
        if flag:
            if len(res) == 0:
                return 3 #用户不存在相关数据库中

        usr = md5(usr)
        select_usr_sql = "select * from Account where usr = '%s'" % (usr)
        flag, res = op_mysql(select_usr_sql)
        if flag == False:
            return -2 #存在bug
        else:
            if res:
                for x in res:
                    if x[0] == usr:
                        return 2 # 用户名已经存在
            else:
                pwd = md5(pwd)
                ins_sql = "insert into Account(usr, pwd) values ('%s', '%s')" % (usr, pwd)
                flag, res = op_mysql(ins_sql)
                if flag:
                    return 0 # 注册成功
                else:
                    return -2 # 出了bug    
    else:
        return -1 #存在输入为空


def login(usr, pwd, isstu=True):
    '''
        登录验证函数
    '''
    query = ""
    if isstu:
        query = "select xh from s where xh = '%s'" % (usr)
    else:
        query = "select gh from t where gh = '%s'" % (usr) 
    flag, res = op_mysql(query)
    if flag:
        if len(res) == 0:
            return 3 #用户不存在相关数据库中
            
    usr = md5(usr)
    pwd = md5(pwd)            
    if usr and pwd:
        select_usr_sql = "select * from Account where usr = '%s'" % (usr)
        flag, res = op_mysql(select_usr_sql)
        if flag == False:
            return -2
        else:
            if res:
                for x in res:
                    if x[0] == usr:
                        if x[1] == pwd:
                            return 0 # 密码正确, 可以登录
                        else:
                            return 1 # 密码错误, 不可登录
            return 2 #此用户不存在
    else:
        return -1 


def searchOnC(iskh=True, iskm=True, isxf=False, isxs=False, isyxh=False,
              kh=None, km=None, xf=None, xs=None, yxh=None
            ):
    '''
    在C表中进行查询
    '''
    ser = []
    if iskh or iskm or isxf or isxs or isyxh:
        if iskh:
            ser.append('kh')
        if iskm:
            ser.append('km')
        if isxf:
            ser.append('xf')
        if isxs:
            ser.append('xs')
        if isyxh:
            ser.append('yxh')
    else:
        ser.append('*')
    ser = ','.join(ser)

    jud = []
    jres = []
    if kh or km or xf or xs or yxh:
        if kh:
            jud.append("kh='%s'")
            jres.append(kh)
        if km:
            jud.append("km='%s'")
            jres.append(km)
        if xf:
            jud.append("xf='%s'")
            jres.append(xf)
        if xs:
            jud.append("xs='%s'")
            jres.append(xs)
        if yxh:
            jud.append("gh='%s'")
            jres.append(yxh)
    jud = ' and '.join(jud)
    jres = tuple(jres)    
    return search(ser, 'c', jud, jres)


def searchOnT(isgh=True, isxm=True, isxl=False, isyxh=False,
            gh=None, xm=None, yxh=None 
            ):
    '''
    在T表中进行查询
    '''
    ser = []
    if isgh or isxm or isxl or isyxh:
        if isgh:
            ser.append('gh')
        if isxm:
            ser.append('xm')
        if isxl:
            ser.append('xl')
        if isyxh:
            ser.append('yxh')
    else:
        ser.append('*')

    ser = ','.join(ser)

    jud = []
    jres = []
    if gh or xm or yxh:
        if gh:
            jud.append("gh='%s'")
            jres.append(gh)
        if xm:
            jud.append("xm='%s'")
            jres.append(xm)
        if yxh:
            jud.append("gh='%s'")
            jres.append(yxh)
    jud = ' and '.join(jud)
    jres = tuple(jres)    

    return search(ser, 't', jud, jres)


def searchOnO(isxq=False, iskh=True, isgh=True, issksj=True, #前面四项代表查询返回项
              xq=None, kh=None, gh=None, sksj=None #后面四项代表要查询项对应条件
              ):
    '''
    根据学期, 课号, 工号, 上课时间
    在开课表O中进行课程查询
    '''
    if xq == None and kh == None and gh == None and sksj == None:
        return None

    ser = []
    if isxq or iskh or isgh or issksj:
        if isxq:
            ser.append('xq')
        if iskh:
            ser.append('kh')
        if isgh:
            ser.append('gh')
        if issksj:
            ser.append('sksj')
    else:
        ser.append('*')
    
    ser = ','.join(ser)

    jud = []
    jres = []
    if xq or kh or gh or sksj:
        if xq:
            jud.append("xq='%s'")
            jres.append(xq)
        if kh:
            jud.append("kh='%s'")
            jres.append(kh)
        if gh:
            jud.append("gh='%s'")
            jres.append(gh)
        if sksj:
            jud.append("sksj='%s'")
            jres.append(sksj)
    jud = ' and '.join(jud)
    jres = tuple(jres)

    return search(ser, 'o', jud, jres)   

def searchOnE(isxh=False, isxq=False, iskh=True, isgh=True,
                xh=None, xq=None, kh=None, gh=None
                ):
    '''
    在e表中进行查询(不考虑成绩的情况下)
    '''
    if xq == None and kh == None and gh == None and xh == None:
        return None
    
    ser = []
    if isxh or isxq or iskh or isgh:
        if isxh:
            ser.append('xh')
        if isxq:
            ser.append('xq')
        if iskh:
            ser.append('kh')
        if isgh:
            ser.append('gh')
    else:
        ser.append('*')
    
    ser = ','.join(ser)

    jud = []
    jres = []
    if xh or xq or kh or gh:
        if xh:
            jud.append("xh='%s'")
            jres.append(xh)
        if xq:
            jud.append("xq='%s'")
            jres.append(xq)
        if kh:
            jud.append("kh='%s'")
            jres.append(kh)
        if gh:
            jud.append("gh='%s'")
            jres.append(gh)
    jud = ' and '.join(jud)
    jres = tuple(jres)

    return search(ser, 'e', jud, jres)

def getclasstime(data):
    '''
    星期一6-10 的数据中获取时间节点
    返回[0, 6, 10]
    '''
    data = data.split('星期')
    res = []
    lis = ['一', '二', '三', '四', '五', '六', '日']
    for x in data:
        if x != '':
            tmp = [] 
            for i in range(len(lis)):
                if x[0] == lis[i]:
                    tmp.append(i)
                    break
            x = x[1:].split('-')
            tmp.append(int(re.sub("\D", "", x[0])))
            tmp.append(int(re.sub("\D", "", x[1])))
            res.append(tmp)
    return res

def judgeclasstime(time1, time2):
    '''
    两个课程时间是否冲突
    time = [(day, st, ed)]
    '''
    time1 = getclasstime(time1)
    time2 = getclasstime(time2)
    for x in time1:
        for y in time2:
            if x[0] != y[0]:
                continue
            if x[1] <= y[1] and y[1] <= x[2]:
                return False
            if y[1] <= x[1] and x[1] <= y[2]:
                return False
            if x[1] <= y[2] and y[2] <= x[2]:
                return False
            if y[1] <= x[2] and x[2] <= y[2]:
                return False        
    return True # 不冲突

def getTerm():
    '''
    # 功能：获取学期
    # 接受参数：
    # 返回参数：
    '''
    sql = "select distinct xq from o order by xq desc"
    _, res = op_mysql(sql)
    data = []
    for x in res:
        data.append(x[0])
    return data


def test():
    print('test')

if __name__ == "__main__":
    test()
            

