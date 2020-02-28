# -*- coding: utf-8 -*-
'''
# Created on Feb-28-20 14:13
# util.py
# @author: ss
# @description: 提供通用数据接口模块
'''

import sys
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))

from BACK.util import getclasstime
from BACK.course import (searchCourse, selectCourse, dropSelectCourse, showSelectCourse, finishedCourse)
from BACK.course import (openCourse, delOpenCourse)
