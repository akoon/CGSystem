# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from models import *
from ProjectManSys.models import *
import datetime, time
from django.utils import timezone
import string

def get_schedule_tasks(request, uid):
    print 'get_schedule_tasks'
    print 'uid    ', uid
    if request.method == 'GET':
        print 'get_schedule_tasks'
        #user_id= request.user.id

        dic={}
        task_list=[]
        
        user = User.objects.get(id=uid)
        
        #查询task_daily
        task_daily = Schedule_Daily.objects.filter(user=user)
        
        for td in task_daily:
            task = Schedule_Task.objects.filter(daily = td)
            
            #查询task——daily所属的task list
            for t in task:
                
                #关联用户读取
                shared_users_str = ''
                shared_users_name = ''
                shared_users = t.user.all()
                for su in shared_users:
                     shared_users_str = shared_users_str + str(su.id) + ','
                     shared_users_name = shared_users_name + str(su.first_name) + ','
                     
                task_line = {'id': t.id, 'daily': td.id,  'title': t.title, 'start': timezone.localtime(t.start_time).strftime('%Y-%m-%d %H:%M:%S'), 'end': timezone.localtime(t.end_time).strftime('%Y-%m-%d %H:%M:%S'),'notes': t.desc,'user': shared_users_str, 'delivered': shared_users_name, 'editable': True}
                
                #判定任务状态
                task_line['cid']= t.status.id
                
                task_list.append(task_line)
            
        #查询其他用户创建共享给我的tasks
        shared_tasks = user.schedule_task_set.all()
                
        print 'shared_tasks   :', shared_tasks
        for st in shared_tasks:
            task_line = {'id': st.id, 'daily': st.daily.id, 'title': st.title + '    --来自 : ' + st.daily.user.first_name, 'start': timezone.localtime(st.start_time).strftime('%Y-%m-%d %H:%M:%S'), 'end': timezone.localtime(st.end_time).strftime('%Y-%m-%d %H:%M:%S'),'notes': st.desc,'editable': False}
            #判定任务状态
            task_line['cid']= 10
            task_list.append(task_line)
        
            
        dic['success'] ='true'
        dic['tasks']=  task_list
        return HttpResponse(simplejson.dumps(dic))
    
def add_schedule_tasks(request, uid):
    print 'add_schedule_task'
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
        
        id = event['id']
        title = event['title']
        start = event['start'].replace('T', ' ')
        end = event['end'].replace('T', ' ')
        notes = event['notes']
        cid = event['cid']
        users = event['user'].split(',')
        print 'start    ', start
        print 'end      ', end
        
        print 'cid      ', cid
        
        #所属daily日期
        daily_date = start[:10]
        
        #写入权限
        
        daily = None
        
        #user_id= request.user.id
        user_id = uid
        #current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        if Schedule_Daily.objects.filter(user_id=user_id, date = daily_date).exists() == False:
            #如果daily不存在,则新建根据task start date
            daily = Schedule_Daily.objects.create(date = daily_date,user_id = user_id)

        else:
            
            daily=Schedule_Daily.objects.get(user_id=user_id, date=daily_date)
        

        task_new = Schedule_Task.objects.create( daily=daily, title=title.decode('unicode_escape'), start_time=start, end_time=end, status=Schedule_Status.objects.get(id=cid), desc=notes.decode('unicode_escape'))
        
        for user in users:
            if user == '' or user == None:
                pass
            else:
                task_new.user.add(User.objects.get(id=user))
            
        task_new.save()
        
        
        #结果赋值
        dic['tasks'] = {"id":task_new.id, "cid":cid, "title":title.decode('unicode_escape'), "start":event['start'], "end":event['end'], "rrule":event['rrule'], "notes":notes.decode('unicode_escape'), "ad":false, "rem":event['rem'], "daily":daily.id, "user":users, 'editable': True}

        dic['success'] ='true'
        
        return HttpResponse(simplejson.dumps(dic))
    
    
