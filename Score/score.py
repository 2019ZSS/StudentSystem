# -*- coding: utf-8 -*-
'''
# Created on Feb-08-20 12:39
# score.py
# @author: ss
'''

'''
这主要是成绩管理模块
'''

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QStackedWidget,
                QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                QLabel, QLineEdit,
                QFrame,
                QComboBox,
                QPushButton, QMessageBox,
                QTabWidget, 
                QAction, QApplication)
from PyQt5.QtGui import QFont, QIcon

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import Score.util as util
from APP.common import center
from Score.Student.transcript import Transcript
from Score.Teacher.scoremanage import Scoremanage

class Score(QWidget):

    def __init__(self, usr=None, term=None, isstu=True):
        super().__init__()
        self.usr = usr 
        self.term = term
        self.isstu = isstu
        self.initUI()
    
    def initUI(self):
        
        termlbl = QLabel('学期: ', self)
        termlbl.setFont(QFont('微软雅黑'))
        
        self.termButton = QComboBox()
        termlists = util.getTerm()
        self.termButton.addItems(termlists)
        for i in range(len(termlists)):
            if termlists[i] == self.term:
                self.termButton.setCurrentIndex(i)
        self.termButton.currentIndexChanged.connect(self.onChangeTerm)

        tophbox = QHBoxLayout()
        tophbox.addStretch(1)
        tophbox.addWidget(termlbl)
        tophbox.addSpacing(10)
        tophbox.addWidget(self.termButton)
        tophbox.addStretch(1)

        centerFrame = QFrame()
        centerFrame.setFrameShape(QFrame.StyledPanel)

        self.centerWidget = QTabWidget(self)

        if self.isstu:
            #需要重载书写这两个模块
            self.centerWidget.tab1 = Transcript(self.usr, self.term)
            # self.centerWidget.tab2 = QWidget()

            self.centerWidget.addTab(self.centerWidget.tab1, '成绩单')
            # self.centerWidget.addTab(self.centerWidget.tab2, '成绩走势')
        else:
            self.centerWidget = Scoremanage(self.usr, self.term)

        centerhbox = QHBoxLayout()
        centerhbox.addWidget(self.centerWidget)
        centerFrame.setLayout(centerhbox)

        totalvbox = QVBoxLayout()
        totalvbox.addLayout(tophbox)
        totalvbox.addWidget(centerFrame)
        self.setLayout(totalvbox)

        center(self)
        self.resize(450, 350)
        self.setWindowIcon(QIcon('./image/search.png'))
        self.setWindowTitle('成绩管理')
        self.setFont(QFont("宋体", 10))
    
    def onChangeTerm(self):

        self.term = self.termButton.currentText()
        if self.isstu:
            self.centerWidget.tab1.term = self.term 
            self.centerWidget.tab1.createCenterTable(util.getScore(self.usr, self.term))
        else:
            self.centerWidget.term = self.term
            self.centerWidget.createCourse(util.showSelectCourse(self.usr, self.term, False))
            if len(self.centerWidget.coursedata) > 0:
                self.centerWidget.courseButton.setCurrentIndex = 0
                self.centerWidget.createCenterTable(util.getClassLists(self.term, self.centerWidget.coursedata[0][0], self.usr))
            else:
                self.centerWidget.createCenterTable([])

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '0101'
    term = term = '2019-2020学年冬季'
    scoreWindow = Score(usr, term, False)
    scoreWindow.resize(700, 300)
    scoreWindow.show()
    sys.exit(app.exec_())