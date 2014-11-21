# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from django.core.files.base import ContentFile
from models import *
import uuid
from PillarsCGSystem.common import *
from django.core import mail
from PillarsCGSystem import settings
from PillarsCGSystem import globalvar
from forms import *
from django.forms.models import modelform_factory
import time

import TimeSheetSys.models
from django.utils import timezone

def position_read(request,index):
    #职位search,list
    info = []
    if request.method == 'GET':
        if index :
            print '获取一条数据'
        else:
            positions = Position.objects.all()
            for p in positions:
                i = {}
                i['id'] = p.id
                i['name'] = p.name
                info.append(i)
    return HttpResponse(simplejson.dumps(info))

def position_detail(request):
    #职位详情获取
    info = {}
    if request.method == 'GET':       
        positions = Position.objects.all()
        i = 0
        l = []
        for p in positions:
            i += 1
            d = {}
            d['id'] = p.id
            d['name'] = p.name
            d['desc'] = p.desc
            l.append(d)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))

def position_create(request):
    Model = Position
    
    info = {}
    if request.method == 'POST':
        try:
            Form = modelform_factory(Model)
            form = Form(request.POST)
            form.save()
            info['message']="添加成功"
            info['success']=True
        except:
            info['message']="添加失败，请输入正确字段"
            info['success'] = False
        finally:
            return HttpResponse(simplejson.dumps(info))
            

def position_update(request):
    Model = Position
    
    info = {}
    if request.method == 'POST':
        try:
            Form = modelform_factory(Model)
            pk = request.POST.get('id','')
            instance = Model.objects.get(pk=pk)
            form = Form(request.POST, instance = instance)
            form.save()
            info['success']=True
        except:
            info['success'] = False
            
        finally:
            return HttpResponse(simplejson.dumps(info))

def position_destroy(request):
    #职位删除
    info = {}
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            p = Position.objects.get(id=id)
            
            #判断是否有外键在使用
            people = UserProfile.objects.filter(position = p)
            if people:
                info['success']=False
                info['errors'] = '此部门在账户中被使用'
                return HttpResponse(simplejson.dumps(info))
            
            p.delete()
        info['success']=True
    return HttpResponse(simplejson.dumps(info))



# def position_create(request):
#     #职位添加
#     info = {}
#     if request.method == 'POST':
#         name = request.POST.get('name','')
#         desc = request.POST.get('desc','')
#         Position.objects.create(name=name, desc=desc)
#         info['success']=True
#     return HttpResponse(simplejson.dumps(info))

# def position_update(request):  
#     #职位修改
#     info = {}
#     if request.method == 'POST':
#         id = request.POST.get('id','')
#         name = request.POST.get('name','')
#         desc = request.POST.get('desc','')
#                    
#         p = Position.objects.filter(id=id)[0]
#         p.name = name
#         p.desc = desc
#         p.save()
#         info['success']=True
        
#     return HttpResponse(simplejson.dumps(info))

def department_read(request,index):
    #部门search,list
    info = []
    if request.method == 'GET':      
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所以父节点  
                p_department = Department.objects.filter(parent = 0)
                for p in p_department:
                    i = {}
                    i['id'] = p.id
                    i['name'] = p.name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                print index
                pass
        else:
            #获取整个列表
            p_department = Department.objects.filter(parent = 0)
            for p in p_department:
                i = {}
                i['id'] = p.id
                i['text'] = p.name
                department = Department.objects.filter(parent = p.id)
                j = []
                if department:
                    for d in department:
                        k = {}
                        k['id'] = d.id
                        k['text'] = d.name
                        j.append(k)
                i['children'] = j
#               i['state'] = "closed"
                info.append(i) 
    return HttpResponse(simplejson.dumps(info))

def department_detail(request):
    #部门详情获取
    info = []
    if request.method == 'GET':      
        p_department = Department.objects.filter(parent = 0)
        for p in p_department:
            i = {}
            i['id'] = p.id
            i['name'] = p.name
            i['desc'] = p.desc
            i['iconCls'] = "icon-blank"
            department = Department.objects.filter(parent = p.id)
            j = []
            if department:
                for d in department:
                    k = {}
                    k['id'] = d.id
                    k['name'] = d.name
                    k['desc'] = d.desc
                    k['iconCls'] = "icon-blank"
                    j.append(k)
            i['children'] = j
#            i['state'] = "closed"
            info.append(i) 
    return HttpResponse(simplejson.dumps(info))

# def department_create(request):
#     Model = Department
#     
#     info = {}
#     if request.method == 'POST':
#         try:
#             Form = modelform_factory(Model)
#             form = Form(request.POST)
#             form.save()
#             info['message']="添加成功"
#             info['success']=True
#         except:
#             info['message']="添加失败，请输入正确字段"
#             info['success'] = False
#         finally:
#             return HttpResponse(simplejson.dumps(info))
#     

