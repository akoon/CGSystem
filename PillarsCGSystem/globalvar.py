# -*- coding: utf-8 -*-
'''
此文件中包含项目中函数调用的全局变量
'''

Errors=None     #文件复制错误信息

Queue=[]        #文件复制队列

ThreadStatus=False #复制线程启动状态

ats = None      #渲染服务器操作终端句柄

MOUNTDIR = '/new'

PROJECTDIR = MOUNTDIR + '/Project'

#Timesheet统计类
class Actual_Task_Statisic():
    def __init__(self):
        self.type = 0   # 1: task   2: mission
        self.task = None
        self.hours = 0
        self.title = ''