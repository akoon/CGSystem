# -*- coding: utf-8 -*-
'''
此文件中包含项目中供views调用的公用函数，这些函数都是与业务逻辑相关的，基本在另一个项目中很难被复用，但是可以供当前项目多个地方调用
'''
import threading
import os, sys
import shutil
import globalvar
import ConfigParser
import uuid
import urllib, cookielib, urllib2
import json
import datetime
from django.core import mail
from sets import Set

from ProjectManSys.models import *
import datetime
# import django.core.mail


#生成资产路径
def getPath(id):
    l = []
    try:
        tg = TaskGroup.objects.filter(id=id)[0]
    except:
        tg = ''
    if tg:
        group= tg.group
        l.append(group.name)
        l.append(tg.name)
        while True:
            if not group.parent_id:
                l.insert(0,group.project.name)
                break
            else:
                group = Groups.objects.filter(id=group.parent_id)[0]
                l.insert(0,group.name)
    l.insert(0,'$PROJECT')
    path = ''
    for i in l:
        path = os.path.join(path,i)
    return path
                    

def groupsTree1(project_id, parent = None):
    result = []
    groups = Groups.objects.filter(parent = parent, project = project_id)
    for item in groups:
        k = {}
        k['id'] = item.id
        k['name'] = item.name
        k['text'] = item.name
        k['project'] = item.project.name
        k['desc'] = item.desc
        k['children'] = groupsTree1(project_id, item.id)
        k['iconCls'] = "icon-blank"
        result.append(k)
    return result

#遍历资产组树
def groupsTree(id,p_id=None,read=False):
    try:
        id = int(id)
    except:
        id =-1
    if id >= 0 : 
        try:
            if p_id and (id == 0):
                gs = Groups.objects.filter(parent = 0,project = p_id)
            else:
                gs = Groups.objects.filter(parent = id)
        except:
            gs = ''
        if gs:
            l = []
            for g in gs:
                k = {}
                k['id'] = g.id
                if (p_id == None) and (id == 0) and read:
                    k['name'] = g.name+'【'+g.project.name+'】'
                    k['text'] = g.name+'【'+g.project.name+'】'
                else:
                    k['name'] = g.name 
                    k['text'] = g.name
                if id == 0:
                    if g.project:
                        k['project'] = g.project.name
                k['desc'] = g.desc
                k['children'] = groupsTree(g.id)
                k['iconCls'] = "icon-blank"
                l.append(k)
            return l
        else:
            return ''

# 遍历资产树
def taskgroupTree(id,p_id=None,read=False):
    try:
        id = int(id)
    except:
        id =-1
    if id >= 0 : 
        try:
            if p_id and (id == 0):
                gs = Groups.objects.filter(parent = 0,project = p_id)
            else:
                gs = Groups.objects.filter(parent = id)
        except:
            gs = ''
        if gs:
            l = []
            for g in gs:
                k = {}
                k['id'] = 'g_' + str(g.id)
                if (p_id == None) and (id == 0) and read:
                    k['name'] = g.name+'【'+g.project.name+'】'
                    k['text'] = g.name+'【'+g.project.name+'】'
                else:
                    k['name'] = g.name 
                    k['text'] = g.name
                if id == 0:
                    if g.project:
                        k['project'] = g.project.name
                k['desc'] = g.desc
                k['iconCls'] = "icon-blank"
                childen = taskgroupTree(g.id)
#                print 'childen    ',     childen
                if childen != '':
                    k['children'] = childen
                else:
                    taskgroups = TaskGroup.objects.filter(group_id=g.id)
                    tgs = []
                    for taskgroup in taskgroups:
                        tg = {}
                        tg['id'] = 'tg_' + str(taskgroup.id)
                        tg['name'] = taskgroup.name
                        tg['text'] = taskgroup.name
                        tg['iconCls'] = "icon-blank"
                        tgs.append(tg)
                    k['children'] = tgs
                l.append(k)
            return l
        else:
            return ''

