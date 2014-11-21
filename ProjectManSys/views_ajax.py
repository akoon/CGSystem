# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from models import *
import datetime
import uuid
from django.utils import timezone

from django.forms.models import modelform_factory
from django.utils import timezone
from PillarsCGSystem.common import groupsTree
from PillarsCGSystem.common import taskgroupTree
from PillarsCGSystem.common import taskgroupTreeRelateable
from PillarsCGSystem.common import dateCompare
from django.core.files.base import ContentFile
import re, time, uuid, os, json, shutil, difflib, traceback
from django.views.decorators.gzip import gzip_page 
from PillarsCGSystem.settings import MEDIA_ROOT  
from PillarsCGSystem.common import *
from PillarsCGSystem import globalvar

from django.forms.models import modelform_factory
from django.contrib.admin.util import model_format_dict
# from gtk import FALSE

#状态search,list
def status_read(request,index):
    info = []
    if request.method == 'GET':
        if index :
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所有
                status = Status.objects.all()
                for t in status:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
            
            elif index == 1:
                #0获取所有项目类型
                status = Status.objects.filter(type = -1)
                for t in status:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
            elif index == 2:
                #0获取所有资产类型
                status = Status.objects.filter(type = -2)
                for t in status:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
            elif index == 3:
                #0获取所有任务类型
                status = Status.objects.filter(type = -3)
                for t in status:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
        else:
            #获取整个列表
            pass
    return HttpResponse(simplejson.dumps(info))

#状态详情获取
def status_detail(request):
    info = []
    if request.method == 'GET':
        #项目状态
        root_node = {}
        root_node['id'] = -1
        root_node['name'] = 'Project'
        
        status = Status.objects.filter(type = -1)
        child_node = []
        for project in status:
            p = {}
            p['id'] = project.id
            p['name'] = project.name
            p['desc'] = project.desc
            p['iconCls'] = "icon-blank"
            child_node.append(p)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        info.append(root_node)
        
        #资产状态
        root_node = {}
        root_node['id'] = -2
        root_node['name'] = 'Asset'
        
        status = Status.objects.filter(type = -2)
        child_node = []
        for asset in status:
            a = {}
            a['id'] = asset.id
            a['name'] = asset.name
            a['desc'] = asset.desc
            a['iconCls'] = "icon-blank"
            child_node.append(a)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        info.append(root_node)
        
        #任务状态
        root_node = {}
        root_node['id'] = -3
        root_node['name'] = 'Task'
        
        status = Status.objects.filter(type = -3)
        child_node = []
        for task in status:
            t = {}
            t['id'] = task.id
            t['name'] = task.name
            t['desc'] = task.desc
            t['iconCls'] = "icon-blank"
            child_node.append(t)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        
        info.append(root_node)
        
    return HttpResponse(simplejson.dumps(info))

#状态添加
def status_create(request):
    Model = Status
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

#状态修改
def status_update(request):
    info = {}
    
    Model = Status
    
    info = {}
    if request.method == 'POST':
        try:
            Form = modelform_factory(Model)
            pk = request.POST.get('id','')
            instance = Model.objects.get(pk=pk)
            form = Form(request.POST, instance = instance)
            form.save()
            info['success']=True
            info['message']="修改成功"
        except:
            info['success'] = False
            info['message']="修改失败"
            
        finally:
            return HttpResponse(simplejson.dumps(info))

#状态删除
def status_destroy(request):
    
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            #判断是否有外键在使用
            project = Project.objects.filter(status = id)
            taskgroup = TaskGroup.objects.filter(status = id)
            task = Task.objects.filter(status = id)
            if project or taskgroup or task:
                info['success']=False
                info['errors'] = '此状态在项目,任务,资产中被使用'
                return HttpResponse(simplejson.dumps(info))
            p = Status.objects.get(id=id)
            p.delete()
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

#类型search,list
def types_read(request,index):
    info = []
    if request.method == 'GET':      
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所有
                types = Types.objects.all()
                for t in types:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
            
            elif index == 1:
                #0获取所有项目类型
                types = Types.objects.filter(type = -1)
                for t in types:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
            elif index == 2:
                #0获取所有资产类型
                types = Types.objects.filter(type = -2)
                for t in types:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
            elif index == 3:
                #0获取所有任务类型
                types = Types.objects.filter(type = -3)
                for t in types:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
                    
        else:
            #获取整个列表
            pass
    return HttpResponse(simplejson.dumps(info))

#类型详情获取
def types_detail(request):
    info = []
    if request.method == 'GET':
        #项目类型
        root_node = {}
        root_node['id'] = -1
        root_node['name'] = 'Project'
        
        types = Types.objects.filter(type = -1)
        child_node = []
        for project in types:
            p = {}
            p['id'] = project.id
            p['name'] = project.name
            p['desc'] = project.desc
            p['iconCls'] = "icon-blank"
            child_node.append(p)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        info.append(root_node)
        
        #资产类型
        root_node = {}
        root_node['id'] = -2
        root_node['name'] = 'Asset'
        
        types = Types.objects.filter(type = -2)
        child_node = []
        for asset in types:
            a = {}
            a['id'] = asset.id
            a['name'] = asset.name
            a['desc'] = asset.desc
            a['iconCls'] = "icon-blank"
            child_node.append(a)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        info.append(root_node)
        
        #任务类型
        root_node = {}
        root_node['id'] = -3
        root_node['name'] = 'Task'
        
        types = Types.objects.filter(type = -3)
        child_node = []
        for task in types:
            t = {}
            t['id'] = task.id
            t['name'] = task.name
            t['desc'] = task.desc
            t['iconCls'] = "icon-blank"
            child_node.append(t)
        root_node['children'] = child_node
        root_node['iconCls'] = "icon-blank"
        info.append(root_node)
        
    return HttpResponse(simplejson.dumps(info))

#类型添加
def types_create(request):
    Model = Types
    
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

#类型修改
def types_update(request):
    Model = Types
    
    info = {}
    if request.method == 'POST':
        try:
            Form = modelform_factory(Model)
            pk = request.POST.get('id','')
            instance = Model.objects.get(pk=pk)
            form = Form(request.POST, instance = instance)
            form.save()
            info['success']=True
            info['message']="修改成功"
        except:
            info['success'] = False
            info['message']="修改失败"
            
        finally:
            return HttpResponse(simplejson.dumps(info))

#状态删除
def types_destroy(request):
    
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            #判断是否有外键在使用
            project = Project.objects.filter(types = id)
            taskgroup = TaskGroup.objects.filter(types = id)
            task = Task.objects.filter(types = id)
            if project or taskgroup or task:
                info['success']=False
                info['errors'] = '此类型在项目,任务,资产中被使用'
                return HttpResponse(simplejson.dumps(info))
            p = Types.objects.get(id=id)
            p.delete()
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

#组search,list
def group_read(request,index):
    info = []
    if request.method == 'GET':
        info = groupsTree1(index)
        
    return HttpResponse(simplejson.dumps(info))
    
    
    
#     info = []
#     if request.method == 'GET':      
#         if index :
#             try:
#                 index = int(index)
#             except:
#                 pass
#             if index == 0:     
#                 #0获取所有
#                 group = Groups.objects.filter(parent = 0)
#                 for g in group:
#                     i = {}
#                     i['id'] = g.id
#                     i['name'] = g.name
#                     info.append(i)
#             else:
#                 #查询或者获取一个或者多个
#                 info = groupsTree(0,index)
#         else:
#             #获取整个列表
#             info = groupsTree(0,read = True)
#     return HttpResponse(simplejson.dumps(info))

#组详情获取
def group_detail(request):   
    info = {}
    if request.method == 'GET':       
#        positions = Group.objects.all()
#        i = 0
#        l = []
#        for p in positions:
#            i += 1
#            d = {}
#            d['id'] = p.id
#            d['name'] = p.name
#            d['desc'] = p.desc
#            l.append(d)
#        info['total'] = i
#        info['rows'] = l  
        a = groupsTree(0)
    return HttpResponse(simplejson.dumps(a))

#组添加
def group_create(request):
    Model = Groups 
    info = {}
    if request.method == 'POST':
        try:
            form = modelform_factory(Model)
            new_instance = form(request.POST)
#             print new_instance.is_valid(), new_instance.errors
            new_instance.save()
            info['success']=True
            info['message']="添加成功"
        except Exception as e:
            print str(e)
            info['success'] = False
            info['message']="添加失败"
        finally:
            return HttpResponse(simplejson.dumps(info))
        
#         parent = request.POST.get('parent','')
#         name = request.POST.get('name','')
#         p_id = request.POST.get('project','')
# #        desc = request.POST.get('desc','')
#         
#         if not parent:
#             parent = 0
# 
#         print parent
#         print name
#         print p_id
# #        print desc
#         
#         if p_id:
#             project = Project.objects.get(id = p_id)
# #            Groups.objects.create(name=name,parent=parent,project=project,desc=desc,)
#             Groups.objects.create(name=name,parent=parent,project=project)
#         else:            
# #            Groups.objects.create(name=name,parent=parent,desc=desc,)
#             Groups.objects.create(name=name,parent=parent)
#         
#         info['success']=True
#     return HttpResponse(simplejson.dumps(info))

