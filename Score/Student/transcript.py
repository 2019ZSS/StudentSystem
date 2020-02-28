# -*- coding: utf-8 -*-
'''
# Created on Feb-15-20 15:56
# transcript.py
# @author: ss
# 说明：成绩单显示成绩模块
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
from PyQt5.QtGui import QFont, QIcon

import sys
# import os 
# sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import sip
import Score.util as util

term = '2019-2020学年冬季学期'
class Transcript(QWidget):

    def __init__(self, usr=None, term=None):
        super().__init__()
        self.usr = usr 
        self.term = term 
        self.initUI()

    def initUI(self):

        self.msg = QLabel(self)
        self.rownum = 0
        self.showtable = None
        self.rbtns = []
        self.centerLayout = QVBoxLayout()
        self.bottom = None
        
        self.createCenterTable(util.getScore(self.usr, self.term))

        self.setLayout(self.centerLayout) 
    
    def delCenterTable(self):

        if self.msg.text() != '':
            self.centerLayout.removeWidget(self.msg)
            sip.delete(self.msg)
            self.msg = QLabel(self)
        
        if self.rownum > 0 and self.rownum > 0 and self.showtable is not None:
            self.centerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.centerLayout.removeWidget(self.bottom)
            sip.delete(self.bottom)
            self.rbtns = []
            self.rownum = 0
    
    def createCenterTable(self, data):
        self.delCenterTable()
        if len(data) == 0:
            self.msg.setText('本学期成绩未出')
            self.msg.setAlignment(Qt.AlignCenter)
            self.centerLayout.addWidget(self.msg)
            return None

        self.rownum = len(data)
        self.showtable = QTableWidget(self.rownum, 6)  
        self.showtable.setHorizontalHeaderLabels(['课程号', '课程名', '学分', '教师', '总分', '评定'])
        for i in range(self.rownum):
            for j in range(6):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))

        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.showtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.centerLayout.addWidget(self.showtable)

        self.avglabel = QLabel(self)
        avg = 0.0
        total = 0.0
        for x in data:
            avg = int(x[2]) * x[-1]
            total = int(x[2])

        avg = avg / total

        self.avglabel.setText('均绩: ' + str(avg))

        self.bottom = QWidget()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addWidget(self.avglabel)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        self.bottom.setLayout(hbox)

        self.centerLayout.addWidget(self.bottom)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '1102'
    term = '2012-2013冬季'
    transcript = Transcript(usr, term)
    transcript.resize(700, 100)
    transcript.show()
    sys.exit(app.exec_())