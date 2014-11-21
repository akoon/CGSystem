# -*- coding: utf-8 -*-
'''
Views 基础模块视图方法包
@summary: 系统基本模块的view方法
'''
from django.contrib import auth
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils import timezone
from PillarsCGSystem import common
from datetime import datetime
from datetime import timedelta
from models import *
from django.contrib.sessions.models import Session

def main(request):
    context = {}
    
    try:
        if request.method == 'GET':
            proj = request.GET.get('proj','')
            context['proj'] = proj
            print 'proj     :', proj
    finally:
        return render_to_response('ProjectManSys/index.html', context, context_instance=RequestContext(request))

#项目管理子系统主页
def index(request):
    context = {}
    
    s = Session.objects.get(pk=request.session.session_key)
    
    context['sessionId'] = request.session.session_key
    context['sessionData'] = s.session_data
    
    return render_to_response('ProjectManSys/index.html', context, context_instance=RequestContext(request))

#项目管理子系统主页
def index_projectlist(request):
    context = {}
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    else:
        context['has_op'] = False
        
    return render_to_response('ProjectManSys/indexProjectlist.html', context, context_instance=RequestContext(request))

#状态管理
def status(request):
    context = {}
    if not request.user.is_staff:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('ProjectManSys/status.html', context, context_instance=RequestContext(request))

#类型管理
def types(request):
    context = {}
    if not request.user.is_staff:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('ProjectManSys/types.html', context, context_instance=RequestContext(request))

#组管理
def group(request):
    context = {}
    if not request.user.is_staff:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('ProjectManSys/group.html', context, context_instance=RequestContext(request))

#模板管理
def templ(request):
    context = {}
    if not request.user.is_staff:
        before = request.META['HTTP_REFERER']
        return HttpResponseRedirect(before)
    return render_to_response('ProjectManSys/templ.html', context, context_instance=RequestContext(request))


#项目主页
def project_index(request,index):
    context = {}
    try:
        index = int(index)
    except:
        index = None
    if index:
        p = Project.objects.filter(id = index)[0]
        request.session['projectId'] = p.id
        request.session['projectName'] = p.name        
        context['name'] = p.name 
        if p.status:
            context['status'] = p.status.name
        if p.user:
            context['username'] = p.user.first_name
        context['desc'] = p.desc
        context['start_time'] = timezone.localtime(p.start_time).strftime('%Y-%m-%d')
        context['end_time'] = timezone.localtime(p.end_time).strftime('%Y-%m-%d')
        if p.thum:
            context['thum'] = p.thum.url
            
        
        project_asset = TaskGroup.objects.filter(project=p)
        project_task = Task.objects.filter(project=p)
        
        asset_status_list = Status.objects.filter(type = -2)
        task_status_list = Status.objects.filter(type = -3)
        asset_types_list = Types.objects.filter(type = -2)
        task_types_list = Types.objects.filter(type = -3)


        asset_status = []
        for asset_status_obj in asset_status_list:
            asset_status_dict = {}
            asset_status_dict['name'] = asset_status_obj.name
            asset_status_dict['count'] = project_asset.filter(status = asset_status_obj.id).count()
            asset_status.append(asset_status_dict)
        context['asset_status'] = asset_status
        
        asset_types = []
        for asset_types_obj in asset_types_list:
            asset_types_dict = {}
            asset_types_dict['name'] = asset_types_obj.name
            asset_types_dict['count'] = project_asset.filter(types = asset_types_obj.id).count()
            asset_types.append(asset_types_dict)
        context['asset_types'] = asset_types
        
        task_status = []
        for task_status_obj in task_status_list:
            task_status_dict = {}
            task_status_dict['name'] = task_status_obj.name
            task_status_dict['count'] = project_task.filter(status = task_status_obj.id).count()
            task_status.append(task_status_dict)
        context['task_status'] = task_status
        
        task_types = []
        for task_types_obj in task_types_list:
            task_types_dict = {}
            task_types_dict['name'] = task_types_obj.name
            task_types_dict['count'] = project_task.filter(types = task_types_obj.id).count()
            task_types.append(task_types_dict)
        context['task_types'] = task_types
        
        #TODO: 注意此处状态字段 
        top_task_list = project_task.exclude(status = 15).order_by('end_time').all()
        top_task = []
        for top_task_obj in top_task_list:
            if not top_task_obj.end_time or not top_task_obj.start_time:
                continue
            top_task_dict = {}
            top_task_dict['name'] = top_task_obj.task_group.name + '-' + top_task_obj.name
            top_task_dict['time'] = timezone.localtime(top_task_obj.end_time).strftime('%Y-%m-%d')
            top_task_dict['days'] = (timezone.localtime(top_task_obj.end_time) - timezone.localtime(top_task_obj.start_time)).days +1
            top_task.append(top_task_dict)
            if len(top_task) == 10:
                break
        print 'top_task     :', top_task
        context['top_task'] = top_task
        
#        #查询工作量
        workload_list = []
        
        try:
            projectPeople = ProjectPeople.objects.filter(project = p)[0]
            
            for user in projectPeople.users.all():
                tasks = Task.objects.filter(user=user, project=p)
                
                sum = 0
                dict = {}
                dict['name'] = user.first_name
                for task in tasks:
                    if task.use_time == '' or task.use_time == None:
                        pass
                    else:
#                        print task.use_time
                        sum += float(task.use_time)
                dict['count'] = sum
                
                if sum != 0:
                    workload_list.append(dict)
            
        except:
            pass
        
        workload_list = common.dict_sort(workload_list, 'count', True)
        
        context['workloads'] = workload_list
            
        
