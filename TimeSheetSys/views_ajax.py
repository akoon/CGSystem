# -*- coding: utf-8 -*-
from __future__ import division 
from django.http import HttpResponse
from django.utils import simplejson
from models import *
from ProjectManSys.models import *
import datetime, time
from django.utils import timezone
import string
from PillarsCGSystem.globalvar import *


#获取Timesheet用户列表
def tsusers_detail(request):
    
    info = {}
    if request.method == 'GET':
        
        user_list = []
        user_list_next = []
        #查询所属的组员信息
        user_list.append(Confirm.objects.get(user = request.user))
        user_list_next.append(Confirm.objects.get(user = request.user))
        
        for ulx in user_list_next:
            #查询所属的组员信息
            groupMember = Confirm.objects.filter(superior = ulx.user)
            print 'groupMember  ', groupMember
            for gp in groupMember:
                if gp.rank == 0:
                    #组员没有下级
                    user_list.append(gp)
                else:
                    user_list.append(gp)
                    user_list_next.append(gp)
        
        i = 0
        l = []
        for u in user_list:
            i += 1
            d = {}
            d['id'] = u.user.id
            if u.user.first_name == '' or u.user.first_name == None:
                d['first_name'] = u.user.username
            else:
                d['first_name'] = u.user.first_name
            d['email'] = u.user.email
            #查询用户当天的任务
            try:
                daily = Actual_Daily.objects.get(user=u.user, date=time.strftime('%Y-%m-%d',time.localtime(time.time())) )
                d['status'] = daily.status.name
            except:
                d['status'] = ''
            d['ops'] = "<a href='/TimeSheetSys/timesheet_viewmode/?date=today&uid=" + str(u.user.id) + "'>Check user</a>&nbsp;&nbsp;<a onclick='reportWinOpen()' href='#'>Report</a>&nbsp;&nbsp;<a onclick='statisticWinOpen()' href='#'>Statistics</a>"
            l.append(d)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))

#####################################Task_Daily###################################

def get_user_tasks(request, uid):
    print 'get_user_tasks'
    if request.method == 'GET':     
        print 'uid    ', uid
        
        #user_id= request.user.id
        user_id = uid
        
        task_list=[]
        dic={}
        
        #当前只显示FengTian项目
#        for task in Task_Asset.objects.filter(assign_id=user_id, project = Project.objects.get(id=69)):
#            t={}
#            t['id']=task.id
#            t['name']=task.type
#            task_list.append(t)
        
        for mission in Mission.objects.all():
            m={}
            m['id']=mission.id
            m['name']=mission.name
            if mission.del_flag == False:
                task_list.append(m)
            
        dic['tasks']=  task_list
        dic['success'] ='true'
        
        return HttpResponse(simplejson.dumps(dic))

def get_user_tasks_combo(request, uid):
    print 'get_user_tasks_combo' 
    if request.method == 'GET':
        print 'uid    ', uid
        #user_id = request.user.id
        user_id = uid
        
        task_list=[]
        dic={}

        for task in Task.objects.filter(user=User.objects.get(id=uid), is_active=True):
            t={}
            t['id']=str(task.id) + '_t'
            t['name']='['+task.project.name+'] - ['+task.task_group.name+'] - '+task.name
            
#---------------------------------只显示当周的任务------------------------------------
#            if task.start_time != None and task.end_time != None:
#
#                weekday = datetime.date.today().weekday()
#                week_start = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()).replace(hour=0, minute=0, second=0, microsecond=0)
#                week_end = week_start
#                week_start = week_start.replace(day= week_start.day - weekday)
#                week_end = week_end.replace(day= week_end.day + (6 - weekday))
#                task_start = timezone.localtime(task.start_time).replace(hour=0, minute=0, second=0, microsecond=0)
#                task_end = timezone.localtime(task.end_time).replace(hour=0, minute=0, second=0, microsecond=0)
##                print 'week_start    ',week_start
##                print 'week_end     ',week_end
##                print 'task_start    ',task_start
##                print 'task_end     ',task_end
##                print '-------------',
#                if task_end < week_start or task_start > week_end:
#                    pass
#                else:
#                    task_list.append(t)
#---------------------------------只显示当周的任务------------------------------------
        