def update_schedule_task(request, uid):
    print 'update_schedule_task'
    print 'uid    ', uid
    if request.method == 'POST':
        print request.POST
        
        dic = request.POST.dict()
        print dic
        event = dic.keys()[0]
        event = event.encode('utf-8')
        false = False
        true = True
        null = None
        
        event = eval(event)
        
        id = event['id']
        
        #id成为 Extensible.calendar.data.EventModel-323 格式的bug
        pos = string.find(str(id), '-')
        if pos != -1:
            id = id[pos + 1:]
            print 'converted   id ', id
        
        cid = event['cid']
        title = event['title']
        start = event['start'].replace('T', ' ')
        end = event['end'].replace('T', ' ')
        notes = event['notes']
        #user_id= request.user.id
        user_id = uid    
#        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        dic={}
        
        task_date = start[:10]

        #查询所属daily
        print 'id    :', id
        task = Schedule_Task.objects.get(id=id)
        daily = task.daily
        
        #所属daily日期
        daily_date = daily.date
        print daily_date
        
        users = event['user']
        if users != '' and users != None:
            users = users.split(',')
             
            #删除原关联
            for old_user in task.user.all():
                task.user.remove(old_user)
                
            #添加关联关系
            for user in users:
                if user != None and user != '' and user != ' ':
                    print 'user      ', User.objects.get(id=int(user))
                    task.user.add(User.objects.get(id=int(user)))
                
                
        if daily_date != task_date:
            print 'move to a different day'
            
            daily_new = None
            if Schedule_Daily.objects.filter(user_id=user_id, date = task_date).exists() == False:
                #如果目的daily不存在,则新建根据task start date
                daily_new = Schedule_Daily.objects.create(date = task_date,user_id = user_id)
                
            else:
                #如果目的daily存在
                daily_new = Schedule_Daily.objects.get(user_id=user_id, date = task_date)
            
            task.daily = daily_new
 
        task.title=title.decode('unicode_escape')
        task.status = Schedule_Status.objects.get(id=cid)
        task.start_time=start
        task.end_time=end
        task.desc=notes.decode('unicode_escape')
        
        task.save()         
        
        
        
        #如果原daily下无task, 删除原daily
        t = Schedule_Task.objects.filter(daily=daily)
        print 'len(t)    ', len(t)
        print 't    ',    t
        print 'daily.id    ', daily.id
        if len(t) == 0:
            daily.delete()
            
        dic['success'] ='true'
        
        return HttpResponse(simplejson.dumps(dic))
    
def remove_schedule_task(request, uid):
    print 'remove_schedule_task'
    print 'uid    ', uid
    if request.method == 'POST':
        print request.POST
        
        dic = request.POST.dict()
        print dic
            
        task = dic.keys()[0]
        task = task.encode('utf-8')
        false = False
        true = True
        task = eval(task)
        
        id=task['id']
        #id成为 Extensible.calendar.data.EventModel-323 格式的bug
        pos = string.find(str(id), '-')
        if pos != -1:
            id = id[pos + 1:]
            print 'converted   id ', id
        
        t = Schedule_Task.objects.get(id = id)
        daily = t.daily
        t.delete()
        
        #如果daily下属没有task, 则删除daily
        if Schedule_Task.objects.filter(daily=daily).count() == 0:
            daily.delete()
            print 'daily has benn deleteded'
        
        dic['success'] ='true'
        return HttpResponse(simplejson.dumps(dic))    

#返回task的状态列表
def get_schedule_status(request):
    if request.method == 'GET':
        print 'get_schedule_status'
        dic={}
        status_list=[]
        
        for status in Schedule_Status.objects.all(): 
            s={}
            s['id']=status.id
            s['title']=status.name
            s['color']=status.id
            
            status_list.append(s)
                
        dic['status']=  status_list
        dic['success'] ='true'              
        return HttpResponse(simplejson.dumps(dic))

#日历可关联用户列表
def get_user_combo(request):
    print 'get_user_tasks_combo' 
    if request.method == 'GET':
        user_list=[]

        for user in User.objects.all():
            if user.id == 1 or user == request.user:
                continue
            u={}
            u['id']=str(user.id)
            u['name']=user.first_name

            user_list.append(u)

        return HttpResponse(simplejson.dumps(user_list))
    
    