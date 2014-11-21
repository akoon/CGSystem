# -*- coding: utf-8 -*-
from __future__ import division 
from django.http import HttpResponse
from django.utils import simplejson
from models import *
import datetime, time
from django.utils import timezone
import string
from PillarsCGSystem.globalvar import *
from TimeSheetSys.models import Confirm
from PillarsCGSystem.common import dateCompare

#查询当前用户的假条
def leave_detail(request):
    info = {}
    if request.method == 'GET':
        list = []
        i = 0
        user = request.user
        #查询当前用户的假条
        leave = Leave.objects.filter(user=user, status__in=[0,1,3]).order_by('-endtime')
        for l in leave:
            i += 1
            d = {}
            d['id'] = l.id
            d['username'] = l.user.first_name
            d['userid'] = l.user.id
            d['reason'] = l.reason
            d['starttime'] = timezone.localtime(l.startime).strftime('%Y-%m-%d %H:%M:%S')
            d['endtime'] = timezone.localtime(l.endtime).strftime('%Y-%m-%d %H:%M:%S')
            d['registertime'] = timezone.localtime(l.registertime).strftime('%Y-%m-%d')
            d['status'] = l.l_status()
            d['sid'] = l.status
            d['interval'] = l.interval
            d['tid'] = l.type.id
            d['type'] = l.type.name
            
            if l.status == 0:
                d['ops'] = "<a onclick='submitLeave("+str(l.id)+")'>提交</a>"
            if l.status == 3:
                d['ops'] = "<a onclick='submitLeave("+str(l.id)+")'>再提交</a>"
            
            list.append(d)
            
        #查询是否有审核权限
         #判断是否有审核的权限
        c = Confirm.objects.get(user=user)
        if c.rank != 0:
            enlisted = Confirm.objects.filter(superior=c.user)
            for e in enlisted:
                #添加需要审核的用户
                leave = Leave.objects.filter(user=e.user, status=1).order_by('-endtime')
                for l in leave:
                    i += 1
                    d = {}
                    d['id'] = l.id
                    d['username'] = l.user.first_name
                    d['userid'] = l.user.id
                    d['reason'] = l.reason
                    d['starttime'] = timezone.localtime(l.startime).strftime('%Y-%m-%d %H:%M:%S')
                    d['endtime'] = timezone.localtime(l.endtime).strftime('%Y-%m-%d %H:%M:%S')
                    d['registertime'] = timezone.localtime(l.registertime).strftime('%Y-%m-%d')
                    d['status'] = l.l_status()
                    d['interval'] = l.interval
                    d['tid'] = l.type.id
                    d['type'] = l.type.name
                    d['ops'] = "<a onclick='leaveJudgementAck("+str(l.id)+")'>审核通过</a>&nbsp<a onclick='leaveJudgementNeg("+str(l.id)+")'>审核不通过</a>"
                    if l.status == 1:
                        list.append(d)
        
        #最高权限审核自身
        if c.rank == c.rank_require:
            try:
                l = Leave.objects.get(user=user)
                i += 1
                d = {}
                d['id'] = l.id
                d['username'] = l.user.first_name
                d['userid'] = l.user.id
                d['reason'] = l.reason
                d['starttime'] = timezone.localtime(l.startime).strftime('%Y-%m-%d %H:%M:%S')
                d['endtime'] = timezone.localtime(l.endtime).strftime('%Y-%m-%d %H:%M:%S')
                d['registertime'] = timezone.localtime(l.registertime).strftime('%Y-%m-%d')
                d['status'] = l.l_status()
                d['interval'] = l.interval
                d['tid'] = l.type.id
                d['type'] = l.type.name
                d['ops'] = "<a onclick='leaveJudgementAck("+str(l.id)+")'>审核通过</a>&nbsp<a onclick='leaveJudgementNeg("+str(l.id)+")'>审核不通过</a>"
                if l.status == 1:
                    list.append(d)
            except:
                pass
            
        info['total'] = i
        info['rows'] = list

    return HttpResponse(simplejson.dumps(info))

#返回请假类型
def leavetype_read(request):
    info = []
    if request.method == 'GET':
        leave = LeaveType.objects.all()
        for l in leave:
            d = {}
            d['id'] = l.id
            d['name'] = l.name
            info.append(d)
            
    return HttpResponse(simplejson.dumps(info))

#新建假条
def leave_create(request):
    info = {}
    if request.method == 'POST':
        try:
            typeid = request.POST.get('type','')
            reason = request.POST.get('reason','')
            startime = request.POST.get('starttime','')
            endtime = request.POST.get('endtime','')
            user = request.user
            registertime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            type = LeaveType.objects.get(id=typeid)
            interval = 0
            days = request.POST.get('intervalDay','')
            hours = request.POST.get('intervalHour','')
            
            if days != None and hours != None:
                interval = (int(days) * 8) + int(hours)
            
            if startime <= endtime:
                Leave.objects.create(user=user,startime=startime, endtime=endtime, registertime=registertime, reason=reason, type=type, status=0, interval=interval)        
                info['success'] = True
                info['message'] = '创建成功'
            else:
                info['success'] = False
                info['message'] = '开始日期必须小于结束日期'
                
        except:
            info['success'] = False
            info['message'] = '创建失败'
            
    return HttpResponse(simplejson.dumps(info))