#---------------------------------显示全部任务------------------------------------
            task_list.append(t)
            
            
        #当前只显示FengTian项目
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=69)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=70)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=71)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=72)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=73)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
#        for task in Task.objects.filter(assign_id=user_id, project = Project.objects.filter(id=74)):
#            t={}
#            t['id']=str(task.id) + '_t'
#            t['name']='['+task.project.name+'] - ['+task.asset.name+'] - '+task.type
#            task_list.append(t)
            
        for mission in Mission.objects.all():
            m={}
            m['id']=str(mission.id) + '_m'
            m['name']=mission.name
            if mission.del_flag == False:
                task_list.append(m)
            
        dic['tasks']=  task_list
        dic['success'] ='true'  
        return HttpResponse(simplejson.dumps(task_list))

#def get_user_missions_combo(request):
#    if request.method == 'GET':     
#        user_id= request.user.id
#        task_list=[]
#        if Task_Asset.objects.filter(assign_id=user_id).exists():
#            dic={}
#            for mission in Mission.objects.all():
#                m={}
#                m['id']=mission.id
#                m['name']=mission.name
#                task_list.append(m)
#            dic['tasks']=  task_list
#            dic['success'] ='true'              
#            return HttpResponse(simplejson.dumps(task_list))
#        else:
#            return HttpResponse(simplejson.dumps('this user has no tasks'))

def update_actual_task(request, uid):
    print 'update_actual_task'
    print 'uid    ', uid
    if request.method == 'POST':
        print 'update_actual_task'
        print request.POST
        
        dic = request.POST.dict()
        print dic
        event = dic.keys()[0]
        event = event.encode('utf-8')
        false = False
        true = True
        null = None
        
        event = eval(event)
        
        id = event['eid']
        
        print 'Event id         ', id
        
        if id != None:
            #id成为 Extensible.calendar.data.EventModel-323 格式的bug
            pos = string.find(str(id), '-')
            if pos != -1:
                id = id[pos + 1:]
                print 'converted   id ', id
            
            sid = event['cid']
            title = event['title']
            start = event['start'].replace('T', ' ')
            end = event['end'].replace('T', ' ')
            notes = event['notes']
            task, type = event['task'].split('_')
            editable = event['editable']
            overtime = event['overtime']
            #user_id= request.user.id
            user_id = uid    
    #        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            
            dic={}
            
            print start[:10]
            print end[:10]
            
            #所属daily日期
            daily_date = start[:10]
            print 'daily_date    ', daily_date
            #判定是否有权限
    #        status = Actual_Daily.objects.get(user_id = user_id, date = daily_date).status.id
    #        if status == 3 or status == 4:
    #            dic['success'] ='false'
    #            dic['msg'] ='当前用户没有权限修改'
                
            #不能更改到当日以外的日期
    #        elif current_date != start[:10] or current_date != end[:10]:
    #            dic['success'] ='false'
    #            dic['msg'] ='不能更改到当日以外的日期'
                
            # 1. task 2. mission
            if(type == 't'):
                type_id = 1
            if(type == 'm'):
                type_id = 2     
                
            print 'daily              :', int(event['daily'])
            #如果daily不存在,则新建根据task start date
            if Actual_Daily.objects.filter(user_id=user_id, date = daily_date).exists() == False:
                daily = Actual_Daily.objects.create(date = daily_date,user_id = user_id,status = Actual_Status.objects.get(id=1))
            else:
                #daily = Actual_Daily.objects.get(id = int(event['daily']))
                #目的日期确定daily
                daily = Actual_Daily.objects.get(date = daily_date, user = User.objects.get(id=uid))
            
            #判定要移动的目的daily是否允许修改
            if daily.status.id == 1 or daily.status.id == 8:
                editable = True
            else:
                editable = False
                
    #        if Actual_Daily.objects.filter(user_id=user_id, date = current_date).exists() == False:
    #            Actual_Daily.objects.create(date = current_date,user_id = user_id,status = Actual_Daily.objects.get(id=1))
        
        
            if editable == True:
                if type_id == 1:
        #            t = Actual_Task(id=id, daily=Actual_Daily.objects.get(user_id=user_id, date=current_date), type=type_id, task=Task_Asset.objects.get(id=task), cid=Actual_Status.objects.get(id=sid), title=title, start_time=start, end_time=end, desc=notes)
                    t = Actual_Task(id=id, daily=daily, type=type_id, task=Task.objects.get(id=task), title=title.decode('unicode_escape'), start_time=start, end_time=end, desc=notes.decode('unicode_escape'), overtime=overtime)
                
                else:
        #            t = Actual_Task(id=id, daily=Actual_Daily.objects.get(user_id=user_id, date=current_date), type=type_id, mission=Mission.objects.get(id=task), cid=Actual_Status.objects.get(id=sid), title=title, start_time=start, end_time=end, desc=notes)
                    t = Actual_Task(id=id, daily=daily, type=type_id, mission=Mission.objects.get(id=task), title=title.decode('unicode_escape'), start_time=start, end_time=end, desc=notes.decode('unicode_escape'), overtime=overtime)
                
                t.save()
                
                dic['success'] ='true'
            else:
                dic['success'] ='false'
                dic['msg'] ='当前用户没有权限修改'
        else:
            dic['success'] ='false'
            dic['msg'] ='修改失败,刷新页面重试'
                
        return HttpResponse(simplejson.dumps(dic))         

