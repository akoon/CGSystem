# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    context = {}
    return render_to_response('ContactSys/index.html', context, context_instance=RequestContext(request))
