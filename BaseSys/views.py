# -*- coding: utf-8 -*-
'''
Views 基础模块视图方法包
@summary: 系统基本模块的view方法
'''

from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import simplejson
from PillarsCGSystem import common
from models import *

def login(request):
    context = {}
    if request.method == 'POST': 
        
        # 提交表单
        username = request.POST['login_input_username']
        password = request.POST['login_input_password']
        
        # 用户验证
        user = auth.authenticate(username=username, password=password)
        if user is not None and common.user_flag(user) <= 4 :
            # 通过验证并登陆返回登陆后主页
            auth.login(request, user)
            request.session.set_expiry(0) 
#            if request.POST.get('login_input_isMem', '') != 'on':
#                request.session.set_expiry(0)

            #记录用户的登录IP
            try:
                profile = UserProfile.objects.get(user = user)
                loginip = None
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    loginip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    loginip =  request.META['REMOTE_ADDR']
                profile.lastloginip = loginip
                profile.save()
            except:
                pass

            if user.is_superuser:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            # 验证信息错误
            context['errors'] = '用户名或密码错误，或该用户已禁用'
            return render_to_response('BaseSys/login_2.html', context, context_instance=RequestContext(request))     
    else:    
        return render_to_response('BaseSys/login_2.html', context, context_instance=RequestContext(request))

def logout(request):
    # 用户注销后返回主页
    auth.logout(request)
    return HttpResponseRedirect('/')

def app(request):
    context = {}
    return render_to_response('BaseSys/app.html', context, context_instance=RequestContext(request))

def index(request):
    context = {}
    if common.user_flag(request.user) >= 2:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('BaseSys/index.html', context, context_instance=RequestContext(request))
#    return HttpResponseRedirect('/BaseSys')

def department(request):
    context = {}    
    if common.user_flag(request.user) >= 2:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('BaseSys/department.html', context, context_instance=RequestContext(request))

def position(request):
    # 职位管理页面
    context = {}    
    if common.user_flag(request.user) >= 2:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('BaseSys/position.html', context, context_instance=RequestContext(request))

def people(request):
    # 人员管理页面
    context = {}    
    if common.user_flag(request.user) >= 2:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('BaseSys/people.html', context, context_instance=RequestContext(request))

def permissions(request):
    # 权限管理页面
    context = {}    
    if common.user_flag(request.user) >= 2:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('BaseSys/permissions.html', context, context_instance=RequestContext(request))
    
def change_passwd(request):
    info = {}
    if request.method == 'POST':
        oldpasswd = request.POST['oldpasswd']
        newpasswd = request.POST['newpasswd']
        if request.user.check_password(oldpasswd):
            request.user.set_password(newpasswd)
            request.user.save()
            info['success'] = True
        else:
            info['success'] = False
    return HttpResponse(simplejson.dumps(info))
        