def remove_actual_task(request, uid):
    print 'remove_actual_task'
    print 'uid    ', uid
    if request.method == 'POST':
        print 'remove_actual_task'
        print request.POST
        
        dic = request.POST.dict()
        print dic
            
        task = dic.keys()[0]
        task = task.encode('utf-8')
        false = False
        true = True
        task = eval(task)
        
        id=task['eid']
        #id成为 Extensible.calendar.data.EventModel-323 格式的bug
        pos = string.find(str(id), '-')
        if pos != -1:
            id = id[pos + 1:]
            print 'converted   id ', id
        
        t = Actual_Task.objects.get(id = id)
        daily = t.daily
        t.delete()
        
        #如果daily下属没有task, 则删除daily
#        print 'daily   :', daily
#        print 'count   :', Actual_Task.objects.filter(daily=daily).count()
        if Actual_Task.objects.filter(daily=daily).count() == 0:
            daily.delete()
            print 'daily has benn deleteded'
        
        dic['success'] ='true'
        return HttpResponse(simplejson.dumps(dic))    
        
def add_actual_task(request, uid):
    print 'add_actual_task'
    print 'uid    ', uid
    if request.method == 'POST':
        print 'add_actual_task'
        print request.POST
        
        dic = request.POST.dict()
        print dic
        event = dic.keys()[0]
        event = event 
        
        false = False
        true = True
        event = eval(event)
        
        id = event['eid']
        title = event['title']
        start = event['start'].replace('T', ' ')
        end = event['end'].replace('T', ' ')
        notes = event['notes']
        task, type = event['task'].split('_')
        print 'start    ', start
        print 'end      ', end
        print 'overtime', event['overtime']
        
        #所属daily日期
        daily_date = start[:10]
        
        #写入权限
        ifEditable = False
        
        daily = None
        
        overtime = event['overtime']
        
        #user_id= request.user.id
        user_id = uid
        #current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        rank = Confirm.objects.get(user=request.user)
        
        # 1. task 2. mission
        if(type == 't'):
            type_id = 1
        if(type == 'm'):
            type_id = 2
        
        #title为空情况在客户端判断 5821
#        if (title == None) or (title == ''):
#            if(type == 't'):
#                title = Task_Asset.objects.get(id=task).name
#            if(type == 'm'):
#                title = Mission.objects.get(id=task).name 
        
        if Actual_Daily.objects.filter(user_id=user_id, date = daily_date).exists() == False:
            #如果daily不存在,则新建根据task start date
            daily = Actual_Daily.objects.create(date = daily_date,user_id = user_id,status = Actual_Status.objects.get(id=1))
            ifEditable = True
        else:
            #如果存在daily, 判定是否有权限
            daily=Actual_Daily.objects.get(user_id=user_id, date=daily_date)
            
            #获取task_daily状态并判断下属的task是否可编辑
            status = daily.status.id
            
            #
            print 'status  ', status
            if status == 1 or status == 8:
                ifEditable = True
        
        if ifEditable == True:
            if type_id == 1:
                task_new = Actual_Task.objects.create( daily=daily, type=type_id, task=Task.objects.get(id=task), title=title.decode('unicode_escape'), start_time=start, end_time=end, desc=notes.decode('unicode_escape'), overtime=overtime)
            else:
                task_new = Actual_Task.objects.create( daily=daily, type=type_id, mission=Mission.objects.get(id=task), title=title.decode('unicode_escape'), start_time=start, end_time=end, desc=notes.decode('unicode_escape'), overtime=overtime)
            
            task_new.save()
            dic['success'] ='true'
            
            #结果赋值
            dic['tasks'] = {"eid":task_new.id, "cid":event['cid'], "title":title.decode('unicode_escape'), "start":event['start'], "end":event['end'], "rrule":event['rrule'], "notes":notes.decode('unicode_escape'), "ad":false, "rem":event['rem'], "task":event['task'], "daily":daily.id, "editable":'true', 'overtime': overtime}

        else:
            dic['success'] ='false'
            dic['msg'] ='添加失败'
                      