#         #查询用户任务数
#         context['taskCount'] = user_task.count()
#         #正在进行
#         context['wipCount'] = user_task.filter(status=12).count()
#         #已发布
#         context['publishCount'] = user_task.filter(publish_status=1).count()
#         #已提交
#         context['submitReCount'] = user_task.filter(review_status=1).count()
#         #审核通过
#         context['passedCount'] = user_task.filter(review_status=3).count()
#         #QC通过
#         context['qcCount'] = user_task.filter(qc_flag=1).count()
        
        
    return render_to_response('ProjectManSys/projectIndex2.html', context, context_instance=RequestContext(request))

#项目资产组
def project_group(request,index):
    context = {}
    p = Project.objects.filter(id = index)[0]
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    elif common.user_flag(request.user) == 2 and p.user_id == request.user.id:
        context['has_op'] = True
    else:
        context['has_op'] = False
    return render_to_response('ProjectManSys/projectGroup.html', context, context_instance=RequestContext(request))

#项目人员
def project_people(request,index):
    context = {}
    p = Project.objects.filter(id = index)[0]
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    elif common.user_flag(request.user) == 2 and p.user_id == request.user.id:
        context['has_op'] = True
    else:
        context['has_op'] = False
    return render_to_response('ProjectManSys/projectPeople.html', context, context_instance=RequestContext(request))

#项目绩效
def project_performance(request,index):
    context = {}
    p = Project.objects.filter(id = index)[0]
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    elif common.user_flag(request.user) == 2 and p.user_id == request.user.id:
        context['has_op'] = True
    else:
        context['has_op'] = False
    return render_to_response('ProjectManSys/projectPerformance.html', context, context_instance=RequestContext(request))


#项目任务
def project_task(request,index):
    context = {}
    p = Project.objects.filter(id = index)[0]
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    elif common.user_flag(request.user) == 2 and p.user_id == request.user.id:
        context['has_op'] = True
    else:
        context['has_op'] = False
    return render_to_response('ProjectManSys/projectTaskDl.html', context, context_instance=RequestContext(request))

#项目甘特图
def project_gantt(request,index):
    context = {}
    ts = Task.objects.filter(user__username__exact = 'shaolei.zhao')
    for t in ts:
        try:
            print t.task_group.id
        except:
            print 'task',t.id
    context['proj'] = index
    return render_to_response('ProjectManSys/projectGantt.html', context, context_instance=RequestContext(request))

#甘特图
def gantt(request, proj):
    context = {}
    
    context['proj'] = proj
    #获取所有项目的开始/结束时间
#        print 'proj     :', proj
    
    #获取所有项目的开始/结束时间
    pList = []
    if proj == 0 or proj == '' or proj == None:
        pList = Project.objects.filter(is_active=True)
    else:
        pList.append(Project.objects.get(id=proj))
    
    if pList != None and len(pList) != 0:
        for project in pList:
            p = {}
            
            pStartDate = None
            pEndDate = None
            
            #获取资产信息
            asset_list=[]
            for task_group in TaskGroup.objects.filter(project=project,is_active=True):
                tg = {}
                
                aStartDate = None
                aEndDate = None
                
                #获取任务信息
                task_list=[]
                for task in Task.objects.filter(task_group=task_group,is_active=True):
                    t = {}
                    
                    if(task.start_time == None):
                        startdate = ''
                    else:
                        startdate = timezone.localtime(task.start_time)
                        #资产最早开始时间计算
                        if aStartDate == None:
                            aStartDate = task.start_time
                        else:
                            if task.start_time < aStartDate:
                                aStartDate = task.start_time
                    
                    if(task.end_time == None):
                        endate = ''
                    else:
                        endate = timezone.localtime(task.end_time)
                    
                        #资产最晚结束时间计算
                        if aEndDate == None:
                            aEndDate = task.end_time
                        else:
                            if task.end_time > aEndDate:
                                aEndDate = task.end_time
                
                #资产最早开始时间赋值
                if(aStartDate == None):
                    startdate = ''
                else:
                    startdate = timezone.localtime(aStartDate)
                
                #资产最晚结束时间赋值
                if(aEndDate == None):
                    endate = ''
                else:
                    endate = timezone.localtime(aEndDate)
                
                #项目最早开始时间计算
                if aStartDate != None:
                    if pStartDate == None:
                        pStartDate = aStartDate
                    else:
                        if aStartDate < pStartDate:
                            pStartDate = aStartDate
                else:
                    pStartDate = project.start_time
                    
                #项目最晚结束时间计算
                if aEndDate != None:
                    if pEndDate == None:
                        pEndDate = aEndDate
                    else:
                        if aEndDate > pEndDate:
                            pEndDate = aEndDate
                else:
                    pEndDate = project.end_time
                    
            #项目最早开始时间赋值
            if(pStartDate == None):
                startdate = ''
            else:
                startdate = timezone.localtime(pStartDate)
            
            #项目最晚结束时间赋值
            if(pEndDate == None):
                endate = ''
            else:
                endate = timezone.localtime(pEndDate)
    
    context['startdate'] = startdate.strftime('%Y-%m-%d')
    context['endate'] = endate.strftime('%Y-%m-%d')
    
    return render_to_response('ProjectManSys/gantt.html', context, context_instance=RequestContext(request))

#项目审核意见
def project_notes(request,index):
    context = {}
    return render_to_response('ProjectManSys/projectNotes.html', context, context_instance=RequestContext(request))

#资产关联
def project_rel(request,index):
    context = {}
    p = Project.objects.filter(id = index)[0]
    if common.user_flag(request.user) < 2:
        context['has_op'] = True
    elif p.user_id == request.user.id:
        context['has_op'] = True
    else:
        context['has_op'] = False
    return render_to_response('ProjectManSys/projectRel.html', context, context_instance=RequestContext(request))
