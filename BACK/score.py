# -*- coding: utf-8 -*-
'''
# Created on Feb-28-20 14:32
# score.py
# @author: ss
# @description: 成绩管理模块
'''

from BACK.util import op_mysql
from BACK.util import judgeclasstime
from BACK.util import search, searchOnC, searchOnE, searchOnO, searchOnT
import matplotlib.pyplot as plt
import matplotlib

def tranScore(x):
    '''
    成绩换算
    '''
    if x >= 90:
        return 4.0
    elif x >= 85:
        return 3.7
    elif x >= 82:
        return 3.3
    elif x >= 78:
        return 3.0
    elif x >= 75:
        return 2.7
    elif x >= 72:
        return 2.3
    elif x >= 68:
        return 2.0
    elif x >= 64:
        return 1.7
    elif x >= 60:
        return 1.0
    else:
        return 0.0    

def getScore(xh, xq):

    sql = "select kh, gh, zpcj from e where xh = '%s' and xq = '%s' and zpcj > 0" % (xh, xq)
    flag, res = op_mysql(sql)
    if flag and (len(res) == 0):
        return []
    elif flag == False:
        return []
    
    data = [] # 课程号', '课程名', '学分', '教师', '总分', '评定']
    for x in res:
        tmp = []
        tmp.append(x[0]) # kh
        tmp.append(searchOnC(iskh=False, iskm=True, kh=x[0])[0][0]) # km
        tmp.append(searchOnC(0, 0, 1, 0, 0, kh=x[0])[0][0]) # xf
        tmp.append(searchOnT(isgh=False, isxm=True, gh=x[1])[0][0]) # js
        tmp.append(x[2]) # zpcj
        tmp.append(tranScore(int(x[2])))
        data.append(tmp)
    return data


def getClassLists(xq, kh, gh):
    '''
    在选课表e中获取某个老师某门课程的班级信息
    '''
    sql = "select xh, pscj, kscj, zpcj from e where xq='%s' and kh='%s' and gh='%s'" %(xq, kh, gh)
    flag, res = op_mysql(sql)
    if flag and len(res) == 0:
        return []
    elif flag == False:
        return []
    data = []
    for x in res:
        tmp = []
        tmp.append(x[0])
        sql = "select xm from s where xh = '%s'" % (x[0])
        _, y = op_mysql(sql)
        tmp.append(y[0][0])
        for i in range(1, 4):
            if x[i] != None:
                tmp.append(str(x[i]))
            else:
                tmp.append('null')
        data.append(tmp)
    return data

def updateStuScore(xh, xq, kh, gh, pscj, kscj, zpcj):
    '''
    更新学生的成绩
    '''
    sql = '''update e set pscj=%s, kscj=%s, zpcj=%s 
                where xh='%s' and xq='%s' and kh='%s' and gh='%s' 
            ''' % (pscj, kscj, zpcj, xh, xq, kh, gh)
    flag, e = op_mysql(sql)
    return flag, e

def drawCourseScore(data, title="课程"):
    '''
    data: 分数列表
    eg: data = [58, 60, 70, 74, 82, 85, 89, 90]
    '''
    def translevel(x):
        if x < 1.0:
            return 0
        elif x < 2.0:
            return 1
        elif x < 3.0:
            return 2
        elif x < 4.0:
            return 3
        else:
            return 4

    for i in range(len(data)):
        data[i] = tranScore(data[i])
        data[i] = translevel(data[i])

    initlabel = ['<1.0', '1.0~1.7', '2.0~2.7', '3.0~3.7', '4.0']
    label = []
    d2 = [0, 0, 0, 0, 0]
    for i in range(len(data)):
        d2[data[i]] = d2[data[i]] + 1
    for i in range(5):
        if d2[i]:
            label.append(initlabel[i])

    #用来字体集为黑体
    plt.rcParams['font.sans-serif']=['SimHei']
    #用来正常显示负号
    plt.rcParams['axes.unicode_minus']=False
    fractions = []
    for i in range(5):
        if d2[i]:
            fractions.append(float(d2[i]) / len(data) * 100)
    explode = []
    for i in range(len(fractions)):
        explode.append(0.1)
    plt.pie(fractions,labels=label,explode=explode,autopct='%1.2f%%')
    plt.title(title + "成绩分布")
    plt.show()

if __name__ == "__main__":
    drawCourseScore(data=[58, 60, 70, 74, 82, 85, 89, 90])