# 遍历可被关联的资产树(与资产树不同的是如果某资产组下没有资产则不显示该资产组)
def taskgroupTreeRelateable(id,p_id=None,read=False,except_list=[]):
    try:
        id = int(id)
    except:
        id =-1
    if id >= 0 : 
        try:
            if p_id and (id == 0):
                gs = Groups.objects.filter(parent = 0,project = p_id)
            else:
                gs = Groups.objects.filter(parent = id)
        except:
            gs = ''
        if gs:
            l = []
            for g in gs:
                k = {}
                k['id'] = 'g_' + str(g.id)
                if (p_id == None) and (id == 0) and read:
                    k['name'] = g.name+'【'+g.project.name+'】'
                    k['text'] = g.name+'【'+g.project.name+'】'
                else:
                    k['name'] = g.name 
                    k['text'] = g.name
                if id == 0:
                    if g.project:
                        k['project'] = g.project.name
                k['desc'] = g.desc
                
                childen = taskgroupTreeRelateable(g.id)
#                print 'childen    ',     childen
                if childen != '':
                    k['children'] = childen
                    if len(childen) != 0:
                        l.append(k)
                else:
                    taskgroups = TaskGroup.objects.filter(group_id=g.id)
                    tgs = []
                    if len(taskgroups) != 0:
                        for taskgroup in taskgroups:
                            
                            tg = {}
                            tg['id'] = 'tg_' + str(taskgroup.id)
                            tg['name'] = taskgroup.name
                            tg['text'] = taskgroup.name
                            tg['iconCls'] = 'icon-blank'
                            
                            #跳过不必要添加的元素
                            if tg['id'] in except_list:
                                continue
                            
                            tgs.append(tg)
                            
                        k['children'] = tgs
                        l.append(k)
            return l
        else:
            return ''

# 遍历可做为当前资产父资产的树    不包括当前资产和其子资产.
#def taskgroupTreeParent(id,p_id=None,read=False, tg):
#    try:
#        id = int(id)
#    except:
#        id =-1
#    if id >= 0 : 
#        try:
#            if p_id and (id == 0):
#                gs = Groups.objects.filter(parent = 0,project = p_id)
#            else:
#                gs = Groups.objects.filter(parent = id)
#        except:
#            gs = ''
#        if gs:
#            l = []
#            for g in gs:
#                k = {}
#                k['id'] = 'g_' + str(g.id)
#                if (p_id == None) and (id == 0) and read:
#                    k['name'] = g.name+'【'+g.project.name+'】'
#                    k['text'] = g.name+'【'+g.project.name+'】'
#                else:
#                    k['name'] = g.name 
#                    k['text'] = g.name
#                if id == 0:
#                    if g.project:
#                        k['project'] = g.project.name
#                k['desc'] = g.desc
#                k['iconCls'] = "icon-blank"
#                childen = taskgroupTree(g.id)
##                print 'childen    ',     childen
#                if childen != '':
#                    k['children'] = childen
#                else:
#                    taskgroups = TaskGroup.objects.filter(group_id=g.id)
#                    tgs = []
#                    for taskgroup in taskgroups:
#                        tg = {}
#                        tg['id'] = 'tg_' + str(taskgroup.id)
#                        tg['name'] = taskgroup.name
#                        tg['text'] = taskgroup.name
#                        tg['iconCls'] = "icon-blank"
#                        tgs.append(tg)
#                    k['children'] = tgs
#                l.append(k)
#            return l
#        else:
#            return ''

# 删除树中包含指定id序列的所有元素
#def remove_from_tree(tree_node, del_list):
#    for node in tree_node:
#        
#        try:
#            remove_from_tree(node['children'], del_list)
#        except:
#            #删除列表已有节点
#            if node['id'] in del_list:
#                print 'node     ', node
#                tree_node.remove(node)

########################增强文件及文件夹复制######################### 

