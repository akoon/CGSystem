# -*- coding: utf-8 -*-

'''
Model OA子系统模型类包
@summary: OA子系统的Model类
'''

from django.db import models
from django.contrib.auth.models import User
import datetime

#请假类型
class LeaveType(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank = True)

#请假单
class Leave(models.Model):
    user = models.ForeignKey(User)
    type = models.ForeignKey(LeaveType)
    reason = models.TextField(null=True, blank = True)
    startime = models.DateTimeField()
    endtime = models.DateTimeField()
    registertime = models.DateField()
    require = models.ForeignKey(User, related_name='require', null=True)
    status = models.IntegerField()
    interval = models.IntegerField()
    
    def l_status(self):
        if self.status == 0:
            return '新建'
        if self.status == 1:
            return '已提交'
        if self.status == 2:
            return '审核通过'
        if self.status == 3:
            return '审核不通过'
        
    