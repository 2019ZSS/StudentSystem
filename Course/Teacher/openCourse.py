# -*- coding: utf-8 -*-
'''
# Created on Feb-11-20 17:00
# openCourse.py
# @author: ss
# 说明：开设课程窗口模块设计
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
class OpenCourse(QWidget):

    def __init__(self, usr=None, term=None):
        super().__init__()
        self.usr = usr
        self.term = term 
        self.initUI()
    
    def initUI(self):
        
        cname = QLabel('课程名:   ')
        self.cnameInput = QLineEdit()

        ctime = QLabel('上课时间： ')
        self.ctimeInput = QLineEdit()
        self.ctimeInput.setPlaceholderText('星期一10-11')
        
        self.confirmbtn = QPushButton('确认开课')
        self.confirmbtn.setIcon(QIcon('./image/confirm.png'))
        self.confirmbtn.setFont(QFont('宋体'))
        self.confirmbtn.clicked.connect(self.onConfirm)

        topvbox1 = QVBoxLayout()
        topvbox1.addWidget(cname)
        topvbox1.addWidget(ctime)

        topvbox2 = QVBoxLayout()
        topvbox2.addWidget(self.cnameInput)
        topvbox2.addWidget(self.ctimeInput)

        tophbox = QHBoxLayout()
        tophbox.addLayout(topvbox1)
        tophbox.addLayout(topvbox2)
        tophbox.setStretchFactor(topvbox1, 1)
        tophbox.setStretchFactor(topvbox2, 3) 

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addStretch(1)
        downhbox.addWidget(self.confirmbtn) 
        downhbox.addStretch(1)
        downhbox.addStretch(1)

        totalvbox = QVBoxLayout()
        totalvbox.addLayout(tophbox)
        totalvbox.addLayout(downhbox)

        self.setLayout(totalvbox)
    
    def onConfirm(self):
        cname = self.cnameInput.text()
        ctime = self.ctimeInput.text()

        if cname == '':
            QMessageBox.warning(self, 'warning', '未输入课程名', QMessageBox.Yes)
        elif ctime == '':
            QMessageBox.warning(self, 'warning', '未输入上课时间', QMessageBox.Yes)
        else:
            reply = QMessageBox.question(self, '提示', '确认开课', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return None
            flag = util.openCourse(self.usr, self.term, cname, ctime)
            if flag == 1:
                QMessageBox.information(self, '恭喜', '开课成功', QMessageBox.Yes)
            elif flag == 0:
                QMessageBox.information(self, '抱歉', '数据库出了点意外', QMessageBox.Yes)
            elif flag == 2:
                QMessageBox.information(self, '抱歉', '课时冲突', QMessageBox.Yes)
            elif flag == 2:
                QMessageBox.information(self, '抱歉', '该课程名对应课号不存在', QMessageBox.Yes)

        self.cnameInput.clear()
        self.ctimeInput.clear()


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '0101'
    openCourse = OpenCourse(usr=usr, term=term)
    openCourse.resize(450, 350)
    openCourse.show()
    sys.exit(app.exec_())