def department_create(request):
    #部门添加
    info = {}
    if request.method == 'POST':
        parent = request.POST.get('parent','')
        name = request.POST.get('name','')
        desc = request.POST.get('desc','')
         
        if name:
            if parent:             
                parent = int(parent)
                parent_object = Department.objects.get(pk=parent)
                if parent_object:
                    Department.objects.create(name = name,parent = parent,desc = desc)
            else:
                Department.objects.create(name = name,parent = 0,desc = desc) 
            info['success']=True
        else:
            info['success']=False
            info['errors'] = "添加失败"
             
    return HttpResponse(simplejson.dumps(info))

def department_destroy(request):
    #部门删除
    info = {}
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            
            p = Department.objects.filter(id=id)[0]
            
            #判断是否有外键在使用
            people = UserProfile.objects.filter(department = p)
            if people:
                info['success']=False
                info['errors'] = '此部门在账户中被使用'
                return HttpResponse(simplejson.dumps(info))
            p.delete()
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

def department_update(request):  
    #部门修改
    info = {}
    if request.method == 'POST':
        id = request.POST.get('id','')
        parent = request.POST.get('parent','')
        name = request.POST.get('name','')
        desc = request.POST.get('desc','')
        if id and parent!=id:
            p = Department.objects.filter(id=id)[0]
            if parent:
                p.parent = int(parent)
            p.name = str(name)
            p.desc = str(desc)
            p.save()
            info['success']=True     
    return HttpResponse(simplejson.dumps(info))

def people_read(request,index):
    #人员search,list
    info = []
    if request.method == 'GET':      
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所以父节点  
                p_people = User.objects.filter(is_active = 1)
                for p in p_people:
                    i = {}
                    i['id'] = p.id
                    i['name'] = p.first_name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                print index
                try:
                    pp = ProjectPeople.objects.get(project__id__exact = index)
                    people = User.objects.exclude(id__in = [user.id for user in pp.users.all()])
                    for p in people:
                        if p.is_active == 1:
                            i = {}
                            i['id'] = p.id
                            i['user'] = p.username
                            i['name'] = p.first_name           
                            i['email'] = p.email
                            info.append(i)
                except:
                    p_people = User.objects.filter(is_active = 1)
                    for p in p_people:
                        i = {}
                        i['id'] = p.id
                        i['user'] = p.username
                        i['name'] = p.first_name           
                        i['email'] = p.email
                        info.append(i)
        else:
            #获取整个列表
            pass
    return HttpResponse(simplejson.dumps(info))

def people_detail(request):
    #人员详情获取
    info = {}
    if request.method == 'GET':
        peoples = User.objects.filter(is_active = 1)
        i = 0
        l = []
        for p in peoples:
            try:
                profile = UserProfile.objects.get(user = p)
            except:
                profile = ''
            i +=1
            k = {}
            k['id'] = p.id
            k['user'] = p.username
            k['name'] = p.first_name           
            k['email'] = p.email
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
                if profile.birthday:    
                    k['birthday'] = timezone.localtime(profile.birthday).strftime('%Y-%m-%d') 
                else:
                    k['birthday'] = ''
                k['bloodtype'] = profile.case_bloodtype()
                k['constellation'] = profile.case_constellation()
                k['hobby'] = profile.hobby
            k['is_superuser'] = p.is_superuser
            l.append(k)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))


# def people_create(request):
# #     info = {}
#     if request.method == 'POST':
#         try:
#             form = UserForm(request.POST)
#             new_user = form.save()
#             print new_user
#         except:
#             pass
#     
# def people_update(request):
#     if request.method == 'POST':
#         pk = request.POST.get('id','')
#         user = UserProfile.objects.get(pk=pk)
#         form = UserForm(request.POST, instance = user)
#         form.save()
#         

