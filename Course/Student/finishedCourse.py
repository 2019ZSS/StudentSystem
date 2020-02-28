# -*- coding: utf-8 -*-
'''
# Created on Feb-10-20 16:50
# finishedCourse.py
# @author: ss
# 说明： 查询已经选修过的所有课程
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

class FinishedCourse(QWidget):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr 
        self.initUI()

    def initUI(self):

        self.centerLayout = QVBoxLayout(self)
        self.msg = QLabel(self)
        self.rownum = 0
        self.showtable = None
        self.setLayout(self.centerLayout)

        self.createCenterTable(util.finishedCourse(self.usr))

    def delCenterTable(self):
        if self.msg.text() != '':
            self.centerLayout.removeWidget(self.msg)

        if self.rownum >= 0 and self.showtable is not None:
            self.centerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)

    def createCenterTable(self, data):
        self.delCenterTable()
        if len(data) == 0:
            self.msg.setText('对不起, 未查到有关的选修记录')
            self.msg.setAlignment(Qt.AlignCenter)
            self.centerLayout.addWidget(self.msg)
            return None
        
        self.rownum = len(data)
        self.showtable = QTableWidget(self.rownum, 6)  
        self.showtable.setHorizontalHeaderLabels(['学期', '课程号', '课程名', '教师号', '教师', '上课时间'])
        for i in range(self.rownum):
            for j in range(0, 6):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))
        
        #设置水平方向表格为自适应的伸缩模式
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # 将表格变为禁止编辑
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置表格整行选中
        self.showtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.centerLayout.addWidget(self.showtable)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    finishedCourse = FinishedCourse('1102')
    finishedCourse.resize(700, 300)
    finishedCourse.show()
    sys.exit(app.exec_())
