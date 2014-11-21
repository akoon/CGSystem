# -*- coding: utf-8 -*-
'''
Model Canendar子系统模型类包
@summary: Canendar子系统的Model类
'''

from django.db import models
from django.contrib.auth.models import User

class Schedule_Status(models.Model):
    name=models.CharField(max_length=64)#0.未完成  1.已完成

class Schedule_Daily(models.Model):
    date=models.DateField()
    user=models.ForeignKey(User) 

class Schedule_Task(models.Model):
    daily=models.ForeignKey(Schedule_Daily)
    title = models.TextField(max_length=50)
    desc=models.TextField()
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    status=models.ForeignKey(Schedule_Status)
    user=models.ManyToManyField(User, null=True)
    