# -*- coding: utf-8 -*-

from PillarsCGSystem.common import CopyFile
from PillarsCGSystem import globalvar
from django.http import HttpResponse
from django.utils import simplejson
from ProjectManSys.models import *
from BaseSys.models import UserProfile
import os
from PillarsCGSystem.common import groupsTree,getPath


#人员信息获取
def people_read(request):
    i = {}
    if request.method == 'POST':
        username = request.POST.get('name','')  
        try:
            user = UserProfile.objects.filter(user__username__exact = username)[0]
        except:
            user = ''
        if user:
            i['name'] = username
            if user.department:
                i['department'] = user.department.name
            if user.position:
                i['position'] = user.position.name
            i['sex'] = user.sex
            i['phone'] = user.phone
            i['home'] = user.home
    return HttpResponse(simplejson.dumps(i))       
        
#获取项目列表
def project_read(request):
    i = {}
    if request.method == 'POST':
        p_id = request.POST.get('p_id','')
        projects = Project.objects.filter(id = p_id)[0]
        for p in projects:
            i['id'] = p.id
            i['name'] = p.namei
    return HttpResponse(simplejson.dumps(i))

#获取资产
def asset_read(request):
    i = {}
    if request.method == 'POST':
        t_id = request.POST.get('t_id','')  
        a_id = request.POST.get('a_id','')        
        if t_id:
            t = Task.objects.filter(id = t_id)[0]
            i['id'] = t.task_group.id
            i['name'] = t.task_group.name
            if t.task_group.types:
                i['type'] = t.task_group.types.name
            if t.task_group.status:
                i['status'] = t.task_group.status.name
            i['group'] = t.task_group.group.name
            i['desc'] = t.task_group.desc
            i['path'] = getPath(t.task_group.id)
        if a_id:
            tg = TaskGroup.objects.filter(id = a_id)[0]
            i['id'] = tg.id
            i['name'] = tg.name
            if tg.types:
                i['type'] = tg.types.name
            if tg.status:
                i['status'] = tg.status.name
            i['group'] = tg.group.name
            i['desc'] = tg.desc
            i['path'] = getPath(tg.id)
    return HttpResponse(simplejson.dumps(i))

#获取某个用户的任务
def task_read(request):
    i = []
    if request.method == 'POST':
        username = request.POST.get('username','')
        p_id = request.POST.get('p_id','')
        t_id = request.POST.get('t_id','')  
        if username:
            try:
                u = User.objects.filter(username = username)
            except:
                u = ''
        if u:           
            if p_id:
                try:
                    ts = Task.objects.filter(project__id__exact = p_id,user = u,is_active=True)
                except:
                    ts = ''
            else:
                try:
                    ts = Task.objects.filter(user = u,is_active=True)
                except:
                    ts  = ''
            for t in ts:
                k = {}
                k['id'] = t.id
                k['name'] = t.name
                if t.status:
                    k['status'] = t.status.name
#                if t.start_time:
#                    k['start_time'] = t.start_time
#                if t.end_time:
#                    k['end_time'] = t.end_time
                if t.version:
                    k['version'] = t.version
                k['desc'] = t.desc
                i.append(k)
        else:
            k = {}
            k['error'] = 'user  not exit'
            i.append(k)
        if t_id:
            u = User.objects.filter(id = t_id)
            ts = Task.objects.filter(user = u,is_active=True)
            for t in ts:
                k = {}
                k['id'] = t.id
                k['name'] = t.name
                if t.status:
                    k['status'] = t.status.name
#                if t.start_time:
#                    k['start_time'] = t.start_time
#                if t.end_time:
#                    k['end_time'] = t.end_time
                if t.version:
                    k['version'] = t.version
                k['desc'] = t.desc
                i.append(k)
    return HttpResponse(simplejson.dumps(i))