#组修改
def group_update(request):
#    if not request.user.is_superuser:
#        info['success']=False
#        info['errors'] = '你无权执行本操作'
#        return HttpResponse(simplejson.dumps(info))
    def find_children(instance):
        ls = []
        childrens = instance.children.all()
        for children in childrens:
            ls.append(children.id)
            for item in find_children(children):
                ls.append(item)
        return ls

    info = {}
    Model = Groups
    if request.method == 'POST':
        try:
            form = modelform_factory(Model)
            pk = request.POST.get('id')
            instance = Model.objects.get(id = pk)
            new_data = request.POST.copy()
            new_data['project'] = instance.project.id
            ls = find_children(instance)
            if int(new_data['parent']) in ls:
                raise Exception('父亲是自己或者儿子...')
            new_instance = form(new_data, instance = instance)
            new_instance.save() 
            info['success']=True
            info['message']="修改成功"
        except Exception as e:
            print str(e)
            info['success']=False
            info['message']="修改失败"
        finally:
            return HttpResponse(simplejson.dumps(info))
        
#         id = request.POST.get('id','')
#         name = request.POST.get('name','')
#         parent = request.POST.get('parent','')
# #        desc = request.POST.get('desc','')
#         
#         p = Groups.objects.filter(id=id)[0]
#         p.name = name
# #        p.desc = desc
#         if parent != None:
#             p.parent = parent
#         
#         p.save()
#         info['success']=True

#组删除
def group_destroy(request):
    info = {}
#    if not request.user.is_superuser:
#        info['success']=False
#        info['errors'] = '你无权执行本操作'
#        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            p = Groups.objects.get(id=id)
            
            #判断是否有外键在使用
            task_group = TaskGroup.objects.filter(group = p, is_active=True)
            sub_group = Groups.objects.filter(parent=p)
            if task_group or sub_group:
                info['success']=False
                info['errors'] = '此资产组包含资产，无法删除'
                return HttpResponse(simplejson.dumps(info))
            
            p.delete()
            info['success']=True
    return HttpResponse(simplejson.dumps(info))

#模板search,list
def templ_read(request,index):
    info = []
    if request.method == 'GET':      
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所有父模板
                templ = Templ.objects.filter(parent = 0)
                for t in templ:
                    i = {}
                    i['id'] = t.id
                    i['name'] = t.name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                print index
                pass
        else:
            #获取整个列表
            pass
    return HttpResponse(simplejson.dumps(info))

#模板详情获取
def templ_detail(request):
    info = []
    if request.method == 'GET':      
        p_templ = Templ.objects.filter(parent = 0)
        for p in p_templ:
            i = {}
            i['id'] = p.id
            i['name'] = p.name
            i['desc'] = p.desc
            i['iconCls'] = "icon-blank"
            templ = Templ.objects.filter(parent = p.id)
            j = []
            if templ:
                for t in templ:
                    k = {}
                    k['id'] = t.id
                    k['name'] = t.name
                    k['desc'] = t.desc
                    k['iconCls'] = "icon-blank"
                    j.append(k)
            i['children'] = j
#            i['state'] = "closed"
            info.append(i) 
    return HttpResponse(simplejson.dumps(info))

