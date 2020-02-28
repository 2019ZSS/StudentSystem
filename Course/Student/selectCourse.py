# -*- coding: utf-8 -*-
'''
# Created on Feb-09-20 19:55
# selectCourse.py
# @author: ss
'''

'''
选课窗口设计
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
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
import sip
import util



usr = 1102
term = '2019-2020学年冬季'
class SelectCourse(QWidget):

    def __init__(self, usr=None, term=None):
        super().__init__()
        self.usr = usr
        self.term = term 
        self.initUI()
    
    def initUI(self):

        cnum = QLabel('课程号:    ')
        self.cnumInput = QLineEdit()

        cname = QLabel('课程名:   ')
        self.cnameInput = QLineEdit()

        tname = QLabel('教师：     ')
        self.tnameInput = QLineEdit()

        ctime = QLabel('上课时间：')
        self.ctimeInput = QLineEdit()

        self.searchbtn = QPushButton('查询', self)
        self.searchbtn.setIcon(QIcon('./image/find1.png'))
        self.searchbtn.clicked.connect(self.onSearch)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(cnum)
        vbox1.addWidget(cname)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.cnumInput)
        vbox2.addWidget(self.cnameInput)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(tname)
        vbox3.addWidget(ctime)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.tnameInput)
        vbox4.addWidget(self.ctimeInput)

        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        hbox1.addStretch(1)
        hbox1.addLayout(vbox3)
        hbox1.addLayout(vbox4)

        hbox1.setStretchFactor(vbox1, 1)
        hbox1.setStretchFactor(vbox2, 3)
        hbox1.setStretchFactor(vbox3, 1)
        hbox1.setStretchFactor(vbox4, 3)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.searchbtn)
        hbox2.addStretch(1)

        vbox5 = QVBoxLayout()
        vbox5.addLayout(hbox1)
        vbox5.addLayout(hbox2)

        self.centerframe = QFrame(self)
        self.centerframe.setFrameShape(QFrame.StyledPanel)

        self.centerLayout = QVBoxLayout(self)
        self.centerframe.setLayout(self.centerLayout)

        self.msg = QLabel(self)
        
        self.rownum = 0
        self.showtable = None
        self.rbtns = []

        self.bottom = None

        total = QVBoxLayout(self)
        total.addLayout(vbox5)
        total.addWidget(self.centerframe)
        total.setStretchFactor(vbox5, 1)
        total.setStretchFactor(self.centerframe, 3)
        self.setLayout(total)
    
    def onSearch(self):
        cnum = self.cnumInput.text()
        cname = self.cnameInput.text()
        tname = self.tnameInput.text()
        ctime = self.ctimeInput.text()

        if cnum == '' and cname == '' and tname == '' and ctime == '':
            QMessageBox.warning(self, 'warning', '对不起你没有输入任何内容', QMessageBox.Yes)
        else:
            self.createCenterTable(util.searchCourse(self.term, cnum, cname, tname, ctime))
        self.cnumInput.clear()
        self.cnameInput.clear()
        self.tnameInput.clear()
        self.ctimeInput.clear()
        return None 
    
    def delCenterTable(self):
        #删除中心布局里的控件
        if self.msg.text() != '':
            self.centerLayout.removeWidget(self.msg)
            sip.delete(self.msg)
            self.msg = QLabel(self)

        if self.rownum > 0 and self.showtable is not None:
            self.centerLayout.removeWidget(self.showtable)
            sip.delete(self.showtable)
            self.centerLayout.removeWidget(self.bottom)
            sip.delete(self.bottom)
            self.rbtns = []
            self.rownum = 0

    def createCenterTable(self, data):
        self.delCenterTable()
        if len(data) == 0:
            self.msg.setText('对不起<br/>没有找到相关课程的信息<br/>请确认输入信息是否有误<br/>')
            self.msg.setAlignment(Qt.AlignCenter)
            self.centerLayout.addWidget(self.msg)
            return None
        
        self.rownum = len(data)
        self.showtable = QTableWidget(self.rownum, 6)  
        self.showtable.setHorizontalHeaderLabels(['', '课程号', '课程名', '教师号', '教师', '上课时间'])
        self.rbtns = []
        for i in range(self.rownum):
            self.rbtns.append(QRadioButton())
            self.showtable.setCellWidget(i, 0, self.rbtns[i])
            for j in range(1, 6):
                self.showtable.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j-1]))
        
        #设置水平方向表格为自适应的伸缩模式
        self.showtable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # 将表格变为禁止编辑
        self.showtable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置表格整行选中
        self.showtable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.centerLayout.addWidget(self.showtable)
        
        self.selectbtn = QPushButton('选课确认')
        self.selectbtn.clicked.connect(self.onSelect)
        
        self.bottom = QWidget()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addWidget(self.selectbtn)
        hbox.addStretch(1)
        hbox.addStretch(1)
        hbox.addStretch(1)
        self.bottom.setLayout(hbox)

        self.centerLayout.addWidget(self.bottom)

    def onSelect(self):

        for i in range(self.rownum):
            if self.rbtns[i].isChecked() == True:
                reply = QMessageBox.question(self, '提示', '确认选课', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.No:
                    return None
                kh = self.showtable.item(i, 1).text()
                gh = self.showtable.item(i, 3).text()
                flag = util.selectCourse(self.usr, self.term, kh, gh)
                if flag == True:
                    QMessageBox.information(self, '恭喜', '选课成功', QMessageBox.Yes)
                else:
                    QMessageBox.information(self, '抱歉', '课时冲突', QMessageBox.Yes)
                return None
    
        QMessageBox.warning(self, 'warning', '对不起你没有选择任何课程', QMessageBox.Yes)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    selecCoure = SelectCourse(usr='1102', term=term)
    selecCoure.resize(700, 450)
    selecCoure.show() 
    sys.exit(app.exec_())
