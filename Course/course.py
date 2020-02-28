# -*- coding: utf-8 -*-
'''
# Created on Feb-07-20 15:02
# course.py
# @author: ss
# 说明：这是课程管理窗口主界面
'''

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QStackedWidget,
                QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                QLabel, QLineEdit,
                QFrame,
                QPushButton, QMessageBox, 
                QAction, QApplication)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.common import center
import Course.util as util

from Course.Student.selectCourse import SelectCourse
from Course.Student.dropCourse import DropCourse
from Course.Student.searchCourse import SearchCourse
from Course.Student.scheduleCourse import ScheduleCourse
from Course.Student.finishedCourse import FinishedCourse 

from Course.Teacher.openCourse import OpenCourse
from Course.Teacher.delCourse import DelCourse

term = '2019-2020学年冬季'
class Course(QWidget):

    def __init__(self, usr=None, term=None, isstu=True):
        super().__init__()
        self.usr = usr 
        self.term = term
        self.isstu = isstu
        self.initUI()

    def initUI(self):

        # 页眉
        tiplbl = QLabel()
        tipstr = self.term + '| 欢迎你: ' + self.usr
        if self.isstu:
            tipstr = tipstr + '同学'
        else:
            tipstr = tipstr + '老师'
        tiplbl.setText(tipstr)
        tiplbl.setFont(QFont("Roman times", 7))
        tiplbl.setAlignment(Qt.AlignRight)

        self.searchCoursebtn = QPushButton('课程查询')
        self.searchCoursebtn.setIcon(QIcon('./image/search.png'))
        self.searchCoursebtn.clicked.connect(self.onSearchCourse)

        if self.isstu:
            self.selectCoursebtn = QPushButton('选课')
            self.selectCoursebtn.setIcon(QIcon('./image/selectcourse.png'))
            self.selectCoursebtn.clicked.connect(self.onSelectCourse)
            self.dropCoursebtn = QPushButton('退课')
            self.dropCoursebtn.setIcon(QIcon('./image/dropcourse.png'))
            self.dropCoursebtn.clicked.connect(self.onDropCourse)
            self.scheduleCoursebtn = QPushButton('已选课程')
            self.scheduleCoursebtn.setIcon(QIcon('./image/schedulecourse.png'))
            self.scheduleCoursebtn.clicked.connect(self.onScheduleCourse)
            self.finishedCoursebtn = QPushButton('已修课程')
            self.finishedCoursebtn.setIcon(QIcon('./image/finishedcourse.jpg'))
            self.finishedCoursebtn.clicked.connect(self.onFinshedCourse)
        else:
            self.showCoursebtn = QPushButton('已开课程')
            self.showCoursebtn.setIcon(QIcon('./image/showcourse.png'))
            self.showCoursebtn.clicked.connect(self.onShowCourse)
            self.openCoursebtn = QPushButton('开课')
            self.openCoursebtn.setIcon(QIcon('./image/opencourse.png'))
            self.openCoursebtn.clicked.connect(self.onOpenCourse)
            self.delCoursebtn = QPushButton('关课')
            self.delCoursebtn.setIcon(QIcon('./image/delcourse.png'))
            self.delCoursebtn.clicked.connect(self.onDelCourse)

        vbox = QVBoxLayout()
        vbox.addWidget(self.searchCoursebtn)

        if self.isstu: 
            vbox.addWidget(self.selectCoursebtn)
            vbox.addWidget(self.dropCoursebtn)
            vbox.addWidget(self.scheduleCoursebtn)
            vbox.addWidget(self.finishedCoursebtn)
        else:
            vbox.addWidget(self.showCoursebtn)
            vbox.addWidget(self.openCoursebtn)
            vbox.addWidget(self.delCoursebtn)

        #建立左半边框
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        left.setLayout(vbox)

        #建立堆栈窗口模块, 每次选择只显示当前对应模块
        self.stackedWidget = QStackedWidget(self)

        # 以下五个为对应模块, 一一 重写对应的模块
        self.searchCoure = SearchCourse(self.term)

        # 学生
        if self.isstu:
            self.selectCourse = SelectCourse(self.usr, self.term) 
            self.dropCourse = DropCourse(self.usr, self.term)
            self.scheduleCourse = ScheduleCourse(self.usr, self.term)
            self.finishedCourse = FinishedCourse(self.usr)
        else:
            self.showCourse = ScheduleCourse(self.usr, self.term, self.isstu)
            self.openCourse = OpenCourse(self.usr, self.term)
            self.delCourse = DelCourse(self.usr, self.term)
        
        self.stackedWidget.addWidget(self.searchCoure)
        # 学生:
        if self.isstu:
            self.stackedWidget.addWidget(self.selectCourse)
            self.stackedWidget.addWidget(self.dropCourse)
            self.stackedWidget.addWidget(self.scheduleCourse)
            self.stackedWidget.addWidget(self.finishedCourse)
        else:
            self.stackedWidget.addWidget(self.showCourse)
            self.stackedWidget.addWidget(self.openCourse)
            self.stackedWidget.addWidget(self.delCourse)

        shbox = QHBoxLayout()
        shbox.addWidget(self.stackedWidget)
        #右半
        right = QFrame(self)
        right.setFrameShape(QFrame.WinPanel)
        right.setLayout(shbox)

        gridlayout = QGridLayout()
        gridlayout.addWidget(left, 1, 1, 5, 2)
        gridlayout.addWidget(right, 1, 3, 5, 6)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(tiplbl)
        vbox1.addSpacing(5)
        vbox1.addLayout(gridlayout)
        vbox1.setStretchFactor(tiplbl, 1)
        vbox1.setStretchFactor(gridlayout, 15)

        self.setLayout(vbox1)

        center(self)
        self.resize(800, 500)
        self.setWindowIcon(QIcon('./image/book.png'))
        self.setWindowTitle('课程管理')
        self.setFont(QFont("宋体", 10))

    #--通用端
    def onSearchCourse(self):
        self.stackedWidget.setCurrentIndex(0)
        self.searchCoure.delCenterTable()

    #--学生端
    def onSelectCourse(self):
        self.stackedWidget.setCurrentIndex(1)
        self.selectCourse.delCenterTable()

    def onDropCourse(self):
        self.stackedWidget.setCurrentIndex(2)
        self.dropCourse.createCenterTable(util.showSelectCourse(self.usr, self.term))

    def onScheduleCourse(self):
        self.stackedWidget.setCurrentIndex(3)
        data = util.showSelectCourse(self.usr, self.term, self.isstu)
        self.scheduleCourse.createUpTable(data)
        self.scheduleCourse.createDownTable(data)

    def onFinshedCourse(self):
        self.stackedWidget.setCurrentIndex(4)

    #----教师端
    def onShowCourse(self):
        self.stackedWidget.setCurrentIndex(1)
        data = util.showSelectCourse(self.usr, self.term, self.isstu)
        self.showCourse.createUpTable(data)
        self.showCourse.createDownTable(data)

    def onOpenCourse(self):
        self.stackedWidget.setCurrentIndex(2)

    def onDelCourse(self):
        self.stackedWidget.setCurrentIndex(3)
        self.delCourse.createCenterTable(util.showSelectCourse(self.usr, self.term, False))         

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    # usr = '0102'
    usr = '1102'
    # ex = Course(usr=usr, term=term, isstu=False)
    ex = Course(usr=usr, term=term, isstu=True)
    ex.show()
    sys.exit(app.exec_())