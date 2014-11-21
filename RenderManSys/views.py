# -*- coding: utf-8 -*-
'''
Created on 2013-5-24

@author: hao.yu
'''
from django.template import RequestContext
from django.shortcuts import render_to_response

def render_admintool_index(request):
    context = {}
    return render_to_response('RenderManSys/index_tmp.html', context, context_instance=RequestContext(request))

def render_operate_tool(request):
    context = {}
    return render_to_response('RenderManSys/operatetool.html', context, context_instance=RequestContext(request))
    
    