#        if Actual_Daily.objects.filter(user_id=user_id).exists():
#            Actual_Task.objects.create(daily_id=Actual_Daily.objects.get(user_id=user_id).id,type=type,task_id=task,mission_id=mission,start_time=start_time,end_time=end_time,desc=desc)
#            Actual_Daily.objects.get(user_id=user_id).update(status=1)
#        else:
#            date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#            Actual_Daily.objects.create(date=date,user_id=user_id,status=1)
#            Actual_Task.objects.create(daily_id=Actual_Daily.objects.get(user_id=user_id).id,type=type,task_id=task,mission_id=mission,start_time=start_time,end_time=end_time,desc=desc)


#        task_list=[]
#        task_line = {'id': task_new.id, 'cid': 1, 'daily': task_new.daily.id, 'title': task_new.title, 'task': event['task'], 'start': event['start'], 'end': event['end'],'notes': event['notes']}
#        task_list.append(task_line)
#        dic['tasks']=  task_list
#        dic['id'] = task_new.id
#        dic_return = {task_line: ''}
#        dic_return['success'] = 'true'
#        
#        print 'event    ', dic.keys()
#
#        print 'event    after ', dic.keys()
#        dic = {u'{"id":888,"cid":1,"title":"\\u75c5\\u5047","start":"2013-02-21T13:30:00","end":"2013-02-21T14:30:00","rrule":"","notes":"","ad":false,"rem":"","task":"2_m","daily":0,"editable":false}': u''}
#        return_dic = {"id":444,"cid":1,"title":"\u75c5\u5047","start":"2013-02-21T15:00:00","end":"2013-02-21T16:00:00","rrule":"","notes":"","ad":false,"rem":"","task":"2_m","daily":0,"editable":false}
        
#        dic.clear()
        return HttpResponse(simplejson.dumps(dic))

def get_actual_tasks(request, uid):
    print 'get_actual_tasks'
    print 'uid    ', uid
    if request.method == 'GET':
        print 'get_actual_task'
        #user_id= request.user.id

        dic={}
        task_list=[]
        
        #查询task_daily
        task_daily = Actual_Daily.objects.filter(user_id = uid)
        
        for td in task_daily:
            task = Actual_Task.objects.filter(daily = td)
            
            #获取task_daily状态并判断下属的task是否可编辑
            status = td.status.id
            
            #提交之后不可修改
            editable = False
            print status
            if status == 1 or status == 8:
                editable = True
            
            try:
                #查询task——daily所属的task list
                for t in task:
#                    print type(t.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                    
                    #Task 和 Mission区分    
                    if t.type == 1:
                        # 1. task
                        task_line = {'eid': t.id, 'cid': status, 'daily':  td.id, 'title': t.title, 'task': str(t.task.id) + '_t', 'start': timezone.localtime(t.start_time).strftime('%Y-%m-%d %H:%M:%S'), 'end': timezone.localtime(t.end_time).strftime('%Y-%m-%d %H:%M:%S'),'notes': t.desc, 'editable': editable, 'overtime': t.overtime}
                    else:
                        # 2. mission
                        task_line = {'eid': t.id, 'cid': status, 'daily':  td.id,  'title': t.title, 'task': str(t.mission.id) + '_m', 'start': timezone.localtime(t.start_time).strftime('%Y-%m-%d %H:%M:%S'), 'end': timezone.localtime(t.end_time).strftime('%Y-%m-%d %H:%M:%S'),'notes': t.desc, 'editable': editable, 'overtime': t.overtime}
                    task_list.append(task_line)
            except:
                pass
        dic['success'] ='true'
        dic['tasks']=  task_list
        return HttpResponse(simplejson.dumps(dic))

#返回当前用户当天的任务是否提交
def get_actual_daily_status(request):
    if request.method == 'GET':
        print 'get_actual_daily_status'
        
        user_id= request.user.id    
        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        dic={}
        #如果已提交，则禁用提交按钮
        
        try:
            daily = Actual_Daily.objects.get(user_id=user_id, date=current_date)
            if daily.status.id == 2 or daily.status.id == 3 or daily.status.id == 4:
                dic['result'] = True
            else:
                dic['result'] = False
        except:
            dic['result'] = False
            
        return HttpResponse(simplejson.dumps(dic))

