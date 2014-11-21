# -*- coding: utf-8 -*-
'''
Views 初始化view
@summary: 初始化view
'''

from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import simplejson
from BaseSys.models import *
from PillarsCGSystem import common
from django.core.mail import send_mail
from django.conf import settings
# from PillarsCGSystem import settings

def index(request):
    context = {}
    return render_to_response('Initialization/index.html', context, context_instance=RequestContext(request))

def validate(request):
    context = {}
    if request.method == 'POST':
        # 提交表单
        pillars_id = request.POST['pillars_id']
        pillars_pwd = request.POST['pillars_pwd']
        pillars_sn = request.POST['pillars_sn']
        mac_address = common.get_mac_address()
        
        if common.validate_pillars_id(pillars_id, pillars_pwd, pillars_sn, mac_address):
            common.wirte_config('pillars', 'pillars_id', pillars_id)
            common.wirte_config('pillars', 'pillars_pwd', pillars_pwd)
            common.wirte_config('pillars', 'serialnumber', pillars_sn)
            common.wirte_config('pillars', 'mac_address', mac_address)
            common.wirte_config('initialization', 'setup', '1')
            return HttpResponseRedirect('/Initialization/0')
        else:
            #TODO: 验证失败，返回
            context['pillars_id'] = pillars_id
            context['pillars_pwd'] = pillars_pwd
            context['pillars_sn'] = pillars_sn
            return render_to_response('Initialization/validate.html', context, context_instance=RequestContext(request))
        
    else:
        return render_to_response('Initialization/validate.html', context, context_instance=RequestContext(request))
   

def setup0(request):
    context = {}
    return render_to_response('Initialization/setup0.html', context, context_instance=RequestContext(request))


def setup1(request):
    context = {}
    if request.method == 'POST':
        language = request.POST['language']
        timezone = request.POST['timezone']
        common.wirte_config('global', 'language', language)
        common.wirte_config('global', 'timezone', timezone)
        
        common.wirte_config('initialization', 'setup', '2')
        return HttpResponseRedirect('/Initialization/2')
    else:
        return render_to_response('Initialization/setup1.html', context, context_instance=RequestContext(request))


def setup2(request):
    
    context = {}
    if request.method == 'POST':
        EMAIL_HOST = request.POST['EMAIL_HOST']
        EMAIL_PORT = request.POST['EMAIL_PORT']
        EMAIL_HOST_USER = request.POST['EMAIL_HOST_USER']
        EMAIL_HOST_PASSWORD = request.POST['EMAIL_HOST_PASSWORD']
        EMAIL_USE_TLS = request.POST['EMAIL_USE_TLS']
        
        #发送测试邮件
        try:
            send_mail('Pillars System测试邮件', '邮件发送成功！', EMAIL_HOST_USER, [EMAIL_HOST_USER], False, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        except:
            context['EMAIL_HOST'] = EMAIL_HOST
            context['EMAIL_PORT'] = EMAIL_PORT
            context['EMAIL_HOST_USER'] = EMAIL_HOST_USER
            context['EMAIL_HOST_PASSWORD'] = EMAIL_HOST_PASSWORD
            context['EMAIL_USE_TLS'] = EMAIL_USE_TLS
            context['EMAIL_ERROR'] = '邮件测试失败！'
            return render_to_response('Initialization/setup2.html', context, context_instance=RequestContext(request))
        
        settings.EMAIL_HOST = EMAIL_HOST
        settings.EMAIL_PORT = EMAIL_PORT
        settings.EMAIL_HOST_USER = EMAIL_HOST_USER
        settings.EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
        settings.EMAIL_USE_TLS = EMAIL_USE_TLS
        
        common.wirte_config('email', 'EMAIL_HOST', EMAIL_HOST)
        common.wirte_config('email', 'EMAIL_PORT', EMAIL_PORT)
        common.wirte_config('email', 'EMAIL_HOST_USER', EMAIL_HOST_USER)
        common.wirte_config('email', 'EMAIL_HOST_PASSWORD', EMAIL_HOST_PASSWORD)
        common.wirte_config('email', 'EMAIL_USE_TLS', EMAIL_USE_TLS)
        
#         common.wirte_config('initialization', 'initialization', 'YES')
        common.wirte_config('initialization', 'setup', '3')
        return HttpResponseRedirect('/Initialization/3')
        
    else:
        return render_to_response('Initialization/setup2.html', context, context_instance=RequestContext(request))

def initialization_skip(request):
    common.wirte_config('initialization', 'setup', '3')
    common.wirte_config('email', 'is_skip', 'True')
    return HttpResponseRedirect('/Initialization/3')

def setup3(request):
    
    def app_info(app_name):
        info = {'img':'未知', 'name' :'未知', 'note': '未知' }
        if 'basesys' == app_name:
            info['img'] = 'BaseSys_6.png'
            info['name'] = 'Base Manager System'
            info['note'] = '基础管理子系统'
        elif 'projectmansys' == app_name:
            info['img'] = 'ProjectManSys_6.png'
            info['name'] = 'Project Manager System'
            info['note'] = '项目管理子系统'
        elif 'timesheetsys' == app_name:
            info['img'] = 'TimeSheetSys_6.png'
            info['name'] = 'Time Sheet System'
            info['note'] = '考勤管理子系统'
        elif 'calendersys' == app_name:
            info['img'] = 'CalendarSys_6.png'
            info['name'] = 'Calenday System'
            info['note'] = '日历管理子系统'
            
        return info
        
    context = {}
    if request.method == 'POST':
        common.wirte_config('initialization', 'setup', 'finished')
        return HttpResponseRedirect('/Initialization/finished')
    else:
        items = common.read_item_section('apps')
        apps = []
        for item in items:
            if item[1] == 'True':
                apps.append(app_info(item[0]))
        context['apps'] = apps
        return render_to_response('Initialization/setup3.html', context, context_instance=RequestContext(request))


def finished(request):
    context = {}
    
    if request.method == 'POST':
        return HttpResponseRedirect('/')
    else:
        pillars_id = common.read_config('pillars', 'pillars_id')
        pillars_pwd = common.read_config('pillars', 'pillars_pwd')
        language = common.read_config('global', 'language')
        timezone = common.read_config('global', 'timezone')
        email_host = common.read_config('email', 'email_host')
        email_port = common.read_config('email', 'email_port')
        email_host_user = common.read_config('email', 'email_host_user')
        email_host_password = common.read_config('email', 'email_host_password')
        email_use_tls = common.read_config('email', 'email_use_tls')
        is_skip = common.read_config('email', 'is_skip')
        apps = common.read_item_section('apps')
        try:
            u = User.objects.create_user(username = pillars_id, email = email_host_user, password = pillars_pwd, is_staff = 1, is_superuser=1)
            u.first_name = pillars_id
            u.save()
        except:
            print '创建用户失败'
        
        pillars = {'pillars_id': pillars_id, 'pillars_pwd': pillars_pwd}
        globals = {'language': language, 'timezone': timezone}
        email = {'email_host': email_host, 'email_port': email_port, 'email_host_user': email_host_user, 'email_host_password': email_host_password, 'email_use_tls': email_use_tls, 'is_skip': is_skip}
        myapps = {}
        for app in apps:
            myapps[app[0]] = app[1]
        
        context['pillars'] = pillars
        context['globals'] = globals
        context['email'] = email
        context['myapps'] = myapps
        
        common.wirte_config('initialization', 'initialization', 'YES')
        
        return render_to_response('Initialization/finished.html', context, context_instance=RequestContext(request))

    