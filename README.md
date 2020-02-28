## 学生选课成绩管理系统

### 项目进展
```
    2020-02-28 第一次实现(后续代更)
```

### 项目简介
```
    这是一个基于pyqt5实现的可视化学生选课成绩管理系统。
    用户面向：学生和老师
    主要功能模块有课程管理和成绩管理
    课程管理模块：
    学生可以进行本学期的课程查询，选课，退课，课程表查看已经查看所修过课程
    教师可以开设本学期课程或者撤销本学期课程
    成绩管理模块：
    学生查看学期成绩单
    教师评定学生成绩

    项目意义：为了完成俺的数据库期末大作业的动手实践(逃)
```

### 项目环境
```
    项目环境: win10 + python3.7 + mysql
    python所需的包有: Pyqt5, pymsql, numpy
     
    项目所有数据库：
    基于(数据库原理一)
    1. 使用的六个基本数据库: 学生表，教师表，院系表，课程表，开课表，选课表.
    2. 新创建的一个用户表。
    具体创建参见 create.sql
```

### 项目目录
```
    --APP(程序运行主目录)
        main.py
        login.py
        register.py
    --BACK(后台数据库接口实现)
    --Course(课程管理模块)
    --Score(成绩管理模块)
    --image(程序图标存放)
```