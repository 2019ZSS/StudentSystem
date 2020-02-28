# -*- coding: utf-8 -*-
'''
# Created on Feb-15-20 17:08
# scoremanage.py
# @author: ss
# 说明：成绩管理窗口
'''

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QStackedWidget,
                QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                QComboBox,
                QLabel, QLineEdit,
                QFrame,
                QTableWidget,
                QTableView,
                QRadioButton,
                QPushButton, QMessageBox, 
                QAction, QApplication,
                QItemDelegate)
from PyQt5.QtGui import QFont, QIcon

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import sip
# import util
import Score.util as util

class EmptyDelegate(QItemDelegate):
    def __init__(self,parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None

class Scoremanage(QWidget):

    def __init__(self, usr=None, term=None):
        super().__init__()
        self.usr = usr
        self.term = term 
        self.initUI()
    
    def initUI(self):
        
        coursename = QLabel("请选择课程： ", self)
        coursename.setAlignment(Qt.AlignRight)
        coursename.setFont(QFont('微软雅黑'))

        self.coursedata = []
        self.courseButton = None
        self.tophbox = QHBoxLayout()
        self.tophbox.addWidget(coursename)

        self.createCourse(util.showSelectCourse(self.usr, self.term, False)) #获取课程数据

        self.centerLayout = QVBoxLayout()
        self.rownum = 0
        self.showtable = None
        self.createCenterTable(util.getClassLists(self.term, self.coursedata[self.courseButton.currentIndex()][0], self.usr))

        self.saveButton = QPushButton('成绩保存')
        self.saveButton.setIcon(QIcon('./image/save.png'))
        self.saveButton.clicked.connect(self.onSave)
        self.drawButton = QPushButton('成绩分布')
        self.drawButton.setIcon(QIcon('./image/showcourse.png'))
        self.drawButton.clicked.connect(self.onDraw)

        midhbox = QHBoxLayout()
        scalelbl = QLabel('成绩比/')
        normal = QLabel('平时占比: ')
        self.normalInput = QLineEdit()
        self.normalInput.setText('0.3')
        exam = QLabel('考试占比: ')
        self.examInput = QLineEdit()
        self.examInput.setText('0.7')

        midhbox.addStretch(1)
        midhbox.addWidget(scalelbl)
        midhbox.addWidget(normal)
        midhbox.addWidget(self.normalInput)
        midhbox.addWidget(exam)
        midhbox.addWidget(self.examInput)
        midhbox.addStretch(1)

        downhbox = QHBoxLayout()
        downhbox.addStretch(1)
        downhbox.addWidget(self.saveButton)
        downhbox.addWidget(self.drawButton)
        downhbox.addStretch(1)

        totallayout = QVBoxLayout()
        totallayout.addLayout(self.tophbox)
        totallayout.addLayout(self.centerLayout)
        totallayout.addLayout(midhbox)
        totallayout.addLayout(downhbox)

        self.setLayout(totallayout)
    
    def createCourse(self, data):

        if self.courseButton is not None:
            self.tophbox.removeWidget(self.courseButton)
            sip.delete(self.courseButton)

        self.coursedata = data
        self.courseButton = QComboBox()
        courselists = []
        for x in self.coursedata:
            courselists.append(x[1])
        self.courseButton.addItems(courselists)
        self.courseButton.currentIndexChanged.connect(self.onChangeCourse)

        self.tophbox.addWidget(self.courseButton)


    def onChangeCourse(self):
        self.createCenterTable(util.getClassLists(self.term, self.coursedata[self.courseButton.currentIndex()][0], self.usr))
    
    def delCenterTable(self):

        if self.showtable is not None:
            self.centerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)

    def createCenterTable(self, data):
        self.delCenterTable()
        self.rownum = len(data)
        collists = ['学号', '姓名', '平时', '考试', '总评']
        self.colnum = len(collists)
        self.showtable = QTableWidget(self.rownum, self.colnum)  
        self.showtable.setHorizontalHeaderLabels(collists)
        for i in range(2):
            self.showtable.setItemDelegateForColumn(i, EmptyDelegate(self)) #设置某列不可编辑
        for i in range(self.rownum):
            for j in range(self.colnum):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))

        self.centerLayout.addWidget(self.showtable)
    
    def onSave(self):
        normal = self.normalInput.text()
        exam = self.examInput.text()
        if normal == '':
            QMessageBox.warning(self, '警告', '请输入平时成绩占比', QMessageBox.Yes)
        elif exam == '':
            QMessageBox.warning(self, '警告', '请输入考试成绩占比', QMessageBox.Yes)
        else:
            reply = QMessageBox.question(self, '提示', '确认保存', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                normal = float(normal)
                exam = float(exam)
                for i in range(self.rownum):
                    pscj = self.showtable.item(i, 2).text()
                    kscj = self.showtable.item(i, 3).text()
                    try:
                        pscj = float(pscj)
                        kscj = float(kscj)
                        xh = self.showtable.item(i, 0).text()
                        kh = self.coursedata[self.courseButton.currentIndex()][0]
                        gh = self.usr
                        xq = self.term
                        zpcj = pscj * normal + kscj * exam
                        zpcj = str(int(zpcj))
                        util.updateStuScore(xh, xq, kh, gh, str(pscj), str(kscj), zpcj)
                    except Exception as e:
                        print(e)
                self.createCenterTable(util.getClassLists(self.term, self.coursedata[self.courseButton.currentIndex()][0], self.usr))
                QMessageBox.information(self, '确认', '成绩更新成功', QMessageBox.Yes)
    
    def onDraw(self):
        
        data = []
        for i in range(self.rownum):
            x = self.showtable.item(i, 4).text()
            if x == 'null':
                continue
            data.append(int(x))
        if len(data) == 0:
            QMessageBox.warning(self, '警告', '未登入有成绩', QMessageBox.Yes)
        else:
            util.drawCourseScore(data, self.courseButton.currentText() + "课程")

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    usr = '0101'
    term = '2019-2020学年冬季'
    scoremanage = Scoremanage(usr, term)
    scoremanage.resize(750, 350)
    scoremanage.show()
    sys.exit(app.exec_())

