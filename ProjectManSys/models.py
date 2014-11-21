# -*- coding: utf-8 -*-
'''
Model 项目管理子系统模型类包
@summary: 项目管理子系统的Model类
'''
from django.db import models
from django.contrib.auth.models import User
from BaseSys.models import *
import datetime

#状态表
class Status(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank = True)
    type = models.IntegerField()
    #状态类型: -1 项目    -2 资产    -3 任务
    
#类型
class Types(models.Model):
    name = models.CharField(max_length=64)  
    desc = models.TextField(null=True, blank = True)
    type = models.IntegerField()
    #类型: -1 项目    -2 资产    -3 任务

#资产组
class Group(models.Model):
    name = models.CharField(max_length=64)
    desc = models.TextField(null=True, blank = True)

#资产模版
class Templ(models.Model):
    name = models.CharField(max_length=64)
    parent = models.IntegerField()
    desc = models.TextField(null=True, blank = True)
    
#项目
class Project(models.Model):
    name = models.CharField(max_length=64)
    types = models.ForeignKey(Types,null=True)
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
    desc = models.TextField(null=True, blank = True)    
    priority = models.IntegerField(default=10)
    creat_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    thum = models.FileField(upload_to='thumbnail/project',null=True) 
    is_active = models.BooleanField(default=True)

#    def save(self):
#        create_time = datetime.datetime.now().strftime('%Y-%m-%d')
#        super.save()
        
#资产组
class Groups(models.Model):
    name = models.CharField(max_length=64)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    project = models.ForeignKey(Project, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

#项目人员
class ProjectPeople(models.Model):
    project = models.ForeignKey(Project)
    users = models.ManyToManyField(User)

#项目部门和职位
class ProjectDePo(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    department = models.ForeignKey(Department,null=True)
    position = models.ForeignKey(Position,null=True)
   
#资产
class TaskGroup(models.Model):
    name = models.CharField(max_length=64)
    namedesc = models.CharField(max_length=128, null=True, blank=True)
    types = models.ForeignKey(Types,null=True)
    status = models.ForeignKey(Status)
    project = models.ForeignKey(Project)
    templ = models.ForeignKey(Templ,null=True)
    desc = models.TextField(null=True)
    group = models.ForeignKey(Groups)
    thum = models.FileField(upload_to='thumbnail/group', null=True) 
    is_active = models.BooleanField(default=True)

#资产关联
class TaskGroupRel(models.Model):
    src = models.ForeignKey(TaskGroup, related_name="srcTaskGroup")
    desc = models.ForeignKey(TaskGroup, related_name="descTaskGroup")

#任务  
class Task(models.Model):
    name = models.CharField(max_length=64)  
    types = models.ForeignKey(Types,null=True)
    status = models.ForeignKey(Status,null=True)
    user = models.ManyToManyField(User,null=True)
    project = models.ForeignKey(Project)
    task_group = models.ForeignKey(TaskGroup)
    priority = models.IntegerField(default=10)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    desc = models.TextField(null=True) 
    percent = models.IntegerField(null=True)
    version = models.CharField(max_length=3,null=True)
    path = models.CharField(max_length=128,null=True) 
    qc_flag = models.IntegerField(null=True)
    publish_status = models.IntegerField(null=True)
    review_status = models.IntegerField(default=0)
    use_time = models.CharField(max_length=3,null=True) 
    is_active = models.BooleanField(default=True)
    def qc(self):
        if self.qc_flag == 1:
            return '是'
        else:
            return '否'
    def p_status(self):
        if self.publish_status == 1:
            return '已发布'
        else:
            return '未发布'
    def r_status(self):
        if self.review_status == 0:
            return '未提交'
        if self.review_status == 1:
            return '已提交'
        if self.review_status == 2:
            return '审核未通过'
        if self.review_status == 3:
            return '审核已通过'

#任务图片       
class TaskImg(models.Model):
    task = models.ForeignKey(Task)
    version = models.CharField(max_length=3,null=True)
    thum = models.FileField(upload_to='thumbnail/task',null=True)
            
#任务版本    
class TaskVersion(models.Model):
    name = models.CharField(max_length=64)  
    types = models.ForeignKey(Types,null=True)
    status = models.ForeignKey(Status,null=True)
    user = models.ManyToManyField(User,null=True)
    project = models.ForeignKey(Project)
    task_group = models.ForeignKey(TaskGroup)
    priority = models.IntegerField(default=10)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    desc = models.TextField(null=True) 
    percent = models.IntegerField(null=True)    
    version = models.CharField(max_length=3,null=True)
    path = models.CharField(max_length=128,null=True) 
    qc_flag = models.IntegerField(null=True)
    publish_status = models.IntegerField(null=True)
    review_status = models.IntegerField(default=0)
    use_time = models.CharField(max_length=3,null=True) 
    publish_time = models.DateTimeField(null=True)
    task = models.ForeignKey(Task)

#审核相关
class TaskReview(models.Model):
    feedback = models.TextField(null=True)
    remark = models.TextField(null=True)
    review_time = models.DateTimeField(null=True)    
    task = models.ForeignKey(Task)

class Note(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    content = models.TextField(null=True)
    task = models.ForeignKey(Task)
    parent = models.IntegerField(default=0)
    important = models.IntegerField(default=0)

class Image(models.Model):
    img = models.FileField(upload_to='Image', null=True)
    
