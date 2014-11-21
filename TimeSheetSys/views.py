# -*- coding: utf-8 -*-
'''
Views Timesheet模块视图方法包
@summary: Timesheet模块的view方法
'''

from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
import time, datetime
from PillarsCGSystem import common


def index(request):
    context = {}
    if common.user_flag(request.user) >= 2:
        return HttpResponseRedirect('/TimeSheetSys/timesheet')
    
    mission_list = Mission.objects.filter(del_flag=0)
    context['mission_count'] = len(mission_list)
    context['mission_list'] = mission_list
    
    status_list = Actual_Status.objects.filter()
    context['status_count'] = len(status_list)
    context['status_list'] = status_list
    
    
    return render_to_response('TimeSheetSys/index.html', context, context_instance=RequestContext(request))
    

#Timesheet
#用户编辑状态
def timesheet(request):
    
    context={}
    
    if request.method == 'GET':
        #当前用户当天
        context['id'] = request.user.id
        context['username'] = request.user.username
        context['firstname'] = request.user.first_name
        
        context['date'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        context['editable'] = True
        context['mode'] = 'edit'
        context['pre_status'] = 'none'
        
        c = Confirm.objects.get(user = request.user)
        context['rank_require'] = c.rank_require
        
        return render_to_response('TimeSheetSys/timesheet2.html',context,context_instance=RequestContext(request))

#审核状态
def timesheet_viewmode(request):
    context={}

    if request.method == 'GET':
        
        #查看当前用户是否有权限
        c = Confirm.objects.get(user = request.user)
        if c.rank != 0:
            #查看指定用户的日历
            uid = request.GET['uid']
            context['id'] = uid
            context['username'] = User.objects.get(id=uid).username
            context['firstname'] = User.objects.get(id=uid).first_name
            
            date = request.GET['date']
            if date == 'today':
                date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            context['date'] = date
            context['editable'] = False
            context['mode'] = 'judge'
            context['rank'] = c.rank
            cr = Confirm.objects.get(user = User.objects.get(id = uid))
            context['rank_require'] = cr.rank_require
            context['pre_status'] = 'none'
            
            return render_to_response('TimeSheetSys/timesheet2.html',context,context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/TimeSheetSys/timesheet')

#审核修改状态
def timesheet_viewedit(request):
    context={}

    if request.method == 'GET':
        
        #查看当前用户是否有权限
        c = Confirm.objects.get(user = request.user)
        if c.rank != 0:
            #查看指定用户的日历
            uid = request.GET['uid']
            context['id'] = uid
            context['username'] = User.objects.get(id=uid).username
            context['firstname'] = User.objects.get(id=uid).first_name
            
            date = request.GET['date']
            if date == 'today':
                date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            context['date'] = date
            context['editable'] = True
            context['mode'] = 'viewedit'
            context['rank'] = c.rank
            cr = Confirm.objects.get(user = User.objects.get(id = uid))
            context['rank_require'] = cr.rank_require
            context['pre_status'] = 'none'
            
            try:
                daily = Actual_Daily.objects.get(user=User.objects.get(id=uid), date=date)
                #保存原状态
                context['pre_status'] = daily.status.id
                #将daily状态改为编辑中
                daily.status = Actual_Status.objects.get(id=1)
                daily.save()
            except:
                return render_to_response('TimeSheetSys/timesheet2.html',context,context_instance=RequestContext(request))
            return render_to_response('TimeSheetSys/timesheet2.html',context,context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/TimeSheetSys/timesheet')
        
#timesheet审核用户列表
def timesheet_users(request):
    context={}
    
    #判定用户是否有权限进入
    user = request.user
#    print user.first_name
    c = Confirm.objects.get(user=user)
    if c.rank == 0:
        return HttpResponseRedirect('/TimeSheetSys/timesheet')
    else:
        return render_to_response('TimeSheetSys/timesheet_users.html',context,context_instance=RequestContext(request))

#timesheet报表
def timesheet_report(request):
    context={}
    print 'timesheet_report'
    
    #判定用户是否有权限进入
    user = request.user
#    print user.first_name
    c = Confirm.objects.get(user=user)
    if c.rank == 0:
        return HttpResponseRedirect('/TimeSheetSys/timesheet')
    else:
        context['uid'] = request.GET['uid']
        context['startdate'] = request.GET['startdate']
        context['enddate'] = request.GET['enddate']

        return render_to_response('TimeSheetSys/report.html',context,context_instance=RequestContext(request))

#timesheet统计
def timesheet_statistic(request):
    context={}
    print 'timesheet_statistic'
    
    #判定用户是否有权限进入
    user = request.user
#    print user.first_name
    c = Confirm.objects.get(user=user)
    if c.rank == 0:
        return HttpResponseRedirect('/TimeSheetSys/timesheet')
    else:
        uid = request.GET['uid']
         
        context['uid'] = uid
        context['username'] = User.objects.get(id=uid).first_name
        context['startdate'] = request.GET['startdate']
        context['enddate'] = request.GET['enddate']
        
        #当前时间
#        date = time.strftime('%Y-%m-%d',)
#        currentTime = datetime.date.today()
#        
#        
#        startTime = currentTime.replace(month = currentTime.month - 1)
#        endTime = currentTime.replace(month = currentTime.month - 1)
        
        #

        return render_to_response('TimeSheetSys/statistic.html',context,context_instance=RequestContext(request))
    

def timesheet_taskstatistic(request):
    context={}
    print 'timesheet_taskstatistic'
    
    #判定用户是否有权限进入
    user = request.user
#    print user.first_name
    c = Confirm.objects.get(user=user)
    if c.rank == 0:
        return HttpResponseRedirect('/TimeSheetSys/timesheet')
    else:
        context['startdate'] = request.GET['startdate']
        context['enddate'] = request.GET['enddate']
        
        return render_to_response('TimeSheetSys/taskStatistic.html',context,context_instance=RequestContext(request))
    
    