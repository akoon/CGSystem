# -*- coding: utf-8 -*-
'''
Views 素材管理子系统
'''

from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


def index(request):
    context = {}
    return render_to_response('MaterialManSys/index.html', context, context_instance=RequestContext(request))