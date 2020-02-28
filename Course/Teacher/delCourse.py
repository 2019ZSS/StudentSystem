# -*- coding: utf-8 -*-
'''
# Created on Feb-28-20 15:10
# delCourse.py
# @author: ss
# @description: 删除课程模块
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
class DelCourse(QWidget):

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
        self.bottom = None 
        self.centerLayout = QVBoxLayout()

        self.createCenterTable(util.showSelectCourse(self.usr, self.term, False))
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
            self.msg.setText('您本学期尚未开设课程')
            self.msg.setAlignment(Qt.AlignCenter)
            self.centerLayout.addWidget(self.msg)
            return None

        self.rownum = len(data)
        self.showtable = QTableWidget(self.rownum, 4)  
        self.showtable.setHorizontalHeaderLabels(['', '课程号', '课程名', '上课时间'])
        self.rbtns = []
        for i in range(self.rownum):
            self.rbtns.append(QRadioButton())
            self.showtable.setCellWidget(i, 0, self.rbtns[i])
            for j in range(1, 4):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j-1]))

        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.showtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.centerLayout.addWidget(self.showtable)

        self.confirmbtn = QPushButton('关闭此课程')
        self.confirmbtn.setIcon(QIcon('./image/exit.png'))
        self.confirmbtn.clicked.connect(self.onConfirm)

        self.bottom = QWidget()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addWidget(self.confirmbtn)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        self.bottom.setLayout(hbox)

        self.centerLayout.addWidget(self.bottom)

    def onConfirm(self):
        reply = QMessageBox.question(self, '提示', '确认退课', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.No:
            return None
        for i in range(self.rownum):
            if self.rbtns[i].isChecked() == True:
                kh = self.showtable.item(i, 1).text()
                gh = self.usr 
                sksj = self.showtable.item(i, 3).text()
                flag, e = util.delOpenCourse(self.term, kh, gh, sksj)
                if flag == True:
                    QMessageBox.information(self, '确认', '已关闭课程', QMessageBox.Yes)
                    self.rbtns.remove(self.rbtns[i])
                    self.showtable.removeRow(i)
                    self.rownum = self.rownum - 1
                    if self.rownum == 0:
                        self.createCenterTable([])
                else:
                    QMessageBox.information(self, '抱歉', str(e), QMessageBox.Yes)
                return None

        QMessageBox.warning(self, 'warning', '对不起你没有选择任何课程', QMessageBox.Yes)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '0101'
    delCourse = DelCourse(usr, term)
    delCourse.resize(700, 450)
    delCourse.show()
    sys.exit(app.exec_())