#返回当前用户当天的任务是否通过审核
def get_actual_daily_passed(request):
    if request.method == 'GET':
        print 'get_actual_daily_passed'
        
        user_id= request.user.id    
        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        dic={}
        #如果已通过审核则不允许修改
        
        try:
            daily = Actual_Daily.objects.get(user_id=user_id, date=current_date)
            if daily.status.id == 3 or daily.status.id == 4:
                dic['result'] = True
            else:
                dic['result'] = False
        except:
            dic['result'] = False
            
        return HttpResponse(simplejson.dumps(dic))

#返回task的状态列表
def get_actual_status(request):
    if request.method == 'GET':
        print 'get_actual_status'
        dic={}
        status_list=[]
        
        for status in Actual_Status.objects.all(): 
            s={}
            s['id']=status.id
            s['title']=status.name
            s['color']=status.color
            
            status_list.append(s)
                
        dic['status']=  status_list
        dic['success'] ='true'              
        return HttpResponse(simplejson.dumps(dic))

#返回当月用户所有的actual_daily的情况
#key:    日期
#value:
def get_actual_daily_month(request, uid):
    if request.method == 'GET':
        print 'get_actual_daily_monthly'
        dic={}
        daily=[]
        
        year, month = time.strftime('%Y-%m',time.localtime(time.time())).split('-')
        print 'year ', year, 'month ', month
        daily_list = Actual_Daily.objects.filter(user_id = uid, date__year = year, date__month = month)
        
        for d in daily_list:
            daily_line={}
            daily_line['date'] = timezone.localtime(d.date).strftime('%Y-%m-%d')
            daily_line['status'] = d.status.id
            daily_line['color'] = d.status.color
            daily.append(daily_line)
        dic['daily'] = daily
        dic['success'] = 'true'
        return HttpResponse(simplejson.dumps(dic))

#获取当前登录用户
def get_current_user(request):
    if request.method == 'GET':
        
        print request.session
        
        return HttpResponse(simplejson.dumps('ok'))

#提交当前用户的events    
def confirm_actual_tasks(request):
    print 'confirm_actual_tasks'
    
    if request.method == 'POST':
        
        uid = request.POST['uid']
        date = request.POST['date']
        dic = {}
        
        #查询当前用户提交但未审核的daily_events
#        tasks=[]
#        tasks = Actual_Daily.objects.filter(user_id=uid, date=date, status=Actual_Status.objects.get(id=1))
#        if len(tasks) != 0:
#            for t in tasks:
#                print t
#                t.status = Actual_Status.objects.get(id=2)
#                t.save()
#            
#        else:
#            return HttpResponse(simplejson.dumps('failed'))
        daily = Actual_Daily.objects.get(user=User.objects.get(id=uid), date=date)
        
        permit_flag = True
        
        #工作时间 <= 8小时, 休息时间>=0.5小时
        #工作时间 > 8小时, 休息时间>=1小时,>=2次
        workseconds = 0
        breakseconds = 0
        breakcount = 0
        task = Actual_Task.objects.filter(daily = daily)
        for t in task:
            print 'start_time    ', t.start_time
            print 'end_time', t.end_time
            print 'time bewteen', (t.end_time - t.start_time).seconds
            try:
                if t.mission != None:
                    n = t.mission.id
                    if n == 1 or n == 4 or n == 5 or n == 6 or n == 7 :
                        breakseconds += (t.end_time - t.start_time).seconds
                        breakcount += 1
                    else:
                        workseconds += (t.end_time - t.start_time).seconds
                else:
                    workseconds += (t.end_time - t.start_time).seconds
            except:
                workseconds += (t.end_time - t.start_time).seconds
        
        
        print 'workseconds    ', workseconds
        print 'breakseconds   ', breakseconds
        
        if workseconds <= 28800:
            if breakseconds >= 1800:
                permit_flag = True
            else:
                permit_flag = False
                dic['msg'] = '提交失败,工作时间在8小时以内(含8小时),休息时间应大于0.5小时'
                dic['result'] = False
                
        else:
            if breakseconds >= 3600 and breakcount >= 2:
                permit_flag = True
            else:
                permit_flag = False
                dic['msg'] = '提交失败,工作时间在8小时以上,应当至少有两次休息且时间总和大于1小时'
                dic['result'] = False
                
        #提交
        if permit_flag == True:
            if (daily.status == Actual_Status.objects.get(id=1)):
                daily.status = Actual_Status.objects.get(id=2)
                daily.save()
                dic['result'] = True
                return HttpResponse(simplejson.dumps(dic))
            #再提交
            elif (daily.status == Actual_Status.objects.get(id=8)):
                
                try:
                    rejected_by = daily.rejected_by
                    if(rejected_by == 0 or rejected_by == ''):
                        daily.status = Actual_Status.objects.get(id=2)
                    else:
                        #状态恢复
                        rank = Confirm.objects.get(user = User.objects.get(id=rejected_by)).rank
                        daily.status = Actual_Status.objects.get(id=rank + 1)
                        
                except:
                    daily.status = Actual_Status.objects.get(id=2)
                finally:
                    daily.save()
                    dic['result'] = True
                    return HttpResponse(simplejson.dumps(dic))
                    
            else:
                dic['result'] = False
                return HttpResponse(simplejson.dumps(dic))
        else:
            dic['result'] = False
            return HttpResponse(simplejson.dumps(dic))

