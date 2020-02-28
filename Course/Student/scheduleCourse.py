# -*- coding: utf-8 -*-
'''
# Created on Feb-10-20 16:42
# scheduleCourse.py
# @author: ss
'''

'''
已选课程
加一点课程表
'''

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QStackedWidget,
                QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                QLabel, QLineEdit,
                QFrame,
                QTableWidget,
                QTableView,
                QRadioButton,
                QPushButton, QMessageBox, 
                QAction, QApplication)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import sip
import util

term = '2019-2020学年冬季'
class ScheduleCourse(QWidget):

    def __init__(self, usr=None, term=None, isstu=True):
        super().__init__()
        self.usr = usr 
        self.term = term 
        self.isstu = isstu
        self.initUI()

    def initUI(self):

        self.totalLayout = QVBoxLayout()
        #数据获取
        data = util.showSelectCourse(self.usr, self.term, self.isstu)
        #上半部分
        uptip = QLabel()
        ups = ''
        if self.isstu:
            ups = '已选课程：'
        else:
            ups = '已开课程：'
        uptip.setText(ups)
        uptip.setFont(QFont('宋体'))

        self.uplayout = QVBoxLayout()
        self.uplayout.addWidget(uptip) 
        self.uptable = None
        self.createUpTable(data)
    
        self.totalLayout.addLayout(self.uplayout)

        #下半部分
        downtip = QLabel('课程表')
        downtip.setFont(QFont('宋体'))

        self.downlayout = QVBoxLayout()
        self.downlayout.addWidget(downtip)
        self.downtable = None
        self.createDownTable(data)

        self.totalLayout.addLayout(self.downlayout)

        self.totalLayout.setStretchFactor(self.uplayout, 1)
        self.totalLayout.setStretchFactor(self.downlayout, 3)
        
        self.setLayout(self.totalLayout)
    
    def createUpTable(self, data):
        if self.uptable is not None:
            self.uplayout.removeWidget(self.uptable)
            sip.delete(self.uptable) 
            self.uptable = None

        rownum, colnum = len(data), 0
        if self.isstu:
            colnum = 5
            self.uptable = QTableWidget(rownum, colnum)
            self.uptable.setHorizontalHeaderLabels(['课程号', '课程名', '教师号', '教师', '上课时间'])
        else:
            colnum = 3
            self.uptable = QTableWidget(rownum, colnum)
            self.uptable.setHorizontalHeaderLabels(['课程号', '课程名', '上课时间'])
        for i in range(rownum):
            for j in range(colnum):
                self.uptable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))
        self.uptable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.uptable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.uptable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.uplayout.addWidget(self.uptable)
    
    def createDownTable(self, data):
        if self.downtable is not None:
            self.downlayout.removeWidget(self.downtable)
            sip.delete(self.downtable)
            self.downtable = None 
        rownum = 13
        colnum = 7
        self.downtable = QTableWidget(rownum, colnum)
        self.downtable.setHorizontalHeaderLabels(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
        for x in data:
            time = x[-1]
            res = util.getclasstime(time)
            for y in res:
                self.downtable.setItem(y[1] - 1, y[0], QtWidgets.QTableWidgetItem(x[1]))
                self.downtable.setSpan(y[1] - 1, y[0], y[2] - y[1] + 1, 1) #单元格合并  
        self.downtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.downtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.downlayout.addWidget(self.downtable)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '0101'
    scheduleCourse = ScheduleCourse(usr=usr, term=term, isstu=False)
    scheduleCourse.resize(700, 600)
    scheduleCourse.show()
    sys.exit(app.exec_())