class CopyFile(threading.Thread):
    def __init__(self):
        #线程类的初始化
        threading.Thread.__init__(self)
        self.src = None             #复制的源
        self.dst = None             #复制的目标
        self.dst2 = None            #复制的目标2
        self.error = None           #错误信息
        self.srcIsDir = None        #复制源是否是文件件 
        self.dstIsExist = None      #目标文件夹是否存在
        self.dst2IsExist = None     #目标文件夹是否存在
        self.sedDir = []            #复制源二级目录列表
        self.srcNames = []          #源文件夹遍历
        self.dstNames = []          #目标文件夹遍历
        self.dst2Names = []         #目标文件夹遍历
        self.isSucess = None        #文件复制状态
        self.task = None            #当前复制任务的信息
        self.onlyCopy = True        #是否修改任务版本及信息
        self.isCopy = True          #是否复制文件

        
    def run(self):
        #线程的执行
        while globalvar.Queue:
            info = globalvar.Queue[0]
            source= info['src']
            self.dst = info['dst']
            self.dst2 = info['dst2']
            self.task = info['task']
            if info['onlyCopy']:
                self.onlyCopy = info['onlyCopy']
            if info['isCopy']:
                self.isCopy = info['isCopy']
            if self.isCopy:
                for src in source:
                    self.src =src
                    self.check_ext()                            #检测参数
                    if not self.error:                          #检测错误
                        self.get_names()                        #获取文件夹内容
                        if self.dstIsExist or self.dst2IsExist: #判断目标是否是文件夹
                            self.check_rep()                    #检测重复文件或文件夹
                        if not self.error:                      #检测错误
                            self.ready()                        #进入文件复制
                        else:
                            globalvar.Errors = self.error
                    else:
                        globalvar.Errors = self.error            
            del globalvar.Queue[0]
            if self.onlyCopy:
                self.task_status()
        globalvar.ThreadStatus = False
 
    
    def task_status(self):
        if self.isSucess: 
            task = Task.objects.get(id=self.task[0])
            if task.version:
                task.version = ('000'+str(int(task.version)+1))[-3:]
            else:
                task.version = '001'
            task.path = ''
            task.qc_flag = self.task[1]
            task.publish_status = 1
            task.save()
            
            create_time = datetime.datetime.now().strftime('%Y-%m-%d')
            
            tv = TaskVersion.objects.create(
                name=task.name,
                project=task.project,
                task_group=task.task_group,
                priority=task.priority,
                desc=task.desc,
                use_time=task.use_time,
                version=task.version,
                path=task.path,
                qc_flag=task.qc_flag,
                publish_status=task.publish_status,
                review_status=task.review_status,
                publish_time=create_time,
                task=task)
            
            if task.status:
                tv.status = task.status
            if task.types:
                tv.types = task.types
            if task.user:
                for u in task.user.all():
                    tv.user.add(u)
            if task.start_time:
                tv.start_time = task.start_time
            if task.end_time:
                tv.end_time = task.end_time
            if task.percent:
                tv.percent = task.percent
            tv.save()
            
               
    def check_ext(self):
        #检查复制源和目标源的合理性
        if os.path.exists(self.src):
            if os.path.isdir(self.src):
                self.srcIsDir = True
            else:
                self.srcIsDir = False
        else:
            self.error = '源文件或文件夹不存在'     
            
        if os.path.exists(self.dst):
            if os.path.isfile(self.dst):
                self.error = '复制目标1是文件'
            else:
                self.dstIsExist = True
        else:
            self.dstIsExist = False
            
        if os.path.exists(self.dst2):
            if os.path.isfile(self.dst2):
                self.error = '复制目标2是文件'
            else:
                self.dst2IsExist = True
        else:
            self.dst2IsExist = False

    
    def get_names(self): 
        #获得源文件夹和目标文件中的文件和文件夹
        if self.srcIsDir :
            self.srcNames = os.listdir(self.src)
        if self.dstIsExist:            
            self.dstNames = os.listdir(self.dst)
        if self.dst2IsExist:            
            self.dst2Names = os.listdir(self.dst2)
               
    def check_rep(self):
        #检测重复的文件和文件夹
        if self.srcIsDir:
            for i in self.srcNames:
                for j in self.dstNames:
                    if i == j:
                        self.error = i + '文件已存在'
        else:
            for i in self.dstNames:
                if self.src == i:
                    self.error = i + '文件已存在'
            for i in self.dst2Names:
                if self.src == i:
                    self.error = i + '文件已存在'
 
    
    def check_dir(self):
        #检测复制源是否有二级目录并返回列表目录名
        for i in self.srcNames:
            if os.path.isdir(i):
                self.sedDir.append(i) 

    
    def ready(self):
        #复制前的准备工作
        if not self.dstIsExist:         #检测目标文件夹是否存在
            os.makedirs(self.dst)       #不存在则创建文件夹
        if not self.dst2IsExist:        #检测目标2文件夹是否存在
            os.makedirs(self.dst2)      #不存在则创建文件夹
        if self.srcIsDir:               #检测是否源是个文件夹
            self.check_dir()            #检测源文件夹中是否有二级二级文件夹
            if self.sedDir:             #检测是否有二级文件夹
                self.copy_tree()        #文件及文件夹的复制
            else:
                self.copy_files()       #多文件复制
        else:
            self.copy_file()            #单文件复制

    
    def copy_file(self):
        #单文件复制       
        self.isSucess = False
        try: 
            shutil.copy(self.src, self.dst)
            shutil.copy(self.src, self.dst2)
            self.isSucess = True
        except:
            pass
 
            
    def copy_files(self):
        #多文件复制
        self.isSucess = False
        try:
            for i in self.srcNames:
                src = os.path.join(self.src,i)
                shutil.copy(src, self.dst)
                shutil.copy(src, self.dst2)
            self.isSucess = True
        except:
            pass
    
    def copy_tree(self):
        #文件及文件夹复制
        pass
    