#审核修改状态  确认修改
def applychange_actual_tasks(request):
    print 'confirm_actual_tasks'
    
    if request.method == 'POST':
        
        uid = request.POST['uid']
        date = request.POST['date']
        sid = request.POST['sid']
        
        #查询当前用户提交但未审核的daily_events
#        tasks=[]
#        tasks = Actual_Daily.objects.filter(user_id=uid, date=date, status=Actual_Status.objects.get(id=1))
#        if len(tasks) != 0:
#            for t in tasks:
#                print t
#                t.status = Actual_Status.objects.get(id=2)
#                t.save()
#            
#        else:
#            return HttpResponse(simplejson.dumps('failed'))
        task = Actual_Daily.objects.get(user=User.objects.get(id=uid), date=date)
        rank = Confirm.objects.get(user = request.user).rank
        if sid == '1':
            task.status = Actual_Status.objects.get(id = rank + 2)
        else:
            task.status = Actual_Status.objects.get(id = sid)
        task.save()
        return HttpResponse(simplejson.dumps('ok'))
    
#审核修改状态  页面关闭返回原状态
def restore_daily_status(request):
    print 'restore_daily_status'
    
    if request.method == 'POST':
        
        uid = request.POST['uid']
        date = request.POST['date']
        sid = request.POST['sid']
        
        print uid
        print date
        print sid
        
        try:
            daily = Actual_Daily.objects.get(user=User.objects.get(id=uid), date=date)
            daily.status = Actual_Status.objects.get(id = sid)
            daily.rejected_by = uid
            daily.save()
        finally:
            return HttpResponse(simplejson.dumps('ok'))

'''
timesheet审核
'''
def timesheet_judge(request):
    print 'timesheet_judge'
    if request.method == 'GET':
        uid = request.GET['uid']
        date = request.GET['date']
        option = request.GET['option']
        rank = Confirm.objects.get(user = request.user).rank
        
        print uid
        print date
        print option
        
        daily = Actual_Daily.objects.get(user=User.objects.get(id=uid), date=date)
        status = daily.status.id
        print status
        if(option == 'accept'):
            daily.status = Actual_Status.objects.get(id=rank + 2)
            daily.save()
            return HttpResponse(simplejson.dumps('accept'))
        
        elif(option == 'reject'):
            daily.status = Actual_Status.objects.get(id=8)
            daily.rejected_by = request.user.id
            daily.save()
            return HttpResponse(simplejson.dumps('reject'))

#timesheet报表显示
def report_detail(request):
    print 'report_detail'
    info = {}
    if request.method == 'GET':
        uid = request.GET['uid']
        startdate = request.GET['startdate']
        enddate = request.GET['enddate']
        
        
        #查询用户的Timesheet信息
        reportUser = User.objects.get(id=uid)
        daily = Actual_Daily.objects.filter(user=reportUser, date__gt=startdate, date__lte=enddate).order_by('date')
        
        i = 0
        l = []
        for d in daily:
            k={}
            
            k['user'] = d.user.first_name    #用户名
            k['date'] = timezone.localtime(d.date).strftime('%Y-%m-%d')                #日期
            k['status'] = d.status.name        #状态
            
            i += 1
            l.append(k)
            
            actualTask = Actual_Task.objects.filter(daily=d).order_by('start_time')
            for at in actualTask:
                k={}
                k['title'] = at.title
                if(at.start_time == None):
                    k['startTime'] = ''
                else:
                    k['startTime'] = timezone.localtime(at.start_time).strftime('%H:%M:%S')    #开始时间
                
                if(at.end_time == None):
                    k['endTime'] = ''
                else:
                    k['endTime'] = timezone.localtime(at.end_time).strftime('%H:%M:%S')     #结束时间
                k['desc'] = at.desc
                
                i += 1
                l.append(k)

        info['total'] = i
        info['rows'] = l
        
    return HttpResponse(simplejson.dumps(info))

