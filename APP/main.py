# -*- coding: utf-8 -*-
'''
# Created on Feb-28-20 13:22
# main.py
# @author: ss
# @description: 应用程序主窗口
'''

from PyQt5 import QtWidgets, QtCore, QtGui 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, 
                QLabel, QLineEdit, QApplication, QPushButton,
                QFrame,
                QMessageBox, QAction)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))

from APP.common import center
from APP.login import LoginWindow
from APP.register import RegisterWindow
from Course.course import Course
from Score.score import Score

class CenterWidget(QWidget):
    '''
    #主窗口中心组件设计中心
    '''
    # parent 传入父亲元素组件
    def __init__(self, parent=None):
        super().__init__()
        self.initUI(parent)
        self.courseWindows = [] #可以存在多个课程窗口
        self.scoreWindows = []

    def initUI(self, parent):

        course_btn = QPushButton('课程管理', self)
        course_btn.setIcon(QIcon('./image/book.png'))
        course_btn.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}"
                                )
        course_btn.clicked.connect(lambda:self.onCourse(parent))

        score_btn = QPushButton('成绩管理', self)
        score_btn.setIcon(QIcon('./image/search.png'))
        score_btn.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:blue}")
        score_btn.clicked.connect(lambda:self.onScore(parent))

        vbox = QVBoxLayout()
        vbox.addWidget(course_btn)
        vbox.addWidget(score_btn)

        midhobx = QHBoxLayout()
        midhobx.addStretch(1)
        midhobx.addLayout(vbox)
        midhobx.addStretch(1)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(midhobx)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(centerFrame)
        hbox.addStretch(1)
        hbox.setStretchFactor(centerFrame, 6)
        self.setLayout(hbox)
    
    def checkUsrTerm(self, parent):
        if parent.usr is None:
            QMessageBox.warning(self, "warning", "用户未登录", QMessageBox.Yes)
            parent.close()
            return False
        elif parent.term is None:
            QMessageBox.warning(self, "warning", "学期不能为空", QMessageBox.Yes)
            parent.close()
            return False
        else:
            return True 

    def onCourse(self, parent):
        if parent is not None:
            if self.checkUsrTerm(parent):
                self.courseWindows.append(Course(parent.usr, parent.term, parent.isstu))
                self.courseWindows[-1].show()
                parent.showMinimized() #父级窗口组件最小化
    
    def onScore(self, parent):
        if parent is not None:
            if self.checkUsrTerm(parent):
                self.scoreWindows.append(Score(parent.usr, parent.term, parent.isstu))
                self.scoreWindows[-1].show()
                parent.showMinimized() #父级窗口组件最小化

term = '2019-2020学年冬季'
class MainWindow(QMainWindow):
    def __init__(self, usr=None, term=None, isstu=True):
        super().__init__()
        self.usr = usr
        self.term = term
        self.isstu = isstu
        self.initUI()
        self.loginWindow = None
    
    def initUI(self):

        #中心组件设置
        centerWidget = CenterWidget(self)
        self.setCentralWidget(centerWidget)

        #菜单栏设置
        menu = self.menuBar().addMenu('账号中心')

        signoutAct = QAction('注销', self) 
        signoutAct.triggered.connect(self.onSignout)
        menu.addAction(signoutAct)

        exitAct = QAction('退出', self)
        exitAct.triggered.connect(self.onExit)
        menu.addAction(exitAct)

        #整体布局
        self.resize(450, 300)
        center(self)
        self.setFont(QFont("Microsoft YaHei", 11))
        self.setWindowTitle('学生选课成绩管理系统')
        self.setWindowIcon(QIcon('./image/j1.png'))
        
        self.bottomlbl = QLabel()
        self.bottomlbl.setFont(QFont("宋体"))
        self.statusBar().addPermanentWidget(self.bottomlbl)
        self.showbottom()

    def showbottom(self):
        #设置底部状态栏, 显示当前登录的用户
        if self.usr is not None:
            s = "欢迎你: " + self.usr
            if self.isstu:
                s = s + ' 同学'
            else:
                s = s + ' 老师'
            self.bottomlbl.setText(s)
    
    #注销重新登录
    def onSignout(self):
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()
    
    def onExit(self):
        self.close()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    registerWindow = RegisterWindow()
    mainWindow = MainWindow(term=term)
    mainWindow.loginWindow = loginWindow 
    registerWindow.loginWindow = loginWindow
    loginWindow.registerWindow = registerWindow
    loginWindow.mainWindow = mainWindow
    loginWindow.show()
    sys.exit(app.exec_())