def read_config_file():
    return os.path.join(os.getcwd(), 'PillarsCGSystem', 'user.settings')  
#     return os.path.join('/var/www/html/', 'PillarsCGSystem', 'PillarsCGSystem', 'user.settings')    

#配置文件读取
def read_config(section, option):
    config_file = read_config_file()
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.get(section, option)

#读取section下所有item
def read_item_section(section):
    config_file = read_config_file() 
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.items(section)
    
#配置文件写入
def wirte_config(section, option, value):
    config_file = read_config_file()    
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    config.set(section, option, value)
    config.write(open(config_file, "w")) 
    

def get_mac_address():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac


def validate_pillars_id(pillars_id, pillars_pwd, pillars_sn, mac_address):
    #TODO: pillars id 验证逻辑
    print pillars_id
    print pillars_pwd
    print pillars_sn
    print mac_address
    
    pillarsCloud = PillarsCloud('172.16.253.201', 8000)
    ret = pillarsCloud.valiPillarsID(pillars_id, pillars_pwd, pillars_sn, mac_address, 'orangemansys/validateactivation')
    
    if ret and ret['success'] == 'true':
        for app in ret['apps']:
            wirte_config('apps', app, True)
        return True
    else:
        return False

class PillarsCloud(object):
    
    COOKIE = os.path.expanduser('~') + '/cookie'

    def __init__(self, server, port):
        self.__server = server
        self.__port = port
        self.__islogin = False
    
    def login(self, username, password, url):
        login_url = 'http://%s:%d/%s' % (self.__server, self.__port, url)
        login_data = urllib.urlencode({ 'login_input_username' : username,
                                        'login_input_password' : password})
        
        req = urllib2.Request(login_url, login_data) 
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0)')
        
        ckjar = cookielib.MozillaCookieJar(PillarsCloud.COOKIE)
        ckproc = urllib2.HTTPCookieProcessor(ckjar)
        try:
            opener = urllib2.build_opener(ckproc)
            f = opener.open(req)
            ckjar.save(ignore_discard=True, ignore_expires=True)
            f.close()
            #判断返回的cookie值的情况
            if ckjar._cookies.__len__() > 0:
                self.__islogin = True
                return True
            else:
                return False
        except:
            return False

    def post(self, url, parm):
        """The parm is a dict"""
        data = urllib.urlencode(parm)
        try:
            req = urllib2.Request(url, data) 
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0)')
            ckjar = cookielib.MozillaCookieJar(PillarsCloud.COOKIE)
            ckproc = urllib2.HTTPCookieProcessor(ckjar)
            opener = urllib2.build_opener(ckproc)
            f = opener.open(req)
            res = f.read()
            ckjar.save(ignore_discard=True, ignore_expires=True)
            f.close()
        except IOError, e:
            print e
            return False
        
    def valiPillarsID(self, pillarsID, passwd, sn, mac_address, url):
        url = r'http://%s:%d/%s' % (self.__server, self.__port, url)
        parm = {}
        parm['pillarsid'] = pillarsID
        parm['pillarspwd'] = passwd
        parm['serialnumber'] = sn
        parm['macaddress'] = mac_address
        res = self.post(url, parm)
        if res:
            result = json.loads(res)
            return result
        else:
            return False