#timesheet统计信息显示
def statistic_detail(request):
    print 'statistic_detail'
    info = {}
    if request.method == 'GET':
        uid = request.GET['uid']
        startdate = request.GET['startdate']
        enddate = request.GET['enddate']
        
        #统计类列表
        actualTaskStatisicList = []
        
        taskCount = 0
        
        daily = Actual_Daily.objects.filter(user=User.objects.get(id=uid), date__gt=startdate, date__lte=enddate)
        for d in daily:
            actualTask = Actual_Task.objects.filter(daily=d)
            
            for at in actualTask:
                timeDeltaObj = at.end_time - at.start_time
                timeDelta = timeDeltaObj.seconds / 3600
                
                #当前任务Id和类型
                curType = at.type
                if curType == 1:
                    curTask = at.task_id
                else:
                    curTask = at.mission.id
#                    print 'mission id    ', curTask.id
#                    print 'at.mission id    ', at.mission.id
                
#                print 'actualTask    ', at
#                print 'curType    ', curType
#                print 'curTask    ', curTask.id
                
                #遍历当前列表查找是否重复
                taskFounded = False
                for atsl in actualTaskStatisicList:
                    if atsl.type == curType:
                        if atsl.task == curTask:
                            #添加时间到任务
                            atsl.hours += timeDelta
                            taskFounded = True
                if taskFounded == False:
                    actualTaskStatisic = Actual_Task_Statisic()
                    actualTaskStatisic.type = curType
                    actualTaskStatisic.task = curTask
                    actualTaskStatisic.title = at.title
                    actualTaskStatisic.hours = timeDelta
                    actualTaskStatisicList.append(actualTaskStatisic)
                
                taskCount += 1
                
        print 'taskCount    ', taskCount
        
        i = 0
        l = []
        
        for atsl in actualTaskStatisicList:
            row = {}
            row['taskId'] = atsl.task
            row['task'] = atsl.title
            row['hours'] = atsl.hours
            
            l.append(row)
        
        info['total'] = i
        info['rows'] = l
        
    return HttpResponse(simplejson.dumps(info))    

def taskStatistic_detail(request):
    print 'taskStatistic_detail'
    info = {}
    if request.method == 'GET':
        startdate = request.GET['startdate']
        enddate = request.GET['enddate']
    
        print 'startdate     ', startdate
        print 'enddate       ', enddate
        
        #统计类列表
        actualTaskStatisicList = []
        
        taskCount = 0
        
        daily = Actual_Daily.objects.filter(date__gt=startdate, date__lte=enddate)
        for d in daily:
            actualTask = Actual_Task.objects.filter(daily=d)
            
            for at in actualTask:
                timeDeltaObj = at.end_time - at.start_time
                timeDelta = timeDeltaObj.seconds / 3600
                
                #当前任务Id和类型
                curType = at.type
                if curType == 1:
                    curTask = at.task_id
                else:
                    curTask = at.mission.id
                    
                #遍历当前列表查找是否重复
                taskFounded = False
                for atsl in actualTaskStatisicList:
                    if atsl.type == curType:
                        if atsl.task == curTask:
                            #添加时间到任务
                            atsl.hours += timeDelta
                            taskFounded = True
                if taskFounded == False:
                    actualTaskStatisic = Actual_Task_Statisic()
                    actualTaskStatisic.type = curType
                    actualTaskStatisic.task = curTask
                    actualTaskStatisic.title = at.title
                    actualTaskStatisic.hours = timeDelta
                    actualTaskStatisicList.append(actualTaskStatisic)
                
                taskCount += 1
                
        print 'taskCount    ', taskCount
        
        i = 0
        l = []
        
        for atsl in actualTaskStatisicList:
            row = {}
            row['taskId'] = atsl.task
            row['task'] = atsl.title
            row['hours'] = atsl.hours
            if atsl.type == 1:
                row['user'] = Task.objects.get(id=atsl.task).user.all()[0].first_name

            else:
                row['user'] = ''
            
            l.append(row)
        
        info['total'] = i
        info['rows'] = l
                
    return HttpResponse(simplejson.dumps(info))


'''
timesheet数据库迁移
'''
def data_transfer(request):
    
    
    
    print 'data_transfer'
    dic={}
    if request.method == 'GET':
        import MySQLdb
        
        conn = MySQLdb.connect(host='172.16.253.192', user='root', passwd='123123',db='CGProjManSys', charset="utf8")
        
