# -*- coding: utf-8 -*-
'''
Created on 2013-5-21

@author: hao.yu
'''
import socket, struct

#存储所有的渲染节点，对渲染节点的各种处理可以成员方法，比如查找IP为某某的节点信息，对节点按照主频排序等等。
class RenNodes(object):
    nodestatus_dead   = 0
    nodestatus_active = 1
    nodestatus_busy   = 2
    class Node:
        def __init__(self, node):
            self.version       = node[0] #版本号，是一串数字(a.b.c.d)
            self.ipv4addr      = node[1] #此节点的IP地址
            self.cpu_frequence = node[2] #节点的主频
            self.cpu_num       = node[3] #节点的核心数
            self.ram_size      = node[4] #节点的内存大小
            self.has_maya      = node[5] #是否支持maya，0代表不支持
            self.has_houdini   = node[6]
            self.has_3dmax     = node[7]
            self.status        = node[8] #节点状态，0代表nodestatus_dead，1代表nodestatus_active，2代表nodestatus_busy
            
        def change_node_status(self, status):
            self.status = status
            
        def tolist(self):
            node = []
            node.append(self.version)
            node.append(socket.inet_ntoa(struct.pack('I', self.ipv4addr)))
            node.append(self.cpu_frequence)
            node.append(self.cpu_num)
            node.append(self.ram_size)
            node.append(self.has_maya)
            node.append(self.has_houdini)
            node.append(self.has_3dmax)
            node.append(self.status)
            return node
            
    def __init__(self):
        self.__nodes = {}
        
    def get_render_nodes(self):
        return self.__nodes
    
    def find_render_node(self, ipv4addr):
        return self.__nodes.get(ipv4addr)
    
    def insert_render_node(self, node):
        self.__nodes[node.ipv4addr] = node
    
    def clear_render_nodes(self):
        self.__nodes.clear()

class RenTasks(object):
    status_uncomment  = 0 #未提交
    status_pending    = 1 #已提交
    status_processing = 2 #正在处理
    status_processed  = 3 #处理完毕
    status_error      = 4 #出错
    status_deleted    = 5 #已删除了（放入回收站了）
    cur_render_task_id=4294967295 - 1000000 #当前任务数
    
    class Task:
        def __init__(self, task):
            self.id              = task[0]
            self.type            = task[1]
            self.OwnerIpv4Addr   = task[2]
            self.Priority        = task[3]
            self.StartFrame      = task[4]
            self.FrameCount      = task[5]
            self.Step            = task[6]
            self.AddTime         = task[7]
            self.RenderStartTime = task[8]
            self.RenderStopTime  = task[9]
            self.Groups          = task[10]
            self.FileType        = task[11]
            self.TaskName        = task[12]
            self.RenderName      = task[13] 
            self.InputPath       = task[14]
            self.InputFileName   = task[15]
            self.OutputPath      = task[16]
            self.Misc            = task[17]
            #任务属性
            self.status = 0 #任务状态
            self.username = None #提交用户
            self.sub_tasks = RenSubTasks()#子任务列表
        
        def change_task_status(self, status):
            self.status = status
            
        def tolist(self):
            task = []
            task.append(self.id)
            task.append(self.type)
            task.append(socket.inet_ntoa(struct.pack('I', self.OwnerIpv4Addr)))
            task.append(self.Priority)
            task.append(self.StartFrame)
            task.append(self.FrameCount)
            task.append(self.Step)
            task.append(self.AddTime)
            task.append(self.RenderStartTime)
            task.append(self.RenderStopTime)
            task.append(self.Groups)
            task.append(self.FileType)
            task.append(self.TaskName)
            task.append(self.RenderName)
            task.append(self.InputPath)
            task.append(self.InputFileName)
            task.append(self.OutputPath)
            task.append(self.Misc)
            task.append(self.status)
            task.append(self.username)
            subtasks = []
            for subtask in self.sub_tasks.get_subtasks():
                subtasks.append(subtask.tolist())
            task.append(subtasks)
            return task
        
    def __init__(self):
        self.__tasks = {}
        
    def get_tasks(self):
        return self.__tasks
    
    def find_task(self, taskid):
        return self.__tasks.get(taskid)
    
    def insert_task(self, task):
        self.__tasks[task.id] = task
        
    def clear_tasks(self):
        self.__tasks.clear()

class RenSubTasks(object):
    substatus_uncommit   = 0
    substatus_pending    = 1
    substatus_processing = 2
    substatus_processed  = 3
    substatus_error      = 4
    class Subtask:
        def __init__(self, subtask):
            self.index        = subtask[0]
            self.task_id      = subtask[1]
            self.startframe   = subtask[2]
            self.endframe     = subtask[3]
            self.rendernodeip = subtask[4]
            self.status       = subtask[5]
            if 6 < len(subtask): 
                self.start_time   = subtask[6]
                self.end_time     = subtask[7]
            else:
                self.start_time   = 0
                self.end_time     = 0
     
        def change_subtask_status(self, status):
            self.status = status

        def tolist(self):
            subtask = []
            subtask.append(self.index)
            subtask.append(self.task_id)
            subtask.append(self.startframe)
            subtask.append(self.endframe)
            subtask.append(socket.inet_ntoa(struct.pack('I', self.rendernodeip)))
            subtask.append(self.status)
            return subtask
            
    def __init__(self):
        self.__subtasks = []

    def get_subtasks(self):
        return self.__subtasks
    
    def find_subtask(self, subtaskindex):
        ary_index = 0
        for subtask in self.__subtasks:
            if subtaskindex == subtask.index:
                return (subtask, ary_index)
            ary_index += 1
        return None
    
    def insert_subtask(self, subtask):
        while len(self.__subtasks) <= subtask.index:
            self.__subtasks.append(subtask)
        self.__subtasks[subtask.index] = subtask     
    
    def clear_subtasks(self):
        self.__subtasks = []
    
class RenInfos(object):
    pass