#提交假条
def leave_commit(request):
    info = {}
    if request.method == 'POST':
        try:
            id = request.POST.get('id','')
            
            leave = Leave.objects.get(id=id)
            leave.status = 1
            leave.save()
            
            info['success'] = True
            info['message'] = '提交成功'
        except:
            info['success'] = False
            info['message'] = '提交失败'
            
    return HttpResponse(simplejson.dumps(info))

#审核假条
def leave_judge(request):
    info = {}
    if request.method == 'POST':
        try:
            id = request.POST.get('id','')
            option = request.POST.get('option','')
            leave = Leave.objects.get(id=id)
            
            if option == 'ack':
                leave.status = 2
                info['success'] = True
                info['message'] = '审核通过'
            elif option == 'neg':
                leave.status = 3
                info['success'] = True
                info['message'] = '审核不通过'
            else:
                pass
            leave.require = request.user
            leave.save()
            
            
        except:
            info['success'] = False
            info['message'] = '审核失败'
            
    return HttpResponse(simplejson.dumps(info))

#修改假条
def leave_update(request):
    info = {}
    if request.method == 'POST':
        try:
            id = request.POST.get('id','')
            typeid = request.POST.get('type','')
            reason = request.POST.get('reason','')
            startime = request.POST.get('starttime','')
            endtime = request.POST.get('endtime','')
            user = request.user
            type = LeaveType.objects.get(id=typeid)
            interval = 0
            days = request.POST.get('intervalDay','')
            hours = request.POST.get('intervalHour','')
            
            if days != None and hours != None:
                interval = (int(days) * 8) + int(hours)
            
            if startime <= endtime:
                leave = Leave.objects.get(id=id)
            
                leave.type = type
                leave.reason = reason
                leave.startime = startime
                leave.endtime = endtime
                leave.interval = interval
                
                leave.save()
                
                info['success'] = True
                info['message'] = '修改成功'
            else:
                info['success'] = False
                info['message'] = '开始日期必须小于结束日期'
                
            
        except:
            info['success'] = False
            info['message'] = '修改失败'
            
    return HttpResponse(simplejson.dumps(info))
    
#查询已归档假条
def archived_leave(request):
    info = {}
    if request.method == 'GET':
        
        list = []
        i = 0
        user = request.user
        
        #用户查询自己的归档
        leave = Leave.objects.filter(user=user, status__in=[2,3]).order_by('-endtime')
        for l in leave:
            i += 1
            d = {}
            d['id'] = l.id
            d['username'] = l.user.first_name
            d['userid'] = l.user.id
            d['reason'] = l.reason
            d['starttime'] = timezone.localtime(l.startime).strftime('%Y-%m-%d %H:%M:%S')
            d['endtime'] = timezone.localtime(l.endtime).strftime('%Y-%m-%d %H:%M:%S')
            d['registertime'] = timezone.localtime(l.registertime).strftime('%Y-%m-%d')
            d['status'] = l.l_status()
            d['interval'] = l.interval
            
            list.append(d)
                
        
        c = Confirm.objects.get(user=user)
        if c.rank != 0:
            #管理员查询所有成员的归档
            enlisted = Confirm.objects.filter(superior=c.user)
            for e in enlisted:
                #添加需要审核的用户
                leave = Leave.objects.filter(user=e.user, status__in=[2,3]).order_by('-endtime')
                for l in leave:
                    i += 1
                    d = {}
                    d['id'] = l.id
                    d['username'] = l.user.first_name
                    d['userid'] = l.user.id
                    d['reason'] = l.reason
                    d['starttime'] = timezone.localtime(l.startime).strftime('%Y-%m-%d %H:%M:%S')
                    d['endtime'] = timezone.localtime(l.endtime).strftime('%Y-%m-%d %H:%M:%S')
                    d['registertime'] = timezone.localtime(l.registertime).strftime('%Y-%m-%d')
                    d['status'] = l.l_status()
                    d['interval'] = l.interval
                    
                    list.append(d)
            
        info['total'] = i
        info['rows'] = list

    return HttpResponse(simplejson.dumps(info))

#删除假条
def leave_destroy(request):
    info = {}
    if request.method == 'POST':
        try:
            id = request.POST.get('id','')
            
            leave = Leave.objects.get(id=id)
            leave.delete()
            
            info['success'] = True
            info['message'] = '删除成功'
        except:
            info['success'] = False
            info['message'] = '删除失败'
            
    return HttpResponse(simplejson.dumps(info))

