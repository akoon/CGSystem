# -*- coding: utf-8 -*-
'''
Model Timesheet子系统模型类包
@summary: Timesheet子系统的Model类
'''
from django.db import models
from django.contrib.auth.models import User
from BaseSys.models import *
from ProjectManSys.models import *

# Timesheet相关
#固定任务    
class Mission(models.Model):
    name=models.CharField(max_length=64)
    del_flag = models.BooleanField(default=False)
 
#task状态
class Actual_Status(models.Model):
    name=models.CharField(max_length=64)#1.正在记录  2.已确定 3.通过审核 4.审核未通过 5.已冻结
    color=models.IntegerField()
    
class Actual_Daily(models.Model):
    date=models.DateField()
    user=models.ForeignKey(User)
    status=models.ForeignKey(Actual_Status)
    rejected_by=models.IntegerField(null=True)    
     
class Actual_Task(models.Model):
    daily=models.ForeignKey(Actual_Daily)
    type=models.IntegerField() # 1. task 2. mission
    task=models.ForeignKey(Task,null=True)
    mission=models.ForeignKey(Mission,null=True)
    title = models.TextField(max_length=50)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    desc=models.TextField()
    overtime=models.BooleanField(default=False)
    
#多级审核列表
class Confirm(models.Model):
    user = models.ForeignKey(User)
    superior = models.ForeignKey(User, related_name='superior', null=True)
    rank = models.IntegerField()
    rank_require = models.IntegerField()
    