def people_create(request):
    #人员添加
    info = {}
    if request.method == 'POST':
         
        user = request.POST.get('user','')
        name = request.POST.get('name','')
        sex = request.POST.get('sex','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        department = request.POST.get('department','')
        position = request.POST.get('position','')
        seatnumber = request.POST.get('seatnumber', '')
        birthday = request.POST.get('birthday', '')
        bloodtype = request.POST.get('bloodtype')
        constellation = request.POST.get('constellation')
        hobby = request.POST.get('hobby', '')
        if sex == '':
            sex = 0
        if department == '':
            d = None
        if position == '':
            p = None
            
        if birthday == '':
            birthday = None
        if bloodtype:
            bloodtype = int(bloodtype)
        else:
            bloodtype = None    
        if constellation:
            constellation = int(constellation)
        else:
            constellation = None         
        if not user :
            info['success']=False
        elif not name:
            info['success']=False
        else:
            try:
                u = User.objects.create_user(username = user, email = email, password = '123456')
                u.first_name = name
                u.save()
                if department != '':
                    d = Department.objects.get(id = department)
                if position != '':
                    p = Position.objects.get(id = position)
                 
                UserProfile.objects.create(user=u, department = d, position = p, sex = int(sex), phone = phone, seatnumber = seatnumber,
                                           birthday = birthday, bloodtype = bloodtype, constellation = constellation, hobby = hobby)
                #同时在Timesheet审核关系表中创建
                c = TimeSheetSys.models.Confirm.objects.create(user=u, superior=User.objects.get(id=1), rank=0, rank_require=1)
                c.save()
                 
                info['success']=True
            except Exception as e:
                print str(e)
                info['success']=False
                 
             
    return HttpResponse(simplejson.dumps(info))

def people_destroy(request):
    #人员删除
    info = {}
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            p = User.objects.get(id=id)
            p.is_active = False
            p.save()
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

def people_update(request):  
    #人员修改
    info = {}
    if request.method == 'POST':
        id = request.POST.get('id','')
        user = request.POST.get('user','')
        name = request.POST.get('name','')
        sex = request.POST.get('sex','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        department = request.POST.get('department','')
        position = request.POST.get('position','')
        seatnumber = request.POST.get('seatnumber', '')
        birthday = request.POST.get('birthday', '')
        bloodtype = request.POST.get('bloodtype', '')
        constellation = request.POST.get('constellation', '')
        hobby = request.POST.get('hobby', '')

        try:
            sex = int(sex)
        except:
            sex = ''
        try:
            department = int(department)
        except:
            department = ''
        try:
            position = int(position)
        except:
            position = ''
        
        if birthday == '':
            birthday = None
            
        try:
            bloodtype = int(bloodtype)
        except:
            bloodtype = None
            
        try:
            constellation = int(constellation)
        except:
            constellation = None         

        if id:
            u = User.objects.get(id = id)
            if user:
                u.username = user
            if name:
                u.first_name = name
            if email:
                u.email = email
            if user or name or email:
                u.save()
            if department:
                d = Department.objects.get(id = department)
            else:
                d = None
            if position:
                p = Position.objects.get(id = position)
            else:
                p = None
            try:
                pro = UserProfile.objects.filter(user = u)[0]  
                if sex != '':
                    pro.sex = sex
                if phone:
                    pro.phone = phone
                if d:
                    pro.department = d
                if p:
                    pro.position = p
                if seatnumber:
                    pro.seatnumber = seatnumber
                    
                pro.birthday = birthday
                pro.bloodtype = bloodtype
                pro.constellation = constellation
                pro.hobby = hobby
                pro.save()
            except Exception as e:
                print str(e)
                UserProfile.objects.create(user=u, department = d, position = p, sex = sex, phone = phone, seatnumber = seatnumber,
                                           birthday = birthday, bloodtype = bloodtype, constellation = constellation, hobby = hobby)  
             
            info['success']=True     
    return HttpResponse(simplejson.dumps(info))

def people_img(request):  
    #人员图片上传
    info = {}
    if request.method == 'POST':
        file = request.FILES.get('peopleImage', None)
        id = request.POST.get('id', None)  
        if  file and id:
            userprofile = UserProfile.objects.get(user__id=id)
            file_content = ContentFile(file.read())
            userprofile.thum.save(str(uuid.uuid1())+os.path.splitext(file.name)[1], file_content)           
        info['sucess']=True
    return HttpResponse(simplejson.dumps(info))

def send_mail(request):
    #邮件发送
    info = {}
    if request.method == 'GET':
        print 'send_mail'
        
        userFrom = request.user
        
        recipientIdList = [82]
        recipientList = []
        
        for ril in recipientIdList:
            user = User.objects.get(id=ril)
            recipientList.append(user.email)
        mail.send_mail('标题', '内容', userFrom.email, recipientList)
#        send_mail(str(subject), str(message), fromEmail, recipientList, fail_silently=False, auth_user=fromEmail, auth_password=authPass)


#        print userFrom.first_name
        
    return HttpResponse(simplejson.dumps(info))

def systemenvironment_detail(request):
    info = {}
    if request.method == 'GET':
        databases = {}
        databases['databasesname'] = settings.DATABASES['default']['NAME']
        databases['databasesuser'] = settings.DATABASES['default']['USER']
        databases['databaseshost'] = settings.DATABASES['default']['HOST']
        databases['databasesport'] = settings.DATABASES['default']['PORT']
        info['databases'] = databases
        info['mountdir'] = globalvar.MOUNTDIR
    return HttpResponse(simplejson.dumps(info))

#提交反馈意见
def report(request):
    info = {}
    
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content', None)
        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        if content == '' or content == None:
            info['success'] = False
        else:
            feedback = Feedback.objects.create(user=user,content=content,creat_time=current_date)
            feedback.save()
            info['success'] = True
    
    return HttpResponse(simplejson.dumps(info))
    
#浏览我的反馈
def my_report(request):
    info = {}
    user = request.user
    if request.method == 'POST':
        feedback = Feedback.objects.filter(user=user)
        i = 0
        l = []
        for fb in feedback:
            i += 1
            d = {}
            d['id'] = fb.id
            d['content'] = fb.content
            d['creat_time'] = timezone.localtime(fb.creat_time).strftime('%Y-%m-%d') 
            l.append(d)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))
    
    return HttpResponse(simplejson.dumps(info))