#模板添加
def templ_create(request):
    Model = Templ
    
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['message'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
        
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
    
#    info = {}
#    if not request.user.is_superuser:
#        info['success']=False
#        info['errors'] = '你无权执行本操作'
#        return HttpResponse(simplejson.dumps(info))
#    if request.method == 'POST':
#        parent = request.POST.get('parent','')
#        name = request.POST.get('name','')
#        desc = request.POST.get('desc','')
#        
#        if parent == '' or parent == None:
#            parent = 0
#        
#        Templ.objects.create(name=name, parent = parent, desc = desc)
#        info['success']=True
#            
#    return HttpResponse(simplejson.dumps(info))

#模板修改
def templ_update(request):      
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    
    Model = Templ
    
    if request.method == 'POST':
        try:
            Form = modelform_factory(Model)
            pk = request.POST.get('id','')
            instance = Model.objects.get(pk=pk)
            form = Form(request.POST, instance = instance)
            form.save()
            info['success']=True
            info['message']="修改成功"
        except:
            info['success'] = False
            info['message']="修改失败"
            
        finally:
            return HttpResponse(simplejson.dumps(info))
    
    
#    if request.method == 'POST':
#        id = request.POST.get('id','')
#        parent = request.POST.get('parent','')
#        name = request.POST.get('name','')
#        desc = request.POST.get('desc','')
#        
#        if id:
#            p = Templ.objects.filter(id=id)[0]
#            if parent:
#                p.parent = int(parent)
#            p.name = str(name)
#            p.desc = str(desc)
#            p.save()
#            info['success']=True
#    return HttpResponse(simplejson.dumps(info))

#模板删除
def templ_destroy(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            p = Templ.objects.filter(id=id)[0]
            p.delete()
            
            #删除下属所有子模板
            nodes = Templ.objects.filter(parent = id)
            for t in nodes:
                t.delete()
        
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

#项目search,list
def project_read(request,index):
    info = []
    if request.method == 'GET':      
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所以父节点  
                pass
            else:
                #查询或者获取一个或者多个
                print index
                pass
        else:
            #获取整个列表
            projects = Project.objects.filter(is_active=True)
            for p in projects:
                i = {}
                i['id'] = p.id
                i['name'] = p.name
                info.append(i) 
    return HttpResponse(simplejson.dumps(info))

#项目详情获取
def project_detail(request):
    
    info = {}
    if request.method == 'GET':       
        projects = Project.objects.filter(is_active=True)
        i = 0
        l = []
        for p in projects:
            i += 1
            d = {}
            d['id'] = p.id
            d['name'] = p.name
            d['types'] = p.types.name
            d['types_id'] = p.types.id
            d['status'] = p.status.name
            d['status_id'] = p.status.id
            d['user'] = p.user.first_name
            d['user_id'] = p.user.id
            if p.creat_time != None:
                d['creat_time'] = timezone.localtime(p.creat_time).strftime('%Y-%m-%d') 
            else:
                d['creat_time'] = ''
            
            if p.start_time != None:
                d['start_time'] = timezone.localtime(p.start_time).strftime('%Y-%m-%d') 
            else:
                d['start_time'] = ''
                
            if p.end_time != None:
                d['end_time'] = timezone.localtime(p.end_time).strftime('%Y-%m-%d') 
            else:
                d['end_time'] = ''
            
            d['desc'] = p.desc
            d['priority'] = p.priority
            l.append(d)
        info['total'] = i
        info['rows'] = l
    return HttpResponse(simplejson.dumps(info))

#项目添加
def project_create(request):
    info = {}
    
    if not request.user.is_superuser:
        info['success']=False
        info['message'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))

#    Model = Project
#    if request.method == 'POST':
#        try:
#            form = modelform_factory(Model)
#            f = form(request.POST)
#            f.status=Status.objects.get(id=request.POST.get('status',''))
#            f.types=Types.objects.get(id=request.POST.get('types',''))
#            f.user=User.objects.get(id=request.POST.get('user',''))
#            f.creat_time= datetime.datetime.now().strftime('%Y-%m-%d')
#            f.save()
#            info['message']="添加成功"
#            info['success']=True
#        except:
#            info['message']="添加失败，请输入正确字段"
#            info['success'] = False
#        finally:
#            return HttpResponse(simplejson.dumps(info))
    
    if request.method == 'POST':
        name = request.POST.get('name','')
        status = request.POST.get('status','')
        type = request.POST.get('types','')
        user = request.POST.get('user','')
        start_time = request.POST.get('start_time','')
        end_time = request.POST.get('end_time','')
        desc = request.POST.get('desc','')
        
        if status and type and user and start_time and end_time:
            if dateCompare(start_time, end_time):
                create_time = datetime.datetime.now().strftime('%Y-%m-%d')
                Project.objects.create(name=name, status=Status.objects.get(id=status), types=Types.objects.get(id=type), user=User.objects.get(id=user),
                                        creat_time=create_time, start_time=start_time, end_time = end_time, desc = desc)        
            
                info['success']=True
                info['message']='添加成功'
            else:
                info['success']=False
                info['message']='开始时间必须小于结束时间'
        else:
            info['success']=False
            info['message']='创建项目失败'
            
    return HttpResponse(simplejson.dumps(info))

#项目修改
def project_update(request):      
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    
#    Model = Project
#    
#    if request.method == 'POST':
#        try:
#            Form = modelform_factory(Model)
#            pk = request.POST.get('id','')[1:]
#            instance = Model.objects.get(pk=pk)
#            form = Form(request.POST, instance = instance)
#            form.save()
#            info['success']=True
#        except:
#            info['success'] = False
#            
#        finally:
#            return HttpResponse(simplejson.dumps(info))
    
    if request.method == 'POST':
        id = request.POST.get('id','')
        name = request.POST.get('name','')
        status = request.POST.get('status','')
        types = request.POST.get('types','')
        user = request.POST.get('user','')
        start_time = request.POST.get('start_time','')
        end_time = request.POST.get('end_time','')
        desc = request.POST.get('desc','')
        
        if id:
            p = Project.objects.filter(id=int(id[1:]))[0]
            
            p.name = str(name)
            p.status=Status.objects.get(id=int(status))
            p.types=Types.objects.get(id=int(types))
            p.user=User.objects.get(id=int(user))
            p.start_time = start_time
            p.end_time = end_time
            p.desc = desc
            
            p.save()
            info['success']=True
    return HttpResponse(simplejson.dumps(info))

#项目删除
def project_destroy(request):
    info = {}
    
    if request.method == 'POST':
        id = request.POST.get('id','')
        
        if id:
            p = Project.objects.filter(id=id[1:])[0]
            p.is_active = False
            p.save()       
            tgs = TaskGroup.objects.filter(project=p,is_active=True)
            for tg in tgs:
                tg.is_active = False
                tg.save()  
            ts = Task.objects.filter(project=p,is_active=True)
            for t in ts:
                t.is_active = False
                t.save()  
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

#项目缩略图
def project_img(request):
    info = {}
    if request.method == 'POST':
        file = request.FILES.get('projectImage', None)
        id = request.POST.get('id', None)  
        if  file and id:
            p = Project.objects.filter(id=id)[0]
            file_content = ContentFile(file.read())
            if p.thum:
                try:
                    os.remove(p.thum.path)
                except OSError:
                    pass
            p.thum.save(str(uuid.uuid1())+os.path.splitext(file.name)[1], file_content)
        info['path'] = p.thum.url
        info['sucess']=True
    return HttpResponse(simplejson.dumps(info))
#资产search,list
def taskGroup_read(request,index):
    info = []
    if request.method == 'POST': 
        projectId = request.POST.get('projectId','')     
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所以父节点  
                pass
            else:
                #查询或者获取一个或者多个
                print index
                pass
        else:
            #获取整个列表
            taskGroups = TaskGroup.objects.filter(project__id__exact = projectId,is_active=True)
            for tg in taskGroups:
                i = {}
                i['id'] = tg.id
                i['text'] = tg.name
                info.append(i)    
    return HttpResponse(simplejson.dumps(info))
        

#资产详情获取
def taskGroup_detail(request):
    info = []
    if request.method == 'POST':
        id = request.POST.get('id','')
        projectId = request.POST.get('projectId','')
        if id: 
            try:
                g_id = -int(id)
            except:
                g_id = ''
            if g_id:
                taskGroup = TaskGroup.objects.filter(group__id__exact = g_id,is_active=True)
                for t in taskGroup:
                    k = {}
                    k['id'] = t.id
                    k['name'] = t.name
                    k['namedesc'] = t.namedesc
                    if t.types:
                        k['type'] = t.types.name
                    if t.status:
                        k['status'] = t.status.name
                    if t.templ:
                        k['templ'] = t.templ.name
                    else:
                        k['templ'] = ''
                    if t.thum:
                        k['img'] = t.thum.url
                    else:
                        k['img'] = ''
                    k['desc'] = t.desc
                    info.append(k)
            else:
                g_id = int(id[1:])
                group = Groups.objects.filter(parent = g_id)
                for g in group:
                    i = {}
                    try:
                        gps = Groups.objects.filter(parent = g.id)                        
                    except:
                        gps = ''
                    if gps:
                        i['id'] = 'g'+str(g.id) 
                    else:
                        i['id'] = -g.id
                    i['name'] = g.name 
                    i['children'] = ''
                    i['state'] = "closed"
                    info.append(i)
        else:
            group = Groups.objects.filter(project__id__exact = int(projectId))
            for g in group:
                i = {}
                try:
                    gs = Groups.objects.filter(parent = g.id)                        
                except:
                    gs = ''
                if gs:
                    i['id'] = 'g'+str(g.id) 
                else:
                    i['id'] = -g.id           
                i['name'] = g.name 
                i['children'] = ''
                i['state'] = "closed"
                info.append(i)
    return HttpResponse(simplejson.dumps(info))

#资产详情添加
def taskGroup_create(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        try:
            name = request.POST.get('name','')
            namedesc = request.POST.get('namedesc', '')
            type = request.POST.get('type','')
            status = request.POST.get('status','')
            templ = request.POST.get('templ','')
            group = request.POST.get('group','')
            desc = request.POST.get('desc','')
            project = request.POST.get('project','')
            if name and type and status and group:
                if templ:
                    taskGroup = TaskGroup.objects.create(
                                                      name=name,
                                                      namedesc = namedesc,
                                                      types=Types.objects.get(id=int(type)),
                                                      status=Status.objects.get(id=int(status)),
                                                      group=Groups.objects.get(id=int(group)),
                                                      templ=Templ.objects.get(id = templ),
                                                      project=Project.objects.get(id=int(project)),
                                                      desc=desc
                                                      )
                    t = Templ.objects.filter(parent= templ)                
                    for i in t:
                        Task.objects.create(name = i.name,task_group = taskGroup,project=Project.objects.get(id=int(project)))
                else:
                    taskGroup = TaskGroup.objects.create(
                                                      name=name,
                                                      namedesc = namedesc,
                                                      types=Types.objects.get(id=int(type)),
                                                      status=Status.objects.get(id=int(status)),
                                                      group=Groups.objects.get(id=int(group)),
                                                      project=Project.objects.get(id=int(project)),
                                                      desc=desc
                                                      )
                info['success']=True
                info['message']='添加成功'
            else:
                info['success']=False
                info['message']='添加失败'
        except:
            info['success']=False
            info['message']='添加失败'
        finally:
            return HttpResponse(simplejson.dumps(info))

#资产详情修改
def taskGroup_update(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        name = request.POST.get('name','')
        namedesc = request.POST.get('namedesc', '')
        type = request.POST.get('type','')
        status = request.POST.get('status','')
        templ = request.POST.get('templ','')
        group = request.POST.get('group','')
        desc = request.POST.get('desc','')
        project = request.POST.get('project','')
        
        if id:
            p = TaskGroup.objects.filter(id=id)[0]
            if name:
                try:
                    p.name = str(name)
                except:
                    pass
            else:
                info['success']=False
                info['errors']= '修改失败'
                return HttpResponse(simplejson.dumps(info))
                
            if type:
                try:
                    p.types = Types.objects.get(id=int(type))
                except:
                    pass
            if status:
                try:
                    p.status = Status.objects.get(id=int(status))
                except:
                    pass
            if templ:
                try:
                    p.templ = Templ.objects.get(id=int(templ))
                except:
                    pass
#            p.group = Group.objects.get(id=int(group))
#            p.project = Project.objects.get(id=int(project))
            p.namedesc = str(namedesc)
            p.desc = str(desc)
            p.save()
            info['success']=True
            info['errors']= '修改成功'
    return HttpResponse(simplejson.dumps(info))

#资产详情删除
def taskGroup_destroy(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            p = TaskGroup.objects.filter(id=id)[0]
            p.is_active = False
            p.save()        
            ts = Task.objects.filter(task_group=p,is_active=True)
            for t in ts:
                t.is_active = False
                t.save()  
        info['success']=True
    return HttpResponse(simplejson.dumps(info))

#资产图片
def taskGroup_img(request):  
    info = {}
    if request.method == 'POST':
        file = request.FILES.get('groupImage', None)
        id = request.POST.get('id', None)  
        if  file and id:
            tg = TaskGroup.objects.filter(id=id)[0]
            file_content = ContentFile(file.read())
            if tg.thum:
                os.remove(tg.thum.path)
            tg.thum.save(str(uuid.uuid1())+os.path.splitext(file.name)[1], file_content)           
        info['sucess']=True
    return HttpResponse(simplejson.dumps(info))

#资产树形结构
def taskGroup_tree(request, index):  
    info = []
    if request.method == 'GET':
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所有
                group = Groups.objects.filter(parent = 0)
                for g in group:
                    i = {}
                    i['id'] = g.id
                    i['name'] = g.name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                info = taskgroupTree(0,index)
        else:
            #获取整个列表
            info = taskgroupTree(0,read = True)
    return HttpResponse(simplejson.dumps(info))

#可被关联的资产树形结构
def taskGroup_tree_relateable(request, proj, src_tg):  
    info = []
    if request.method == 'GET':
        print src_tg
        #查询已关联的taskGroup
        src_id = src_tg.split('_')[1]
        except_list = []
        taskGroupRel = TaskGroupRel.objects.filter(src_id = src_id)
        
        #添加已关联
        for tgr in taskGroupRel:
            except_list.append('tg_' + str(tgr.desc.id))
        
        #添加自身
        except_list.append(src_tg)
        
        
        print except_list
        
        if proj :          
            try:
                proj = int(proj)
            except:
                pass
            if proj == 0:     
                #0获取所有
                group = Groups.objects.filter(parent = 0)
                for g in group:
                    i = {}
                    i['id'] = g.id
                    i['name'] = g.name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                info = taskgroupTreeRelateable(0,proj, except_list = except_list)
        else:
            #获取整个列表
            info = taskgroupTreeRelateable(0,read = True, except_list = except_list)
        
        
        print info
#        remove_from_tree(info, taskGroupRelArray)
        
    return HttpResponse(simplejson.dumps(info))


#项目人员search,list
def projectPeople_read(request,index):
    info = []
    if request.method == 'POST': 
        p_id = request.POST.get('projectId','')     
        if index :          
            try:
                index = int(index)
            except:
                pass
            if index == 0:     
                #0获取所以父节点  
                pass
            else:
                #查询或者获取一个或者多个
                print index
                pass
        else:
            #获取整个列表
            pp = ProjectPeople.objects.get(project__id__exact = p_id)
            for p in pp.users.all():
                i = {}
                i['id'] = p.id
                i['name'] = p.first_name
                info.append(i)
    return HttpResponse(simplejson.dumps(info))

#项目人员详情获取
def projectPeople_detail(request):
    info = {}
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')     
        try:
            projectPeople = ProjectPeople.objects.filter(project__id__exact = p_id)[0] 
        except:
            projectPeople = ''     
        if projectPeople:
            i = 0
            l = []
            for user in projectPeople.users.all():
                try:
                    profile = UserProfile.objects.get(user = user)
                except:
                    profile = ''
                i += 1
                k = {}
                k['id'] = user.id
                k['user'] = user.username
                k['name'] = user.first_name           
                k['email'] = user.email
                if profile:
                    k['sex'] = profile.sex
                    k['phone'] = profile.phone
                    if profile.thum:
                        k['img'] = profile.thum.url
                    else:
                        k['img'] = ''
                try:
                    pdepo = ProjectDePo.objects.filter(project__id__exact = p_id,user=user)[0]
                except:
                    pdepo = ''
                if pdepo:
                    if pdepo.department:
                        k['department'] = pdepo.department.name
                    if pdepo.position:
                        k['position'] = pdepo.position.name
                l.append(k)
            info['total'] = i
            info['rows'] = l
        else:
            info['total'] = 0
            info['rows'] = []
    return HttpResponse(simplejson.dumps(info))

#项目人员添加
def projectPeople_create(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')
        id = request.POST.getlist('id[]','')
        if p_id and id:
            p = Project.objects.get(id = p_id)
            try:
                pp = ProjectPeople.objects.get(project = p)
            except:
                pp = ProjectPeople()                         
                pp.project = p        
                pp.save()           
            for i in id:
                u = User.objects.get(id = i)
                pp.users.add(u)
            info['success'] = True
        else:
            info['success'] = True
    return HttpResponse(simplejson.dumps(info))

#项目人员修改
def projectPeople_update(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        pid = request.POST.get('pid','')
        did = request.POST.get('department','')
        poid = request.POST.get('position[]','')
        if id and pid: 
            p = Project.objects.filter(id=int(pid))[0] 
            u = User.objects.filter(id=int(id))[0]   
            if did:
                try:
                    d = Department.objects.filter(id=int(did))[0]   
                except:
                    d = ''
            if poid:
                try:
                    po = Position.objects.filter(id=int(poid))[0]   
                except:
                    po = '' 
            try:
                pdp = ProjectDePo.objects.filter(project=p,user=u)[0] 
            except:
                pdp = ''
            if pdp:
                if d and po:
                    pdp.department = d
                    pdp.position = po
                    pdp.save()
                elif d:
                    pdp.department = d
                    pdp.save()
                elif po:
                    pdp.position = po
                    pdp.save()
            else: 
                if d and po:
                    ProjectDePo.objects.create(project=p,user=u,department=d,position=po)
                elif d:
                    ProjectDePo.objects.create(project=p,user=u,department=d)
                elif po:
                    ProjectDePo.objects.create(project=p,user=u,position=po)
                else:              
                    ProjectDePo.objects.create(project=p,user=u)
            info['success'] = True 
    return HttpResponse(simplejson.dumps(info))

#项目人员删除
def projectPeople_destroy(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')
        id = request.POST.getlist('id[]','')
        if p_id and id:
            try:
                pp = ProjectPeople.objects.get(project__id__exact = p_id)
            except:
                pp = None
            if pp:
                for i in id:
                    u = User.objects.get(id = i)
                    pp.users.remove(u)
        info['success'] = True 
    return HttpResponse(simplejson.dumps(info))

#项目任务search,list
def projectTask_read(request):
    pass

#项目任务详情获取
@gzip_page
def projectTask_detail(request):
    info = []
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')     
        tasks = Task.objects.filter(project__id__exact=p_id,is_active=True)
        if tasks:           
            for t in tasks:               
                k = {}
                k['id'] = t.id
                k['group'] = t.task_group.group.id
                k['taskGroup'] = t.task_group.name
                k['name'] = t.name
                if t.status:
                    k['status'] = t.status.name 
                if t.types:         
                    k['type'] = t.types.name
                if t.user:
                    users = ''
                    for u in t.user.all():
                        if users:
                            users += ','
                        users += u.first_name                       
                    k['user'] = users
                if t.start_time:
                    k['startTime'] = timezone.localtime(t.start_time).strftime('%Y-%m-%d')
                if t.end_time:
                    k['endTime'] = timezone.localtime(t.end_time).strftime('%Y-%m-%d')
                if t.finish_time:
                    k['finishTime'] = timezone.localtime(t.finish_time).strftime('%Y-%m-%d')
                k['desc'] = t.desc
                if t.use_time:
                    k['useTime'] = str(t.use_time)
                if t.percent:
                    k['percent'] = t.percent
                else:
                    k['percent'] = 0
                
                if t.version:
                    k['version'] = t.version
                else:
                    k['version'] = ''
                k['qc'] =t.qc()
                k['reviewStatus'] = t.r_status()
                k['publishStatus'] = t.p_status() 
                try:
                    ti = TaskImg.objects.filter(task=t)[0]
                except:
                    ti = ''
                if ti:
                    k['thum'] = ti.thum.url                   
                info.append(k)
                info = sorted(info,key = lambda x:x['group'])
    return HttpResponse(simplejson.dumps(info))

#项目任务添加
def projectTask_create(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['message'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        try:
            p_id = request.POST.get('projectId','')
            tg = request.POST.get('taskGroup','')
            name = request.POST.get('name','')
            desc = request.POST.get('desc','')
            if tg and name:
                taskGroup = TaskGroup.objects.get(id = tg)
                Task.objects.create(name = name,desc = desc,task_group = taskGroup,project=Project.objects.get(id=p_id))
                info['success'] = True
                info['message'] = '添加成功'
            else:
                info['success'] = False
                info['message'] = '添加失败'
        except:
            info['success'] = False
            info['message'] = '添加失败'
        finally:
            return HttpResponse(simplejson.dumps(info))

#项目任务修改
def projectTask_update(request):
    info = {}
    if request.method == 'POST':
        type = request.POST.get('type','')      
        id = request.POST.get('id','')
        if type:
            task = Task.objects.get(id = id)
            
            if type == 'qc':
                if task.user.all():
                    user = task.user.all()[0]
                    username = user.username
                else:
                    username = ''
                if not request.user.username==username:
                    info['errors'] = '你无权执行本操作'
                else:
                    qc = request.POST.get('qc','')
                    if qc=='true':
                        task.qc_flag = 1
                    else:
                        task.qc_flag = 0
                    task.save()
                    info['success'] = True
            elif type == 'review':
                if not request.user.is_superuser:
                    info['errors'] = '你无权执行本操作'
                else:
                    review = request.POST.get('review','')
                    if review:
                        task.review_status = review                        
                        task.save()
                        info['success'] = True
            return HttpResponse(simplejson.dumps(info))       
        if not request.user.is_superuser:
            info['success']=False
            info['errors'] = '你无权执行本操作'
            return HttpResponse(simplejson.dumps(info))
        name = request.POST.get('name','')
        status = request.POST.get('status','')
        user = request.POST.getlist('user[]','')
        startTime = request.POST.get('startTime','')
        endTime = request.POST.get('endTime','')
        finishTime = request.POST.get('finishTime','')
        useTime = request.POST.get('useTime','')
        desc = request.POST.get('desc','')
        percent = request.POST.get('percent','')
        if id:
            task = Task.objects.get(id = id)
            if name:
                task.name = name
            if status:
                try:
                    s = Status.objects.get(id = status)
                    task.status = s
                except:
                    pass
            if user:
                try:
                    pass
                except:
                    pass
                us = []
                for u in user:
                    if u:       
                        try:
                            ur = User.objects.get(id = u) 
                            us.append(ur)                         
                        except:
                            print u
                if us:            
                    task.user.clear()
                    for uu in us:
                        task.user.add(uu)
            if startTime:
                task.start_time = startTime
            if endTime:
                task.end_time = endTime
            if finishTime:
                task.finish_time = finishTime
            task.desc = desc
            task.percent = int(percent)
            task.use_time = str(useTime)
            task.save()
            info['success'] = True
    return HttpResponse(simplejson.dumps(info))

#项目任务删除
def projectTask_destroy(request):
    info = {}
    if not request.user.is_superuser:
        info['success']=False
        info['errors'] = '你无权执行本操作'
        return HttpResponse(simplejson.dumps(info))
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id:
            t = Task.objects.get(id = id)
            t.is_active = False
            t.save()
            info['success'] = True 
    return HttpResponse(simplejson.dumps(info)) 

#项目任务图片
def projectTask_img(request):
    info = {}
    if request.method == 'POST':
        file = request.FILES.get('mytaskImage', '')
        id = request.POST.get('id', '')       
        if  file and id:
            t = Task.objects.filter(id=id)[0]
            if t.user.all():
                user = t.user.all()[0]
                username = user.username
            else:
                username = ''
                
#            if not request.user.username==username:
#                info['errors'] = '你无权执行本操作'
#            else:
            file_content = ContentFile(file.read())
            try:
                ti = TaskImg.objects.filter(task=t)[0]
            except:
                ti = TaskImg.objects.create(task=t,version=t.version)
            if ti.thum:
                os.remove(ti.thum.path)
            ti.thum.save(str(uuid.uuid1())+os.path.splitext(file.name)[1], file_content)           
            info['sucess'] = True
        else:
            info['errors'] = '上传失败'
    return HttpResponse(simplejson.dumps(info))

#提交文件上传
def issueFileUpload(request):
    print 'issueFileUpload'
    info = {}
    if request.method == 'POST':
        
        name = request.POST.get('Filename', '')
        #projectId = request.POST.get('projectId', '')
        taskId = request.POST.get('taskId', '')
        sessionId = request.POST.get('sessionId', '')
        file = request.FILES.get('Filedata', '')
        
#        print projectId
        print taskId
        print sessionId
        
        path = MEDIA_ROOT + '/' + sessionId
        print path
        
        if os.path.isdir(path) == False:
            os.mkdir(path)
        
        try:
            
            fp = open(path+'/'+name, 'wb')
            for content in file.chunks():   
                fp.write(content)
            fp.close()
            
            return HttpResponse('1')
        except:
            return HttpResponse('2')

#提交权限判定 只能提交用户自己的任务
def issue_authorized(request):
    print 'issue_authorized'
    info = {}
    if request.method == 'POST':
        taskId = request.POST.get('taskId', '')
        task = Task.objects.get(id = taskId)
        
        if task.user.all():
            user = task.user.all()[0]
            username = user.username
            if request.user.username == username:
                info['success'] = True
            else:
                info['success'] = False
        else:
            info['success'] = False
            
        
    return HttpResponse(simplejson.dumps(info))
    
#项目任务提交
def projectTask_issue(request):
    
    print 'projectTask_issue     '
    info = {}
    if request.method == 'POST':
        #projectId = request.POST.get('projectId','')
        taskId = request.POST.get('taskId','')
        sessionId = request.POST.get('sessionId','')
        fileCount = int(request.POST.get('fileCount',''))
        
#        print projectId
        print taskId
        print sessionId
#        project = Project.objects.get(id=projectId)
        task = Task.objects.get(id=taskId)
        taskgroup = task.task_group
        filename = ''
        dirname = ''
        
        #版本号+1
        version = 0
        if task.version != None:
            version = int(task.version)
        
        version += 1
        
        if version < 10:
            version = '00' + str(version)
        elif version < 100:
            version = '0' + str(version)
        else:
            version = str(version)
        
        #存储路径
        src = MEDIA_ROOT + '/' + sessionId
        desc = globalvar.PROJECTDIR
        
        #资产分类
        print 'fileCount     ', fileCount
        
        #texture
        if task.name == 'texture':
            try:
                desc = cascadeCreateDir(desc, [task.project.name, 'Texture'])    
                
                for line in os.listdir(src):
                    shutil.copy(src+'/'+line, desc)
                info['success'] = True
            except:
                print traceback.print_exc()
                info['success'] = False
        #shot
        elif taskgroup.types == Types.objects.get(name='shot'):
            
            if fileCount == 1:
                #单文件
                try:
                    desc = cascadeCreateDir(desc, [task.project.name, 'shot'])    
                    for line in os.listdir(src):
                        shutil.copy(src+'/'+line, desc)
                        filename = generateNewFileName(line, [taskgroup.name, task.name, 'v'+version], '_')
                        os.rename(desc+'/'+line, desc+'/'+filename)
                except:
                    print traceback.print_exc()
                    info['success'] = False
            else:
                #多文件
                try:
                    dirname = taskgroup.name + '_' + task.name + '_' + 'v'+version
                    desc = cascadeCreateDir(desc, [task.project.name, 'shot', dirname])    
                    
                    for line in os.listdir(src):
                        shutil.copy(src+'/'+line, desc)
                except:
                    print traceback.print_exc()
                    info['success'] = False
            info['success'] = True
        #asset
        else:
            filelist = os.listdir(src)
            if findSameExt(filelist) == True:
                #有重复文件
                info['success'] = False
                info['msg'] = "上传文件类型不允许相同."
                
            else:
                desc = cascadeCreateDir(desc, [task.project.name, 'Asset', taskgroup.name])
                for line in os.listdir(src):
                    shutil.copy(src+'/'+line, desc)
                    filename = generateNewFileName(line, [taskgroup.name, task.name, 'v'+version], '_')
                    os.rename((desc+'/'+line).encode('utf-8'), (desc+'/'+filename).encode('utf-8'))
                info['success'] = True

        if info['success'] == True:
            #数据库修改
            task.version = version
            task.publish_status = 1
            task.review_status = 1
            task.save()
            
        
        #删除临时文件
        shutil.rmtree(src)
        
    return HttpResponse(simplejson.dumps(info))

#项目任务延时加载 资产列表
def projectTaskDl_taskgroup(request):
    info = []
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')
        taskGroup = TaskGroup.objects.filter(project__id__exact=p_id, is_active=1)
        for t in taskGroup:
            i = {}
            i['id'] = t.id
            i['name'] = t.name
            info.append(i)

    return HttpResponse(simplejson.dumps(info))

#项目任务延时加载 任务列表
def projectTaskDl_detail(request):
    info = []
    if request.method == 'POST':
        g_id = request.POST.get('taskgroupId','')
        taskGroup = Task.objects.filter(task_group__id__exact=g_id,is_active=True)
        for t in taskGroup:
            k = {}
            k['id'] = t.id
            k['group'] = t.task_group.group.id
            k['taskGroup'] = t.task_group.name
            k['taskGroupId'] = t.task_group.id
            k['name'] = t.name
            if t.status:
                k['status'] = t.status.name 
                k['statusId'] = t.status.id
                
            if t.types:         
                k['type'] = t.types.name
            if t.user:
                users = ''
                userId = ''
                for u in t.user.all():
                    if users:
                        users += ','
                    users += u.first_name
                    userId = u.id

                k['user'] = users
                k['userId'] = userId
            if t.start_time:
                k['startTime'] = timezone.localtime(t.start_time).strftime('%Y-%m-%d')
            if t.end_time:
                k['endTime'] = timezone.localtime(t.end_time).strftime('%Y-%m-%d')
            k['desc'] = t.desc
            if t.use_time:
                k['useTime'] = str(t.use_time)
            if t.finish_time:
                k['finishTime'] = timezone.localtime(t.finish_time).strftime('%Y-%m-%d')
            if t.percent:
                k['percent'] = t.percent
            else:
                k['percent'] = 0
            
            if t.version:
                k['version'] = t.version
            else:
                k['version'] = ''
            k['qc'] =t.qc()
            k['reviewStatus'] = t.r_status()
            k['publishStatus'] = t.p_status() 
            try:
                ti = TaskImg.objects.filter(task=t)[0]
            except:
                ti = ''
            if ti:
                k['thum'] = ti.thum.url                   
                
            #统计任务的评论数
            noteCount = 0
            try:
                noteCount = Note.objects.filter(task=t).count()
            finally:
                k['noteCount'] = noteCount
            info.append(k)
            info = sorted(info,key = lambda x:x['group'])

    return HttpResponse(simplejson.dumps(info))


#主页项目详细显示
def index_project(request):
    info = []
    if request.method == 'POST':
        id = request.POST.get('id','')
        if id: 
            t = id[:1]
            if t == 'a':
                groups = Groups.objects.filter(project = id[1:])
                for g in groups:
                    i = {}
                    i['id'] = 'b'+id[1:]+'o'+str(g.id)
                    i['name'] = g.name 
                    i['children'] = ''
                    i['state'] = "closed"
                    i['iconCls'] = "icon-blank"
                    info.append(i)
            elif t == 'b':
                list = id[1:]
                list = list.split('o')
                p_id = int(list[0])
                g_id = int(list[1])
                try:
                    groups = Groups.objects.filter(parent = g_id)
                except:
                    groups = ''
                if groups:
                    for group in groups:
                        i = {}
                        i['id'] = 'b'+list[0]+'o'+str(group.id)
                        i['name'] = group.name 
                        i['children'] = ''
                        i['state'] = "closed"
                        i['iconCls'] = "icon-blank"
                        info.append(i)
                else:
                    tgs = TaskGroup.objects.filter(project__id__exact = p_id,group__id__exact = g_id,is_active=True)
                    for tg in tgs:
                        i = {}
                        i['id'] = 'c'+list[0]+'o'+str(tg.id)
                        i['name'] = tg.name 
                        if tg.status:
                            i['status'] = tg.status.name
                        else:
                            i['status'] = ''
                        i['desc'] = tg.desc
                        i['children'] = ''
                        i['state'] = "closed"
                        i['iconCls'] = "icon-blank"
                        info.append(i)
            elif t == 'c':
                list = id[1:]
                list = list.split('o')
                p_id = int(list[0])
                tg_id = int(list[1])
                tasks = Task.objects.filter(project__id__exact=p_id,task_group__id__exact=tg_id,is_active=True)
                for tk in tasks:
                    i = {}
                    i['id'] = 'd'+list[0]+'o'+str(tk.id)
                    i['name'] = tk.name 
                    if tk.status:
                        i['status'] = tk.status.name
                    if tk.user:
                        nu = 0
                        names = ''
                        for u in tk.user.all():
                            nu += 1
                            names += u.first_name
                            if nu > 1:
                                names += '|'
                        i['user'] = names
                    if tk.start_time:
                        i['startTime'] = timezone.localtime(tk.start_time).strftime('%Y-%m-%d')
                    if tk.end_time:
                        i['endTime'] = timezone.localtime(tk.end_time).strftime('%Y-%m-%d')
                    i['desc'] = tk.desc
                    i['iconCls'] = "icon-blank"
                    info.append(i)
        else:
            projects = Project.objects.filter(is_active=True)
            for p in projects:
                i = {}
                i['id'] = 'a'+str(p.id)
                i['name'] = p.name 
                i['user'] = p.user.first_name
                i['user_id'] = p.user.id
                
                if p.status:
                    i['status'] = p.status.name
                    i['status_id'] = p.status.id
                else:
                    i['status'] = ''
                    
                if p.types:
                    i['types'] = p.types.name
                    i['types_id'] = p.types.id
                else:
                    i['types'] = ''
                    
                if p.start_time:
                    i['startTime'] = timezone.localtime(p.start_time).strftime('%Y-%m-%d')
                if p.end_time:
                    i['endTime'] = timezone.localtime(p.end_time).strftime('%Y-%m-%d')
                i['desc'] = p.desc
                i['children'] = ''
                i['state'] = "closed"
                i['iconCls'] = "icon-blank"
                info.append(i)
    return HttpResponse(simplejson.dumps(info))

#主页我的任务显示
def index_task(request):
    info = []
    if request.method == 'POST':
        u = request.user
        ps =Project.objects.filter(is_active=True).exclude(status_id=5)
        for p in ps:
            try:
                ts = Task.objects.filter(user=u,project=p,is_active=True)
            except:
                ts = ''
            if ts:
                k = {}
                k['id'] = 'p'+str(p.id)
                k['name'] = p.name 
                a = {}
#                 ts.query.group_by = ['task_group_id']
                for t in ts:
                    a_id = t.task_group.id
                    if not a.has_key(a_id):
                        a[a_id] = []
                b = []
                for id in a:
                    tg = TaskGroup.objects.filter(id = id)[0]
                    x = {}
                    x['id'] = 'a'+str(tg.id)
                    x['name'] = tg.name
                    try:
                        ts2 = Task.objects.filter(task_group=tg,is_active=True)
                    except:
                        ts2 = ''
                    c = []
                    if ts2:
                        for t2 in ts2:
                            j = {}                    
                            j['groupId'] = t2.task_group.id
                            j['id'] = 't'+str(t2.id)
                            j['name'] =  t2.name
                            if t2.status:
                                j['status'] = t2.status.name   
                            if t2.start_time:
                                j['startTime'] = timezone.localtime(t2.start_time).strftime('%Y-%m-%d')  
                            if t2.end_time:
                                j['endTime'] = timezone.localtime(t2.end_time).strftime('%Y-%m-%d')  
                            if t2.finish_time:
                                j['finishTime'] = timezone.localtime(t2.finish_time).strftime('%Y-%m-%d')  
                            j['desc'] = t2.desc
                            j['percent'] = t2.percent 
                            if t2.version:
                                j['version'] = t2.version
                            else:
                                j['version'] = ''
                            j['qc'] =t2.qc()
                            j['review_status'] = t2.r_status()
                            j['publishStatus'] = t2.p_status()
                            if t2.user.all():
                                user = t2.user.all()[0]
                                j['user'] = user.first_name
                                if user == u:
                                    j['dis'] = False
                                else:
                                    j['dis'] = True
                            else:
                                j['dis'] = True
                            try:
                                ti = TaskImg.objects.filter(task=t2)[0]
                            except:
                                ti = ''
                            if ti:
                                if ifMediaAvalible(ti.thum.url):
                                    j['thum'] = ti.thum.url
                            j['iconCls'] = "icon-blank"
                            c.append(j)
                    x['children'] = c
                    x['iconCls'] = "icon-blank"
                    b.append(x)
                k['children'] = b
                k['iconCls'] = "icon-blank"
                info.append(k)
    return HttpResponse(simplejson.dumps(info))

# 甘特图
@gzip_page
def get_gantt_tasks(request):
    print 'get_gantt_tasks'
    if request.method == 'GET':
        dic={}
        proj_list=[]
        
        proj_id = 0
        try:
            proj_id = int(request.GET.get('proj',''))
            print 'proj     :', proj_id
        except:
            pass
        
        #获取项目信息
        try:
            pList = []
            if proj_id == 0 or proj_id == '' or proj_id == None:
                pList = Project.objects.filter(is_active=True)
            else:
                pList.append(Project.objects.get(id=proj_id))
            
            if pList != None and len(pList) != 0:
                for project in pList:
                    p = {}
                    p['Id'] = project.id
                    p['Name'] = project.name
                    
                    #项目状态
                    p['Status'] = project.status.name
                    
                    pStartDate = None
                    pEndDate = None
                    
                    p['PercentDone'] = 0
                    
                    #获取资产信息
                    asset_list=[]
                    for task_group in TaskGroup.objects.filter(project=project,is_active=True):
                        tg = {}
                        tg['Id'] = 'tg_' + str(task_group.id)
                        tg['Name'] = task_group.name
                        
                        #资产状态
                        tg['Status'] = task_group.status.name
                        
                        aStartDate = None
                        aEndDate = None
                        
                        #获取任务信息
                        task_list=[]
                        for task in Task.objects.filter(task_group=task_group,is_active=True):
                            t = {}
                            t['Id'] = 't_' + str(task.id)
                            t['Name'] = task.name
                            
                            #任务分配
                            t['Assign'] = ''
                            if(task.user != None):
                                user = task.user.all()
                                for u in user:
                                    t['Assign'] = t['Assign'] + u.first_name + ' '
    #                            t['Assign'] = task.user
                            
                            if(task.start_time == None):
                                t['StartDate'] = ''
                            else:
                                t['StartDate'] = timezone.localtime(task.start_time).strftime('%Y-%m-%dT%H:%M:%S')
                                #资产最早开始时间计算
                                if aStartDate == None:
                                    aStartDate = task.start_time
                                else:
                                    if task.start_time < aStartDate:
                                        aStartDate = task.start_time
                            
                            if(task.end_time == None):
                                t['EndDate'] = ''
                            else:
                                t['EndDate'] = timezone.localtime(task.end_time).strftime('%Y-%m-%dT%H:%M:%S')
                            
                                #资产最晚结束时间计算
                                if aEndDate == None:
                                    aEndDate = task.end_time
                                else:
                                    if task.end_time > aEndDate:
                                        aEndDate = task.end_time
                            
                            
                            if(task.percent == None):
                                t['PercentDone'] = 0
                            else: 
                                t['PercentDone'] = task.percent
                                
                            t['expanded'] = 1
                            t['leaf'] = 1
                            
                            #审核相关
                            try:
                                taskReview = TaskReview.objects.filter(task=task).order_by('-review_time')[0]
                                
                                if taskReview != None:
                                    print taskReview.review_time
                                    
#                                    # 0 未提交
#                                    # 1 已送审
#                                    # 2 审核通过
#                                    # 3 审核未通过
#                                    if task.status == None:
#                                        t['Status'] = ''
#                                    else:
#                                        check_status = task.check_status
#                                        if check_status == 0:
#                                            #任务状态
#                                            t['Status'] = task.status.name
#                                            
#                                        if check_status == 1:
#                                            t['Status'] = '已送审'
#                                        if check_status == 2:
#                                            t['Status'] = '审核通过'
#                                        if check_status == 3:
#                                            t['Status'] = '审核未通过'
                                    
                                    if task.status == None:
                                        t['Status'] = ''
                                    else:
                                        t['Status'] = task.status.name
                                    
                                    #备注
                                    if(taskReview.remark == None):
                                        t['Remark'] = ''
                                    else:
                                        t['Remark'] = taskReview.remark
                                    
                                    #导演反馈意见
                                    if(taskReview.feedback == None):
                                        t['Feedback'] = ''
                                    else:
                                        dr = re.compile(r'<[^>]+>',re.S)
                                        
                                        t['Feedback'] = dr.sub('',taskReview.feedback)
                                
                            except:
                                t['Status'] = ''
                                t['Remark'] = ''
                                t['Feedback'] = ''
    
                            
                            task_list.append({'Task': t})
                        
                        #资产最早开始时间赋值
                        if(aStartDate == None):
                            tg['StartDate'] = ''
                        else:
                            tg['StartDate'] = timezone.localtime(aStartDate).strftime('%Y-%m-%dT%H:%M:%S')
                        
                        #资产最晚结束时间赋值
                        if(aEndDate == None):
                            tg['EndDate'] = ''
                        else:
                            tg['EndDate'] = timezone.localtime(aEndDate).strftime('%Y-%m-%dT%H:%M:%S')
                        
                        
                        tg['Tasks'] = task_list
                        tg['expanded'] = 1
                        tg['leaf'] = 0
                        
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
                            
                        asset_list.append({'Task': tg})
                    p['Tasks'] = asset_list
                    
                    #项目最早开始时间赋值
                    if(pStartDate == None):
                        p['StartDate'] = ''
                    else:
                        p['StartDate'] = timezone.localtime(pStartDate).strftime('%Y-%m-%dT%H:%M:%S')
                    
                    #项目最晚结束时间赋值
                    if(pEndDate == None):
                        p['EndDate'] = ''
                    else:
                        p['EndDate'] = timezone.localtime(pEndDate).strftime('%Y-%m-%dT%H:%M:%S')
    
    
    #                if(project.start_time == None):
    #                    p['StartDate'] = ''
    #                else:
    #                    p['StartDate'] = timezone.localtime(project.start_time).strftime('%Y-%m-%dT%H:%M:%S')
    #                
    #                if(project.end_time == None):
    #                    p['EndDate'] = ''
    #                else:
    #                    p['EndDate'] = timezone.localtime(project.end_time).strftime('%Y-%m-%dT%H:%M:%S')
                    
                    p['leaf'] = 0
                    p['expanded'] = 1
                        
                    proj_list.append({'Task': p})
        finally:    
            dic['Tasks'] =  proj_list
            dic['success'] ='true'
        
        return HttpResponse(simplejson.dumps(dic))

#甘特图项目列表
def gantt_projlist(request):
    print 'get_user_tasks_combo' 
    if request.method == 'GET':
        proj_list=[]
        
        proj_list.append({'name': '全部项目', 'id': 0})
        
        for project in Project.objects.filter(is_active=True):
            m={}
            m['id']=str(project.id)
            m['name']=project.name
            proj_list.append(m)

        return HttpResponse(simplejson.dumps(proj_list))

#审核资产列表
def notes_grouplist(request):
    info = []
    print 'notes_grouplist'
    if request.method == 'POST':
#        id = request.POST.get('id','')
        projectId = request.POST.get('projectId','')
        
        if projectId != None and projectId != '':
            taskGroup = TaskGroup.objects.filter(project=Project.objects.get(id=projectId),is_active=True)
            for tg in taskGroup:
                i = {}
                
                i['id'] = tg.id           
                i['name'] = tg.name 
                i['children'] = ''
                info.append(i)
    print info
    return HttpResponse(simplejson.dumps(info))

#审核资产列表
def notes_grouplists(request):
    info = []
    if request.method == 'POST':
        projectId = request.POST.get('projectId','')
        if projectId != None and projectId != '':
            try:
                index = int(projectId)
            except:
                pass
            if index == 0:     
                #0获取所有
                group = Groups.objects.filter(parent = 0)
                for g in group:
                    i = {}
                    i['id'] = g.id
                    i['name'] = g.name
                    info.append(i)
            else:
                #查询或者获取一个或者多个
                info = groupsTree(0,index)
        else:
            #获取整个列表
            info = groupsTree(0,read = True)
    return HttpResponse(simplejson.dumps(info))

#审核任务列表
def notes_tasklist(request):
    info = []
    print 'notes_tasklist'
    if request.method == 'POST':
#        id = request.POST.get('id','')
        id = request.POST.get('id','')
        if id != None and id != '':
            task = Task.objects.filter(task_group=TaskGroup.objects.get(id=id),is_active=True)
            for t in task:
                i = {}
                
                i['id'] = t.id           
                i['name'] = t.name 
                i['children'] = ''
                info.append(i)
    print info
    return HttpResponse(simplejson.dumps(info))

#审核任务详细信息
def notes_taskdetails(request):
    info = {}
    print 'notes_taskdetails'
    if request.method == 'POST':
#        id = request.POST.get('id','')
        id = request.POST.get('id','')
        if id != None and id != '':
            try:
                task = Task.objects.get(id=int(id))
                info['name'] = task.name
                
                if task.user != None:
#                    info['leader'] = task.user.first_name
                    info['leader'] = ''
                    for tu in task.user.all():
                        info['leader'] += tu.first_name + ' '
                else:
                    info['leader'] = ''
                
                if task.status != None:
                    info['status'] = task.status.name
                else:
                    info['status'] = ''
                
                if task.start_time != None:
                    info['startTime'] = timezone.localtime(task.start_time).strftime('%Y-%m-%d')
                else:
                    info['startTime'] = ''
                
                if task.end_time != None:
                    info['endTime'] = timezone.localtime(task.end_time).strftime('%Y-%m-%d')
                else:
                    info['endTime'] = ''
                
                info['desc'] = task.desc
                
            except:
                pass
#            print info
    
    return HttpResponse(simplejson.dumps(info))

#审核信息列表获取
def note_detail(request):
    info = []
    print 'note_detail'
    if request.method == 'POST':
#        id = request.POST.get('id','')
        task = request.POST.get('task','')
        notes = Note.objects.filter(task=task).order_by('-time')
        for n in notes:
            i = {}
            
            i['id'] = n.id
            i['content'] = n.content
            i['time'] = timezone.localtime(n.time).strftime('%Y-%m-%d %H:%M:%S') 
            i['author'] = n.user.first_name
            i['important'] = n.important
            
            info.append(i)
    print info
    return HttpResponse(simplejson.dumps(info))
    
#审核信息添加
def note_create(request):
    info = {}
    if request.method == 'POST':
        taskId = request.POST.get('task','')
        content = request.POST.get('content','')
        user = request.user
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#        print task
#        print content
#        print user.first_name
#        print date
        
        task=Task.objects.get(id=taskId)
        
        if task.project.user == user:
            Note.objects.create(user=user, time=date, content=content, task=task, important = 1)
        else:
            Note.objects.create(user=user, time=date, content=content, task=task)
        
    return HttpResponse(simplejson.dumps(info))

#编辑器图片上传
def image_upload(request):
    print 'image_upload'
    if request.method == 'POST':
        dic={}
#        print request.POST
#        print request.FILES
        fileObj = request.FILES.get('imgFile', None)
#        print fileObj
        taskId = request.POST.get('task', None)
        if fileObj != None:
            fileName = str(uuid.uuid1()) + '.jpg'
            try:
                image = Image()
                image.img.save(fileName, fileObj)
                image.save()
                
                dic['error'] = 0
                dic['url'] = '/media/Image/' + fileName
                print 'url  ', dic['url']
            except:
                dic['error'] = 1
                dic['message'] = '上传失败'
                
        
        
        return HttpResponse(simplejson.dumps(dic))


# 项目管理系统数据迁移
def data_transfer(request):
    print 'data_transfer'
    if request.method == 'GET':
        dic={}
        
        import MySQLdb
        
        conn = MySQLdb.connect(host='172.16.253.192', user='root', passwd='123123',db='CGProjManSys', charset="utf8")
        
        #Project 表 数据迁移
        count = 0
        cursor = conn.cursor()
        cursor.execute('select * from ProjMan_project where id = 73')
        
        for cp in cursor.fetchall():
            print cp
            
            projectNew = Project()
            projectNew.id = cp[0]
            projectNew.name = cp[1]
            projectNew.types = Types.objects.get(id=7)
            projectNew.status = Status.objects.get(id=int(cp[2]))
            
            #旧数据库取对应用户名
            cursor_user = conn.cursor()
            cursor_user.execute('select username from auth_user where id = ' + str(cp[3]))
            username =  cursor_user.fetchall()[0][0]
            
            try:
                userNew = User.objects.get(username = username)
                projectNew.user = userNew
            except:
                projectNew.user = User.objects.get(id=10)
            
            projectNew.desc = cp[8]
            projectNew.priority = 10
            projectNew.creat_time=cp[5]
            projectNew.start_time=cp[6]
            projectNew.end_time=cp[7]
#            thum
            projectNew.save()
        
            count += 1
        print count
        #Project 表 数据迁移
    
        #taskgroup 表 数据迁移
        cursor = conn.cursor()
        cursor.execute('select * from ProjMan_asset where project_id = 73')
        
        for ca in cursor.fetchall():
            print ca
            taskGroup = TaskGroup()
            taskGroup.id = ca[0]
            taskGroup.project = Project.objects.get(id=int(ca[1]))
            taskGroup.name = ca[3]
#            types
#            templ
            taskGroup.status = Status.objects.get(id=6)
            taskGroup.group = Group.objects.get(id=1)
            taskGroup.desc = ca[13]
#            group
#            thum
            taskGroup.save()
            
        #taskgroup 表 数据迁移
    
        #task 表 数据迁移
        count = 0
        cursor = conn.cursor()
        cursor.execute('select * from ProjMan_task_asset where project_id = 73')
            
        for ct in cursor.fetchall():
            print ct
            task = Task()
            task.id = ct[0]
            task.name = ct[1]
            task.project = Project.objects.get(id=int(ct[5]))
            task.task_group = TaskGroup.objects.get(id=int(ct[6]))
            task.priority = 10
            task.start_time = ct[8]
            task.end_time = ct[9]
            task.desc = ct[19]
            task.percent = ct[13]
            task.version = ct[14]
            task.priority = ct[15]
            
            
            task.save()
            count += 1
        print count
        
        #task 表 数据迁移
            
    return HttpResponse(simplejson.dumps(dic))

def task_test(request):
    info = {}
    
    i = 0
    while i < 300:
        
        p_id = 76
        tg = 36
        name = '测试任务-' + str(i)
        desc = request.POST.get('desc','')
        if tg and name:
            taskGroup = TaskGroup.objects.get(id = tg)
            Task.objects.create(name = name,desc = desc,task_group = taskGroup,project=Project.objects.get(id=p_id))
            print 'task ' + str(i) + 'inserted'
        
        i += 1
    
    info['success'] = True 
    
    return HttpResponse(simplejson.dumps(info))
    

#资产list
#def srcTaskGroup_read(request):   
#    info = []
#    if request.method == 'GET':      
#        g_id = request.GET.get('id','')
#        
#        taskGroup = TaskGroup.objects.filter(group_id=g_id,is_active=True)
#        
#        for tg in taskGroup:
#            i = {}
#            i['id'] = tg.id
#            i['name'] = tg.name
#            info.append(i)
#    return HttpResponse(simplejson.dumps(info))

#关联资产列表
def descTaskGroup_detail(request):   
    info = []
    if request.method == 'GET':
        type, id = request.GET.get('id','').split('_')
        
        if type == 'tg':
            taskGroupRel = TaskGroupRel.objects.filter(src_id=id)
        
            for tgr in taskGroupRel:
                try:
                    i = {}
                    desc = tgr.desc
                    i['id'] = desc.id
                    i['relId'] = tgr.id
                    i['name'] = desc.name
                    i['status'] = desc.status.name
                    i['types'] = desc.types.name
                    i['templ'] = desc.templ.name
                    i['desc'] = desc.desc
                    
                    info.append(i)
                except:
                    continue
    return HttpResponse(simplejson.dumps(info))

#关联资产search list
def descTaskGroup_read(request, id):   
    info = []
    if request.method == 'GET':
        taskGroup = TaskGroup.objects.filter(project_id=id,is_active=True)
        
        for tg in taskGroup:
            i = {}
            i['id'] = tg.id
            i['name'] = tg.name
            info.append(i)
    return HttpResponse(simplejson.dumps(info))



#关联资产添加
def descTaskGroup_create(request):
    info = {}
    
    if request.method == 'POST':
        src = request.POST.get('src','')
        refs = request.POST.get('refs','')
        
        type, src_id = src.split('_')
        
        refs = json.loads(refs)
        success_count = 0
        for ref in refs:
            ref_id = ref['id'].split('_')[1]
            
            tgr = TaskGroupRel.objects.filter(src_id=src_id, desc_id=ref_id)
            
            if src != ref:
                if len(tgr) == 0:
                    TaskGroupRel.objects.create(src_id=src_id, desc_id=ref_id)
                    success_count += 1
                
        info['successCount'] = success_count
            
    return HttpResponse(simplejson.dumps(info))

#关联资产删除
def descTaskGroup_destroy(request):
    info = {}
    if request.method == 'POST':
        rows = request.POST.get('rows','')
        rows = json.loads(rows)
        
        print rows
        
        success_count = 0
        for row in rows:
            print row['relId']
            try:
                tgr = TaskGroupRel.objects.get(id=int(row['relId']))
                tgr.delete()
                success_count += 1
            except:
                pass
                
        info['successCount']=success_count
    return HttpResponse(simplejson.dumps(info))

#查询项目汇总信息
def project_summary(request):
    info = {}
    if request.method == 'POST':
        proj_id = request.POST.get('proj_id','')
        
        print proj_id
        
        #用户任务
        user_task = Task.objects.filter(project=Project.objects.get(id=proj_id))
        
        #查询用户任务数
        info['taskCount'] = user_task.count()
        #正在进行
        info['wipCount'] = user_task.filter(status=12).count()
        #已发布
        info['publishCount'] = user_task.filter(publish_status=1).count()
        #已提交
        info['submitReCount'] = user_task.filter(review_status=1).count()
        #审核通过
        info['passedCount'] = user_task.filter(review_status=3).count()
        #QC通过
        info['qcCount'] = user_task.filter(qc_flag=1).count()
        
    return HttpResponse(simplejson.dumps(info))

#查询项目用户汇总信息
def project_user_summary(request):
    info = {}
    if request.method == 'POST':
        proj_id = request.POST.get('proj_id','')
        user_id = request.POST.get('user_id','')
        
        print proj_id
        print user_id
        
        #用户任务
        user_task = Task.objects.filter(user=User.objects.get(id=user_id), project=Project.objects.get(id=proj_id))
        
        #查询用户任务数
        info['taskCount'] = user_task.count()
        #正在进行
        info['wipCount'] = user_task.filter(status=12).count()
        #已发布
        info['publishCount'] = user_task.filter(publish_status=1).count()
        #已提交
        info['submitReCount'] = user_task.filter(review_status=1).count()
        #审核通过
        info['passedCount'] = user_task.filter(review_status=3).count()
        #QC通过
        info['qcCount'] = user_task.filter(qc_flag=1).count()
        
    return HttpResponse(simplejson.dumps(info))

#项目人员详情获取
def projectPerformance_detail(request):
    info = {}
    if request.method == 'POST':
        p_id = request.POST.get('projectId','')     
        try:
            projectPeople = ProjectPeople.objects.filter(project__id__exact = p_id)[0] 
        except:
            projectPeople = ''    
            
        if True:
            i = 0
            l = []
            for user in User.objects.all():
                try:
                    profile = UserProfile.objects.get(user = user)
                except:
                    profile = ''
                i += 1
                k = {}
                k['id'] = user.id
                k['user'] = user.username
                k['name'] = user.first_name           
                
                sp = 0
                sa = 0
                efficiency = 0
                
                now = timezone.now()

                week_start = now - datetime.timedelta(days = now.weekday())
                week_end = now + datetime.timedelta(days = (7 - now.weekday()))
                
                #遍历用户任务
                for task in Task.objects.filter(user=user):
                    if task.start_time == None or task.end_time == None or task.finish_time == None:
                        pass
                    else:
                        if timezone.localtime(task.finish_time) >= week_start and timezone.localtime(task.finish_time) <= week_end:
                            sp += (timezone.localtime(task.end_time) - timezone.localtime(task.start_time)).days
                            sa += (timezone.localtime(task.finish_time) - timezone.localtime(task.start_time)).days
                        
#                         print sp
#                         print sa
                try:
                    efficiency = round(float(sp) / float(sa),2)
                except:
                    efficiency = 0
                
                k['efficiency'] = efficiency
                
                l.append(k)
            
            
            ll = dict_sort(l, 'efficiency', True)
            
            info['total'] = i
            info['rows'] = ll
        else:
            info['total'] = 0
            info['rows'] = []
    return HttpResponse(simplejson.dumps(info))

