# -*- coding: utf-8 -*-
'''
Model 基础数据模型类包
@summary: 本类包包含系统中基础数据的Model类
'''
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name=models.CharField(max_length=64)
    parent=models.IntegerField()
    desc=models.TextField(null=True)

class Position(models.Model):
    name=models.CharField(max_length=64, unique=True)
    desc=models.TextField(null=True, blank=True)

#扩展User字段 
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    # Other fields here
    department = models.ForeignKey(Department, null=True)
    position = models.ForeignKey(Position, null=True)
    sex = models.IntegerField(null=True) #0女 1男
    phone = models.CharField(max_length=64, null=True)
    thum = models.FileField(upload_to='thumbnail/user', max_length=100, null=True)
    home = models.CharField(max_length=500, null=True)
    birthday = models.DateField(null=True, blank=True)
    bloodtype = models.IntegerField(null=True, blank=True)
    constellation = models.IntegerField(null=True, blank=True)
    hobby = models.CharField(max_length=128, null=True, blank=True)
    seatnumber = models.CharField(max_length=64, null=True, blank=True)
    lastloginip = models.IPAddressField(max_length=15, null = True)
    
    def case_bloodtype(self):
        if self.bloodtype == 0:
            return 'O型血'
        elif self.bloodtype == 1:
            return 'A型血'
        elif self.bloodtype == 2:
            return 'B型血'
        elif self.bloodtype == 3:
            return 'AB型血'
        else:
            return '其他'
 
    def case_constellation(self):
        if self.constellation == 0:
            return '白羊座'
        if self.constellation == 1:
            return '金牛座'
        if self.constellation == 2:
            return '双子座'
        if self.constellation == 3:
            return '巨蟹座'
        if self.constellation == 4:
            return '狮子座'
        if self.constellation == 5:
            return '处女座'
        if self.constellation == 6:
            return '天秤座'
        if self.constellation == 7:
            return '天蝎座'
        if self.constellation == 8:
            return '射手座'
        if self.constellation == 9:
            return '魔羯座'
        if self.constellation == 10:
            return '水瓶座'
        if self.constellation == 11:
            return '双鱼座'
        else:
            return '未知'

#反馈意见        
class Feedback(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    creat_time = models.DateTimeField()
    
    