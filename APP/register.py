# -*- coding: utf-8 -*-
'''
# Created on Feb-07-20 23:23
# register.py
# @author: ss
'''

'''
这是一个注册对话窗口
'''


from PyQt5 import QtWidgets, QtCore, QtGui 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QStackedWidget,
                QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                QLabel, QLineEdit,
                QFrame,
                QRadioButton,
                QPushButton, QMessageBox, 
                QAction, QApplication)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from APP.common import center
from BACK.util import register
import login

class RegisterWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loginWindow = None
    
    def initUI(self):

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)

        user = QLabel('账号: ')
        pwd = QLabel('密码: ')
        cpwd = QLabel('确认：')

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText('请输入学号')

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入密码')
        self.pwdInput.setEchoMode(QLineEdit.Password) #密码不以明文显示

        self.cpwdInput = QLineEdit()
        self.cpwdInput.setPlaceholderText('请输入密码')
        self.cpwdInput.setEchoMode(QLineEdit.Password)

        self.registerButton = QPushButton('注册', self)
        self.registerButton.setIcon(QIcon('./image/sgin.png'))
        self.registerButton.clicked.connect(self.onRegister)

        self.loginButton = QPushButton('登录', self)
        self.loginButton.setFont(QFont('黑体'))
        # self.loginButton.setStyleSheet("border:2px; border-radius:10px; background-color:rgba(0,0,255,200)")
        self.loginButton.setIcon(QIcon('./image/login.png'))
        self.loginButton.clicked.connect(self.onLogin)

        formlayout = QFormLayout()
        formlayout.addRow(user, self.userInput)
        formlayout.addRow(pwd, self.pwdInput)
        formlayout.addRow(cpwd, self.cpwdInput)

        self.stubtn = QRadioButton('学生')
        self.teabtn = QRadioButton('教师')

        rhbox = QHBoxLayout()
        rhbox.addStretch(1)
        rhbox.addWidget(self.stubtn)
        rhbox.addWidget(self.teabtn)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.registerButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(formlayout)
        vbox.addLayout(rhbox)
        vbox.addLayout(hbox)
        vbox.setStretchFactor(formlayout, 5)

        centerFrame.setLayout(vbox)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addStretch(1)
        hbox1.addWidget(self.loginButton)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(centerFrame)
        vbox1.addLayout(hbox1)

        self.setLayout(vbox1)

        self.resize(350, 250) # 设置窗口大小
        center(self) # 使得串口显示在屏幕中央
        self.setFont(QFont("宋体", 11))
        self.setWindowTitle('账号注册')
        self.setWindowIcon(QIcon('./image/sgin.png'))
    
    def onLogin(self):
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()
    
    def onRegister(self):

        usr = self.userInput.text()
        pwd = self.pwdInput.text()
        cpwd = self.cpwdInput.text()

        if self.stubtn.isChecked() == False and self.teabtn.isChecked() == False:
             QMessageBox.warning(self, 'Warining', '没有选择您的身份', QMessageBox.Yes)
        else:
            flag = register(usr, pwd, cpwd, self.stubtn.isChecked())
            if flag == 1:
                QMessageBox.warning(self, 'Warining', '两次输入密码不一致', QMessageBox.Yes)
            elif flag == 2:
                QMessageBox.warning(self, 'Warining', '该用户已注册', QMessageBox.Yes)
            elif flag == 3:
                if self.stubtn.isChecked():
                    QMessageBox.warning(self, 'Sorry', '抱歉, 该学生用户不存在', QMessageBox.Yes)
                else:
                    QMessageBox.warning(self, 'Sorry', '抱歉, 该教师用户不存在', QMessageBox.Yes)
            elif flag == 0:
                QMessageBox.information(self, '恭喜', '注册成功', QMessageBox.Yes, QMessageBox.Yes)
                self.onLogin()
            elif flag == -1:
                QMessageBox.warning(self, 'Warining', '输入不能为空', QMessageBox.Yes)
            else:
                QMessageBox.warning(self, 'Warining', '你程序写烂了', QMessageBox.Yes)

        self.userInput.clear()
        self.pwdInput.clear()
        self.cpwdInput.clear()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    registerWindow = RegisterWindow()
    loginWindow = login.LoginWindow()
    loginWindow.registerWindow = registerWindow
    registerWindow.loginWindow = loginWindow
    registerWindow.show()
    sys.exit(app.exec_())