def user_flag(user):
    
    #超级管理员
    if user.username == 'admin':
        return 0
    #管理员
    elif user.is_superuser == 1 and user.is_staff == 1 and user.is_active==1:
        return 1
    #项目经理
    elif user.is_superuser == 1 and user.is_staff==0 and user.is_active == 1:
        return 2
    #员工
    elif user.is_superuser == 0 and user.is_staff==1 and user.is_active == 1:
        return 3
    #其他
    elif user.is_superuser == 0 and user.is_staff==0 and user.is_active == 1:
        return 4
    #未知
    else:
        return 5

#级联创建目录
def cascadeCreateDir(path, attrbutes):
    for attr in attrbutes:
        path = path + '/' + attr
        if os.path.isdir(path) == False:
            os.mkdir(path)
    return path

#文件名修改,将数组中的元素拼接成主文件名,中间用分隔符,保留原扩展名.
def generateNewFileName(src, attrbutes, spliter):
    #取扩展名
    result = ''
    ext = src.split('.')[-1]
    for attr in attrbutes:
        if result != '': 
            result = result + spliter + str(attr)
        else:
            result = str(attr)
    
    result = result+'.'+ext
    
    return result

#查询资源文件有效性
def ifMediaAvalible(url):
    return os.path.exists(os.path.join(os.path.dirname(__file__)) + '/..' + url)

#查询是否有后缀名相同的文件
def findSameExt(filelist):
    extlist = []
    for fl in filelist:
        extlist.append(fl.split('.')[-1])
    
    if len(Set(extlist)) != len(extlist):
        return True
    else:
        return False

#判断是否开始时间小于结束时间
def dateCompare(start, end):
    startDate = start.split('-')
    endDate = end.split('-')
    sy = int(startDate[0])
    sm = int(startDate[1])
    sd = int(startDate[2])
    
    ey = int(endDate[0])
    em = int(endDate[1])
    ed = int(endDate[2])
    
    startDate = datetime.date(sy, sm, sd)
    endDate = datetime.date(ey, em, ed)
    
    if startDate <= endDate:
        return True
    else:
        return False

#字典型列表排序
def dict_sort(l, key, reverse):
    def eff(s):
        return s[key]
    
    return sorted(l, key = eff, reverse = reverse)
    
# def send_mail(subject, message, from_email, recipient_list,):
#     is_skip = read_config('email','is_skip')
#     if is_skip == 'True':
#         return False
#     
#     email_host_password = read_config('email','email_host_password')
#     email_use_tls = read_config('email','email_use_tls')
#     email_port = read_config('email','email_port')
#     email_host_user = read_config('email','email_host_user')
#     email_host = read_config('email','email_host')
#     mail.send_mail(subject, message, from_email, recipient_list, False, email_host_user, email_host_password)

######################## 邮件相关 #########################
#class MailService(django.core.mail):
#    def __init__(self):
#        self.from_email = ''
#        self.to_email = ''
#        self.auth_user = ''
#        self.auth_password = ''
#        
#    def send(self, userFrom, userTo, title, msg):
#        print userFrom.first_name
#        print userTo.first_name
#        print title
#        print msg
##        self.send_mail(subject, message, from_email, recipient_list, fail_silently, auth_user, auth_password)

#遍历删除项目的.svn文件夹
#find ./ -name '.svn' -exec rm -rf {} \;

if __name__ == "__main__":
#    print generateNewFileName('aaa.txt', ['project', 'asset', 'task'], '_')
#    print cascadeCreateDir('/Pillars/Project', ['project', 'asset', 'task'])
    print dateCompare(u'2013-5-23', u'2013-5-22')

