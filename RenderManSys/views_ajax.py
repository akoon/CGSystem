# -*- coding: utf-8 -*-
'''
Created on 2013-5-24

@author: hao.yu
'''
from django.http import HttpResponse
from django.utils import simplejson
import time
from PillarsCGSystem.globalvar import ats, MOUNTDIR

def connect_render_server(request):
    status = 0
    if 'GET' == request.method:
        svrip = request.GET.get('svrip', '')
        svrport = request.GET.get('svrport', '')
        request.session['svrip'] = svrip
        request.session['svrport'] = svrport
        status = ats.connect_render_server((svrip, int(svrport)))
    return HttpResponse(simplejson.dumps({'status' : status}))    

def get_connect_status(request):
    svrip = request.session['svrip']
    svrport = request.session['svrport']
    connect_status = ats.get_connect_status((svrip, int(svrport)))
    return HttpResponse(simplejson.dumps({'connectstatus' : connect_status}))

def get_render_nodes(request):
    svrip = request.session['svrip']
    svrport = request.session['svrport']
    rennodes = ats.request_rennodes((svrip, int(svrport)))
    return HttpResponse(simplejson.dumps(rennodes))

def get_render_tasks(request):
    svrip = request.session['svrip']
    svrport = request.session['svrport']
    rentasks = ats.request_rentasks((svrip, int(svrport)))
    return HttpResponse(simplejson.dumps(rentasks))
    
def put_process_cmd(request):
    svrip = request.session['svrip']
    svrport = request.session['svrport']
    if 'GET' == request.method:
        cmds = request.GET.get('cmds', '')
        cmds = simplejson.loads(cmds)
        cmd_count = ats.insert_process_cmd(cmds, request.user.username, (svrip, int(svrport)))
    return HttpResponse(simplejson.dumps({'cmdcount' : cmd_count}))
    
def put_render_task(request):
    status = -1
    if 'POST' == request.method:
        cmds = request.POST.get('cmds', '');
        cmds = simplejson.loads(cmds)
        connectstatus = ats.connect_render_server()
        if 1 == connectstatus:
            time.sleep(1)
            loginstatus = ats.get_connect_status()
            if 2 == loginstatus:
                status = ats.insert_process_cmd(cmds, request.user.username)
    return HttpResponse(simplejson.dumps({'msgcode' : status}))      
        
def get_file_tree(request):
    import os
    r = ['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r = ['<ul class="jqueryFileTree" style="display: none;">']
        d = request.POST.get('dir', MOUNTDIR)
        paths = os.listdir(d)
        paths.sort(lambda x,y: cmp(x.lower(),y.lower()))
        for f in paths:
            ff = os.path.join(d, f)
            if os.path.isdir(ff):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff, f))
            else:
                e = os.path.splitext(f)[1][1:]  # get .ext and remove dot
                r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e, ff, f))
        r.append('</ul>')
    except Exception, e:
        r.append('Could not load directory: %s' % str(e))
    r.append('</ul>')
    return HttpResponse(''.join(r))
        
