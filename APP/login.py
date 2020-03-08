# -*- coding: utf-8 -*-
'''
# Created on Feb-06-20 16:04
# login.py
# @author: ss
'''

'''
应用程序登录界面
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, 
                QLabel, QLineEdit, QApplication, QPushButton,
                QFrame,
                QRadioButton,
                QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))

from APP.common import center
import register
from BACK.util import login

# 注意类型
class LoginWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.registerWindow = None
        self.mainWindow = None
    
    def initUI(self):
        
        logomap = QPixmap('./image/shu.jpg')

        logolbl = QLabel(self)
        logolbl.setPixmap(logomap)
        logolbl.setScaledContents(True) # 图片自适应标签大小

        title = QLabel('学生课程成绩管理系统')
        title.setAlignment(Qt.AlignCenter) # 设置中间对其
        title.setFont(QFont("Microsoft YaHei", 15)) 

        user = QLabel('账号: ')
        pwd = QLabel('密码: ')

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText('请输入学号')

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入密码')
        self.pwdInput.setEchoMode(QLineEdit.Password) #密码不以明文显示

        # 设置登录按钮
        self.loginButton = QPushButton('登录', self)
        self.loginButton.setIcon(QIcon('./image/login.png'))
        self.loginButton.clicked.connect(self.loginCheck)
        
        self.cannelButton = QPushButton('取消', self)
        self.cannelButton.setIcon(QIcon('./image/cannel.png'))
        self.cannelButton.clicked.connect(self.cannelCheck)

        self.registerButton = QPushButton('注册', self)
        self.registerButton.setFont(QFont('黑体'))
        self.registerButton.setIcon(QIcon('./image/sgin.png'))
        self.registerButton.clicked.connect(self.onRegister)

        # 设置网格布局
        gridlayout = QGridLayout()
        gridlayout.addWidget(user, 0, 0, 1, 1)
        gridlayout.addWidget(pwd, 1, 0, 1, 1)
        gridlayout.addWidget(self.userInput, 0, 1, 1, 3)
        gridlayout.addWidget(self.pwdInput, 1, 1, 1, 3)
        self.stubtn = QRadioButton('学生')
        self.teabtn = QRadioButton('教师')

        rhbox = QHBoxLayout()
        rhbox.addWidget(self.stubtn)
        rhbox.addWidget(self.teabtn)

        gridlayout.addLayout(rhbox, 2, 1, 3, 3)

        rightmidFrame = QFrame()
        rightmidFrame.setFrameShape(QFrame.WinPanel)
        rightmidFrame.setLayout(gridlayout)

        # 嵌套水平布局
        hbox = QHBoxLayout()
        hbox.addWidget(self.loginButton)
        hbox.addWidget(self.cannelButton)

        vboxright = QVBoxLayout()
        vboxright.addWidget(title)
        vboxright.addWidget(rightmidFrame)
        vboxright.addLayout(hbox)

        vbox1 = QVBoxLayout()
        vbox1.addLayout(vboxright)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1) # 增加一个伸缩因子
        hbox2.addWidget(self.registerButton)

        vbox1.addLayout(hbox2)
       
        #水平布局
        hbox1 = QHBoxLayout()
        hbox1.addWidget(logolbl)
        hbox1.addLayout(vbox1)
        # 设置整体布局
        self.setLayout(hbox1)
        
        self.resize(450, 300) # 设置窗口大小
        center(self)    #使得串口显示在屏幕中央
        self.setFont(QFont("宋体", 11))
        self.setWindowTitle('欢迎使用')
        self.setWindowIcon(QIcon('./image/j1.png'))

    def loginCheck(self):

        usr = self.userInput.text()
        pwd = self.pwdInput.text()

        if usr == '':
            QMessageBox.warning(self, "warning", "用户名不能为空", QMessageBox.Yes)
        elif pwd == '':
            QMessageBox.warning(self, "warning", "密码不能为空", QMessageBox.Yes)
        else:
            if self.stubtn.isChecked() == False and self.teabtn.isChecked() == False:
                QMessageBox.warning(self, "warning", "请选择您的身份", QMessageBox.Yes)
            else:
                flag = login(usr, pwd, self.stubtn.isChecked()) 
                if flag == 0:
                    if self.mainWindow is not None:
                        self.close()
                        self.mainWindow.usr = usr
                        self.mainWindow.isstu = self.stubtn.isChecked()
                        self.mainWindow.showbottom()
                        self.mainWindow.show()
                elif flag == 1:
                    QMessageBox.warning(self, 'Sorry', '抱歉, 您输入的密码有误', QMessageBox.Yes)
                elif flag == 2:
                    QMessageBox.warning(self, 'Sorry', '抱歉, 该用户名不存在', QMessageBox.Yes)
                elif flag == 3:
                    if self.stubtn.isChecked():
                        QMessageBox.warning(self, 'Sorry', '抱歉, 该学生用户不存在', QMessageBox.Yes)
                    else:
                        QMessageBox.warning(self, 'Sorry', '抱歉, 该教师用户不存在', QMessageBox.Yes)
                elif flag == -2:
                    QMessageBox.warning(self, 'Oh my god', '你程序bug了, 快维修吧', QMessageBox.Yes)

        self.userInput.clear()
        self.pwdInput.clear()

    def cannelCheck(self):
        reply = QMessageBox.question(self, "message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 第一个字符串显示在消息框的标题栏，第二个字符串显示在对话框，第三个参数是消息框的俩按钮，最后一个参数是默认按钮，这个按钮是默认选中的。返回值在变量reply里。
        if reply == QMessageBox.Yes:
            self.close()
    
    def onRegister(self):
        
        if self.registerWindow is not None:
            self.close()
            self.registerWindow.show() 

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    registerWindow = register.RegisterWindow()
    loginWindow.registerWindow = registerWindow
    registerWindow.loginWindow = loginWindow
    loginWindow.show()
    sys.exit(app.exec_())