def all_read(request,index):
    info = []
    if request.method == 'POST':
        if index:
            type = index[:1]
            index = index[1:]
            try:
                id = int(index)
            except:
                if index[:1] == 'a':
                    id = -int(index[1:])
                else:
                    id = None
            if id :
                if type == 'p':
                    gs = Groups.objects.filter(parent=0,project__id__exact=id)
                    for g in gs:
                        k = {}
                        try:
                            gps = Groups.objects.filter(parent = g.id)                        
                        except:
                            
                            gps = ''
                        if gps:
                            k['id'] = 'g'+str(g.id) 
                        else:
                            k['id'] = 'ga'+str(g.id)
                        k['name'] = g.name
                        info.append(k)
                elif type == 'g':
                    if id < 0:
                        tgs = TaskGroup.objects.filter(group__id__exact = -id,is_active=True)
                        for t in tgs:
                            k = {}
                            k['id'] = 'a'+str(t.id)
                            k['name'] = t.name
                            if t.types:
                                k['type'] = t.types.name
                            else:
                                k['type'] = ''
                            info.append(k)
                    else:
                        gs = Groups.objects.filter(parent = id)
                        for g in gs:
                            k = {}
                            try:
                                gps = Groups.objects.filter(parent = g.id)                        
                            except:
                                gps = ''
                            if gps:
                                k['id'] = 'g'+str(g.id) 
                            else:
                                k['id'] = 'ga'+str(g.id)
                            k['name'] = g.name
                            info.append(k)
                elif type == 'a':
                    ts = Task.objects.filter(task_group__id__exact = id,is_active=True)
                    for t in ts:
                        k = {}
                        k['id'] = 't'+str(t.id)
                        k['name'] = t.name
                        if t.version:                                                      
                            k['version'] = t.version
                        else:
                            k['version'] = '000'
                        if t.user:
                            l = []
                            for u in t.user.all():
                                l.append(u.username)
                                k['user'] = l
                        else:
                            k['user'] = ''
                        info.append(k)
                elif type == 't':
                    pass
        else:
            ps = Project.objects.filter(is_active=True)
            for p in ps:
                k = {}
                k['id'] = 'p' + str(p.id)
                k['name'] = p.name
                info.append(k)
    return HttpResponse(simplejson.dumps(info))

        
# 资产发布
def publish_task(request):
    if request.method == 'POST':
        src = request.POST.get('src','')
        dst = request.POST.get('dst','')
        t_id = request.POST.get('task_id','')
        qc = request.POST.get('qc','')
        is_copy = request.POST.get('is_copy','')
        src = simplejson.loads(src)
        info = {}
        info['dst'] = os.path.join('/Pillars/Pub/',dst)
        info['dst2'] = os.path.join('/PillarsBig/Pub/',dst)       
        info['task'] = [t_id,qc]
        if is_copy:
            info['isCopy'] = False
        l = []
        for s in src:           
            l.append( os.path.join('/Pillars/Job/',s))
        info['src'] = l   
        globalvar.Queue.append(info)       
        if not globalvar.ThreadStatus:
            print 'thread_start'
            globalvar.ThreadStatus = True
            copy_thread = CopyFile()
            copy_thread.start()
        print globalvar.Errors
                    
    i = []
    return HttpResponse(simplejson.dumps(i))

# 文件复制
def copy_file(request):
    if request.method == 'POST':
        src = request.POST.get('src','')
        dst = request.POST.get('dst','')
        src = simplejson.loads(src)
        info = {}
        info['dst'] = os.path.join('/Pillars/Pub/',dst)
        info['dst2'] = os.path.join('/PillarsBig/Pub/',dst)
        info['onlyCopy'] = False   
        l = []
        for s in src:           
            l.append( os.path.join('/Pillars/Job/',s))
        info['src'] = l   
        globalvar.Queue.append(info)       
        if not globalvar.ThreadStatus:
            print 'thread_start'
            globalvar.ThreadStatus = True
            copy_thread = CopyFile()
            copy_thread.start()
        print globalvar.Errors
                    
    i = []
    return HttpResponse(simplejson.dumps(i))
