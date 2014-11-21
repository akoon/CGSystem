# -*- coding: utf-8 -*-
'''
Middleware 类包
@summary: 本类包保存系统中使用的Middleware类
'''

from django.http import HttpResponseRedirect
from PillarsCGSystem import common
import PillarsCGSystem.settings
import re

LOGIN_PATH="/login/"

INIT_PATH="/Initialization/"
INIT_PATH_V="/Initialization/validate"
INIT_PATH_0="/Initialization/0"
INIT_PATH_1="/Initialization/1"
INIT_PATH_2="/Initialization/2"
INIT_PATH_3="/Initialization/3"
INIT_PATH_FINISHED="/Initialization/finished"
INIT_PATH_SKIP="/Initialization/skip"

#登陆验证
class LoginAuth(object):

    def process_request(self, request):
        
#         print common.user_flag(request.user)
        
#         print common.read_config("initialization","initialization")
        
        if 'NO' == common.read_config("initialization","initialization"):
            if '0' == common.read_config("initialization","setup"):
                if request.path not in(INIT_PATH_0, INIT_PATH_V, INIT_PATH):
                    return HttpResponseRedirect(INIT_PATH)
            elif '1' == common.read_config("initialization","setup"):
                if request.path not in(INIT_PATH_1, INIT_PATH_0, INIT_PATH_V, INIT_PATH):
                    return HttpResponseRedirect(INIT_PATH_1)
            elif '2' == common.read_config("initialization","setup"):
                if request.path not in (INIT_PATH_2, INIT_PATH_1,INIT_PATH_0, INIT_PATH_V, INIT_PATH, INIT_PATH_SKIP):
                    return HttpResponseRedirect(INIT_PATH_2)
            elif '3' == common.read_config("initialization","setup"):
                if request.path not in (INIT_PATH_3, INIT_PATH_2, INIT_PATH_1,INIT_PATH_0, INIT_PATH_V, INIT_PATH, INIT_PATH_SKIP):
                    return HttpResponseRedirect(INIT_PATH_3)
                
        else:
            if request.path in (INIT_PATH, INIT_PATH_V, INIT_PATH_0, INIT_PATH_1, INIT_PATH_2, INIT_PATH_3):
                return HttpResponseRedirect('/')
            
            if request.path!=LOGIN_PATH:
                if request.user.is_authenticated():
                    pass
                else: 
                    return HttpResponseRedirect('/login/?next=%s' % request.path)


#     def process_view(self, request, callback, callback_args, callback_kwargs):
#         path=request.path
#         if path.startswith('/accounts'):
#             if request.user.is_superuser==1:          
#                 pass
#             else:
#                 return HttpResponseRedirect('/')  

                          
#访问IP限制
class Acl():
    def process_request(self, request):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
            ip =  request.META['HTTP_X_FORWARDED_FOR']  
        else:  
            ip = request.META['REMOTE_ADDR']
        
#         print 'Access ip is :    ', ip
        
        if request.path!=LOGIN_PATH:
            if len(PillarsCGSystem.settings.ACCEPT_IP) == 0:
                pass
            else:
                for i in PillarsCGSystem.settings.ACCEPT_IP:
                    if re.search(i, ip):
                        break
                    else:
                        return HttpResponseRedirect('/login/?next=%s' % request.path)
        else:
            pass
            
            
            
            
    