#Daily 表 数据迁移

        count = 0
        cursor = conn.cursor()
        cursor.execute('select * from ProjMan_actual_daily')
        for r1 in cursor.fetchall():
            
            #旧数据库取对应用户名
            cursor_user = conn.cursor()
            cursor_user.execute('select username from auth_user where id = ' + str(r1[2]))
            username =  cursor_user.fetchall()[0][0]
#            print 'old  username     :', username
            
            #根据用户名查询新id
            userNew = None
            try:
                userNew = User.objects.get(username = username)
            except:
                userNew = None
            
            if userNew != None:
#                    print userNew.first_name
#                    Actual_Daily.objects.create(date=r1[1], user=userNew, status=r1[3], rejected_by=r1[4])
#                    Actual_Daily.save()
                print r1[0], '   ',r1[1], '  ', userNew, '  ', r1[3], '   ', r1[4]
                dailyNew = Actual_Daily()
                dailyNew.id = r1[0]
                dailyNew.date =  timezone.localtime(r1[1])
                dailyNew.user = userNew
                dailyNew.status=Actual_Status.objects.get(id=int(r1[3]))
                dailyNew.rejected_by = r1[4]
                dailyNew.save()
#                    Actual_Daily.objects.create(date=r1[1], user=userNew, status=Actual_Status.objects.get(id=int(r1[3])), rejected_by=int(r1[4]))
        
            
            count += 1
        print count
#Daily 表 数据迁移

#Task 表 数据迁移

        count = 0
        cursor = conn.cursor()
        cursor.execute('select * from ProjMan_actual_task')
        for r2 in cursor.fetchall():
#            print r2
            taskNew = Actual_Task()
            taskNew.id = r2[0]
            taskNew.type = int(r2[2])
            taskNew.title = r2[3]
            
            if taskNew.type == 1:
                #查询所属task
#                cursor_task = conn.cursor()
#                cursor_task.execute('select project_id, asset_id from ProjMan_task_asset where id = ' + str(r2[4]))
#                csl = cursor_task.fetchall()[0]
#                project_id =  csl[0]
#                asset_id =  csl[1]
#                
#                #task所属project, asset
#                cursor_project = conn.cursor()
#                cursor_project.execute('select name from ProjMan_project where id = ' + str(project_id))
#                project_name =  cursor_project.fetchall()[0][0]
#                
#                cursor_asset = conn.cursor()
#                cursor_asset.execute('select name from ProjMan_asset where id = ' + str(asset_id))
#                asset_name =  cursor_asset.fetchall()[0][0]
#                
#                print project_name,'    ' ,asset_name
#                
#                try:
#                    taskNew.task=Task.objects.get(project=Project.objects.get(name=project_name, task_group=TaskGroup.objects.get(name=asset_name)))
#                except:
#                    taskNew.task=None
                try:
                    taskNew.task = Task.objects.get(id=r2[4])
                except:
                    pass
            else:
                taskNew.mission = Mission.objects.get(id=r2[5])
            
            taskNew.start_time = timezone.localtime(r2[6])
            taskNew.end_time = timezone.localtime(r2[7])
            taskNew.desc = r2[8]
            
            try:
                taskNew.daily = Actual_Daily.objects.get(id=int(r2[1]))
                taskNew.save()
            except:
                pass
            count += 1
        print count
        
#Task 表 数据迁移
            
        conn.close()
        
        return HttpResponse(simplejson.dumps(dic))

#审核修改
def comfirm_change(request):
    print 'comfirm_change'
    dic={}
    
    confirm = Confirm.objects.all()
    
    for c in confirm:
        if c.superior_id == 39:
            c.superior_id = 56
        if c.superior_id == 56:
            c.superior_id = 39
        c.save()
    return HttpResponse(simplejson.dumps(dic))
            

def adminlist(request):
    #人员详情获取
    info = {}
    if request.method == 'GET':
        
        admin_confirm = Confirm.objects.filter(rank = 1)
        
        i = 0
        l = []
        for c in admin_confirm:
            try:
                profile = UserProfile.objects.get(user = c.user)
            except:
                profile = ''
            i +=1
            k = {}
            k['id'] = c.user.id
            k['user'] = c.user.username
            k['name'] = c.user.first_name           
            k['email'] = c.user.email
            if profile:
                k['sex'] = profile.sex
                k['phone'] = profile.phone
                if profile.department:
                    k['department'] = profile.department.name
                if profile.position:
                    k['position'] = profile.position.name
                if profile.thum:
                    k['img'] = profile.thum.url
                if profile.seatnumber:
                    k['seatnumber'] = profile.seatnumber
            k['is_superuser'] = c.user.is_superuser
            l.append(k)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))


        