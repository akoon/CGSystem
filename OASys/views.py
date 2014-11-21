# -*- coding: utf-8 -*-
'''
Views OA模块视图方法包
@summary: OA模块的view方法
'''

from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import *
import time, datetime
from PillarsCGSystem import common
from TimeSheetSys.models import Confirm

def leave(request):
    context = {}
    return render_to_response('OASys/leave.html', context, context_instance=RequestContext(request))
    
def leave_archive(request):
    context = {}
    return render_to_response('OASys/leaveArchive.html', context, context_instance=RequestContext(request))