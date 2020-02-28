# -*- coding: utf-8 -*-
'''
# Created on Feb-28-20 14:29
# course.py
# @author: ss
# @description: 课程管理相关数据库接口函数实现
'''
import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from BACK.util import op_mysql
from BACK.util import judgeclasstime
from BACK.util import search, searchOnC, searchOnE, searchOnO, searchOnT

def searchCourse(xq, cnum=None, cname=None, tname=None, ctime=None):
    kh = cnum
    if (kh is None or kh == '') and (cname and cname != ''):
        res = searchOnC(iskh=True, iskm=False, km=cname)
        if res:
            kh = res[0][0]
        else:
            return []

    gh = None    
    if tname is not None and tname !='':
        res = searchOnT(isgh=True, isxm=False, xm=tname)
        if res:
            gh = res[0][0]
        else:
            return []

    res = searchOnO(xq=xq, kh=kh, gh=gh, sksj=ctime)
    ans = []
    for x in res:
        tmp = []
        tmp.append(x[0]) # 课号
        #课名
        if  cname: 
            tmp.append(cname)
        else:
            tmp.append(searchOnC(iskh=False, iskm=True, kh=x[0])[0][0])
        #教师号
        tmp.append(x[1])
        if tname:
            tmp.append(tname)
        else:
            tmp.append(searchOnT(isgh=False, isxm=True, gh=x[1])[0][0])
        # 上课时间
        tmp.append(x[2])
        ans.append(tmp)
    return ans

def selectCourse(usr, xq, kh, gh):
    '''
    选课
    尚未判断选课冲突的情况(待补充)
    '''
    time1 = searchOnO(0, 0, 0, 1, xq=xq, kh=kh, gh=gh)[0][0]
    res = searchOnE(0, 0, 1, 1, xh=usr, xq=xq)
    for x in res:
        time2 = searchOnO(0, 0, 0, 1, xq=xq, kh=x[0], gh=x[1])[0][0]
        if judgeclasstime(time1, time2) == False:
            return False

    sql = "insert into e values('%s', '%s',	'%s', '%s', null, null, null)" % (usr, xq, kh, gh)
    flag, _ = op_mysql(sql)
    return flag

def dropSelectCourse(usr, term, kh, gh):
    '''
    退课
    '''
    sql = "delete from e where xh='%s' and xq = '%s' and kh='%s' and gh='%s'" % (usr, term, kh, gh)
    flag, _ = op_mysql(sql)
    return flag


def showSelectCourse(usr, term, isstu=True):
    '''
    展示某学生已选修课程 在e表中进行课程查询
    或者是某老师开设的所有课程 在o表中进行查询
    '''
    if isstu:
        sql = "select kh, gh from e where xh='%s' and xq = '%s'" % (usr, term)
        flag, res = op_mysql(sql)
        if flag == False or len(res) == 0:
            return []
        data = []
        for x in res:
            tmp = []
            tmp.append(x[0]) #课号
            tmp.append(searchOnC(iskh=False, iskm=True, kh=x[0])[0][0]) #课程名
            tmp.append(x[1]) #工号
            tmp.append(searchOnT(isgh=False, isxm=True, gh=x[1])[0][0]) #教师名
            tmp.append(searchOnO(iskh=False, isgh=False, issksj=True, xq=term, kh=x[0], gh=x[1])[0][0]) # 上课时间
            data.append(tmp)
        return data
    else:
        sql = "select kh from o where gh='%s' and xq='%s'" % (usr, term)
        flag, res = op_mysql(sql)
        if flag == False or len(res) == 0:
            return []
        data = []
        for x in res:
            tmp = []
            tmp.append(x[0]) #课号
            tmp.append(searchOnC(iskh=False, iskm=True, kh=x[0])[0][0]) #课程名
            tmp.append(searchOnO(iskh=False, isgh=False, issksj=True, xq=term, kh=x[0], gh=usr)[0][0]) # 上课时间
            data.append(tmp)
        return data

def finishedCourse(usr):
    '''
    查询某学生已经修过的课程
    定义: 总分大于60才能算修过
    '''
    sql = "select xq, kh, gh from e where xh = '%s' and (zpcj >= 60)" % (usr)
    flag, res = op_mysql(sql)
    if flag == False or len(res) == 0:
        return []
    data = []
    for x in res:
        tmp = []
        tmp.append(x[0]) #学期
        tmp.append(x[1]) #课号
        tmp.append(searchOnC(iskh=False, iskm=True, kh=x[1])[0][0]) #课程名
        tmp.append(x[2]) #工号
        tmp.append(searchOnT(isgh=False, isxm=True, gh=x[2])[0][0]) #教师名
        tmp.append(searchOnO(iskh=False, isgh=False, issksj=True, xq=x[0], kh=x[1], gh=x[2])[0][0]) # 上课时间
        data.append(tmp)
    return data

def openCourse(usr, term, cname, ctime):
    '''
    往开课表中增加数据
    老师开课()
    '''
    time1 = ctime
    res = searchOnO(0, 0, 0, 1, xq=term, gh=usr)
    for x in res:
        time2 = x[0]
        if judgeclasstime(time1, time2) == False:
            return 2 # 课时冲突

    kh = searchOnC(1, 0, 0, 0, 0, km=cname)[0][0] 
    if kh is None:
        return 3 # 课号不存在
    sql = "insert into O values('%s',	'%s',  '%s',	'%s')" % (term, kh, usr, ctime)
    flag, e = op_mysql(sql)
    if flag:
        return 1 # 开课成功
    else:
        print(e)
        return 0 # 数据库意外

def delOpenCourse(xq, kh, gh, sksj):
    '''
    删除已经开设的课程
    '''
    sql = "SET FOREIGN_KEY_CHECKS=0"
    op_mysql(sql)
    
    sql = "delete from o where xq = '%s' and kh = '%s' and gh = '%s' and   sksj = '%s'" % (xq, kh, gh, sksj)
    flag, e = op_mysql(sql)

    sql = "SET FOREIGN_KEY_CHECKS=1"
    op_mysql(sql)

    return flag, e