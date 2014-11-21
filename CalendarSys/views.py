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
import time

# 用户计划
def calendar(request):
    context={}
    
    if request.method == 'GET':
        
        #当前用户当天
        context['id'] = request.user.id
        context['username'] = request.user.username
        context['date'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        context['editable'] = True
        context['mode'] = 'edit'
        context['pre_status'] = 'none'

        context['rank_require'] = 1
        
        return render_to_response('CalendarSys/calendar.html',context,context_instance=RequestContext(request))

