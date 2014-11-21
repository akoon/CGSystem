# -*- coding: utf-8 -*-
'''
Created on 2013-5-20

@author: hao.yu
'''
import asyncore, socket, time, threading
from collections import deque
import util, json2binary as j2b
from RenderManSys.renderelement import RenNodes, RenTasks, RenSubTasks
import struct
from RenderManSys import json2binary

class BaseAdminTool(asyncore.dispatcher):
    status_unlogin      = 0
    status_loginning    = 1
    status_login_ok     = 2
    status_login_failed = 3
    
    DEFAULT_BUFSIZE = 4096
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.loginLock = threading.Condition()
        self.loginstatus = BaseAdminTool.status_unlogin
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(address)
        #用于同步前台页面提交命令
        self.sendbuf = deque()
        #用于缓存接受数据
        self.recvbuf = b''
        #保存链接的渲染服务器地址
        self.address = address
       
    def __del__(self):
        self.handle_close()
    
    #发送出错的时候会产生链接事件，调用此函数
    def handle_connect(self):
        self.loginstatus = BaseAdminTool.status_login_failed
        
    def handle_error(self):
        asyncore.dispatcher.handle_error(self)
        self.loginstatus = BaseAdminTool.status_login_failed
    
    def handle_close(self):
        self.close()
            
    def writable(self):
        return len(self.sendbuf) > 0
    
    def readable(self):
        return True
      
    def handle_read(self):
        self.recvbuf += self.recv(BaseAdminTool.DEFAULT_BUFSIZE)
        while True:
            buf_len = len(self.recvbuf)
            if buf_len < j2b.cmd_header_len:
                return
            dev_type,cmd_id,client_id,ipv4addr,username,cmd_data_len,cmd_extra_data_len = j2b.rencmd_demux_basecmd(self.recvbuf)
            cmd_len=j2b.cmd_header_len + cmd_data_len + cmd_extra_data_len
            if buf_len < cmd_len:
                return
            self.handle_process_cmd(cmd_id, cmd_data_len, cmd_extra_data_len)
            self.recvbuf = self.recvbuf[cmd_len:]
            
    def handle_write(self):
        while True:
            buf = self.sendbuf.pop()
            sent = self.send(buf)
            if len(buf) > sent:
                self.sendbuf.append(buf[sent:])
                break
            if sent == 0 or len(self.sendbuf) == 0:
                break
    
    #定义一个钩子函数，子类可以重载此函数       
    def handle_process_cmd(self, cmd_id, cmd_data_len, cmd_msg_len):
        pass
        
class AdminTool(BaseAdminTool):
    def __init__(self, address):
        BaseAdminTool.__init__(self, address)
        #用于存储渲染节点
        self.rennodes = RenNodes()
        self.rennodes_rwlock = util.RWLock()
        #用于存储渲染任务,包括渲染子任务。共用一把锁
        self.rentasks = RenTasks()
        self.rensubtasks = RenSubTasks()
        self.rentasks_rwlock = util.RWLock()
        #用于存储渲染输出信息
        self.reninfos = None
        self.reninfos_rwlock = util.RWLock()
        self.__login_render_server()
    
    def get_login_status(self):
        loginstatus = self.loginstatus
        return loginstatus
    
    def handle_process_cmd(self, cmd_id, cmd_data_len, cmd_msg_len):
        #登录
        if cmd_id == j2b.CmdIds.cmd_response_login:
            self.__process_login_response_cmd(cmd_data_len, cmd_msg_len)
        #返回节点
        elif cmd_id == j2b.CmdIds.cmd_render_nodes:
            self.__process_render_nodes(cmd_data_len, cmd_msg_len)    
        #返回挂起的任务
        elif cmd_id == cmd_id == j2b.CmdIds.cmd_unprocess_tasks:
            self.__process_tasks_cmd(RenTasks.status_pending,cmd_data_len, cmd_msg_len)
        #返回正在进行的任务
        elif cmd_id == j2b.CmdIds.cmd_processing_tasks:
            self.__process_tasks_cmd(RenTasks.status_processing,cmd_data_len, cmd_msg_len)
        #返回执行完的任务
        elif cmd_id == j2b.CmdIds.cmd_processed_tasks:
            self.__process_tasks_cmd(RenTasks.status_processed,cmd_data_len, cmd_msg_len)
        #新节点连接
        elif cmd_id == j2b.CmdIds.cmd_new_node:
            self.__process_new_render_node(cmd_data_len,cmd_msg_len)
        #接收到其他admintool提交的任务
        elif cmd_id == j2b.CmdIds.cmd_render_task:
            self.__process_add_render_task_notify(cmd_data_len, cmd_msg_len)
        #子任务发生改变
        elif cmd_id == j2b.CmdIds.cmd_sub_task_changed:
            self.__process_sub_task_changed(cmd_data_len, cmd_msg_len)
        #主任务的所有子任务    
        elif cmd_id == j2b.CmdIds.cmd_sub_tasks_of_task:
            self.__process_sub_tasks_of_task(cmd_data_len, cmd_msg_len)
        #节点状态改变
        elif cmd_id == j2b.CmdIds.cmd_node_status_changed:
            self.__process_node_status_changed(cmd_data_len, cmd_msg_len)
        #子任务成功
        elif cmd_id == j2b.CmdIds.cmd_sub_render_successed:
            self.__process_sub_render_successed(cmd_data_len, cmd_msg_len)
        #渲染任务成功
        elif cmd_id == j2b.CmdIds.cmd_render_successed:
            self.__process_render_successed(cmd_data_len, cmd_msg_len)
        #删除任务回应
        elif cmd_id == j2b.CmdIds.cmd_tasks_deleted:
            self.__process_tasks_deleted(cmd_data_len, cmd_msg_len)
        #提交任务，服务器返回任务的新ID
        elif cmd_id == j2b.CmdIds.cmd_response_render_task:
            self.__process_response_add_render_task(cmd_data_len, cmd_msg_len)
        #提交的任务，不合法
        elif cmd_id == j2b.CmdIds.cmd_render_task_invalid:
            self.__process_render_task_invalid(cmd_data_len, cmd_msg_len)
        
    def store_send_data(self, jsondata, username):
        bindata = self.__json2bin(jsondata, username)
        cmd_count = 0
        for data in bindata:
            self.sendbuf.appendleft(data)
            cmd_count += 1
        return cmd_count
        
    def get_render_nodes(self):
        rennodes = {}
        count = 0
        self.rennodes_rwlock.read_acquire()
        for key in self.rennodes.get_render_nodes():
            node = self.rennodes.get_render_nodes()[key]
            rennodes[count] = node.tolist()
            count += 1
        self.rennodes_rwlock.read_release()
        return rennodes
    
    def get_render_tasks(self):
        rentasks = {}
        count = 0
        self.rentasks_rwlock.read_acquire()
        for key in self.rentasks.get_tasks():
            task = self.rentasks.get_tasks()[key]
            rentasks[count] = task.tolist()
            count += 1
        self.rentasks_rwlock.read_release()
        return rentasks
    
    def __json2bin(self, jsondata, username):
        bindata = []
        for cmddata in jsondata:
            cmd = cmddata.get('cmd')
            if j2b.CmdIds.cmd_render_task == j2b.get_cmd_index(cmd):
                task_id = RenTasks.cur_render_task_id
                RenTasks.cur_render_task_id += 1
                if RenTasks.cur_render_task_id == 4294967295:
                    RenTasks.cur_render_task_id = 4294967295-1000000
                rendertype      = int(cmddata.get('type'))
                OwnerIpv4Addr   = int(util.LOCALIPADDR)
                Priority        = int(cmddata.get('Priority', 1))
                StartFrame      = int(cmddata.get('StartFrame', 1))
                FrameCount      = int(cmddata.get('FrameCount', 1))
                Step            = int(cmddata.get('Step', 1))
                AddTime         = int(cmddata.get('AddTime', time.time()))
                RenderStartTime = int(cmddata.get('RenderStartTime', 0))
                RenderStopTime  = int(cmddata.get('RenderStopTime', 0))
                if cmddata.get('Groups') == '':
                    Groups = 0
                else:
                    Groups      = int(cmddata.get('Groups', 1))
                FileType        = int(cmddata.get('FileType', 0))
                TaskName        = str(cmddata.get('TaskName'))
                RenderName      = str(cmddata.get('RenderName'))
                InputPath       = str(cmddata.get('InputPath', ''))
                InputFileName   = str(cmddata.get('InputFileName', ''))
                OutputPath      = str(cmddata.get('OutputPath', ''))
                Misc            = str(cmddata.get('Misc', ''))

                task = RenTasks.Task([task_id, rendertype, OwnerIpv4Addr, Priority, StartFrame, FrameCount, \
                                     Step, AddTime, RenderStartTime, RenderStopTime, Groups, FileType,\
                                     TaskName, RenderName, InputPath, InputFileName, OutputPath, Misc])
                
                self.rentasks_rwlock.write_acquire()
                self.rentasks.insert_task(task)
                self.rentasks_rwlock.write_release()
                
                InputPath = '/'.join(InputPath.split('/')[2:])
                OutputPath = '/'.join(OutputPath.split('/')[2:])
                print InputPath.split('/'), OutputPath.split('/')
                print InputPath, OutputPath
                
                taskdata = j2b.rencmd_mux_add_task_cmd_data(task_id, rendertype, OwnerIpv4Addr, Priority, StartFrame, FrameCount, \
                                     Step, AddTime, RenderStartTime, RenderStopTime, Groups, FileType,\
                                     TaskName, RenderName, InputPath, InputFileName, OutputPath, Misc)
                
                
                head_taskdata = j2b.rencmd_mux_cmd(j2b.devtype_admin_tool,
                                            j2b.CmdIds.cmd_render_task,
                                            j2b.INVALIDE_ID,#admin tool不用id来管理
                                            util.LOCALIPADDR,
                                            username,
                                            taskdata,
                                            None)
                bindata.append(head_taskdata)
                
        return bindata
            
    #登录渲染服务器
    def __login_render_server(self):
        des_password = util.DES_KEY.encrypt(str(util.LOGINPASSWD))
        cmd_data = j2b.rencmd_mux_login_cmd(j2b.devtype_admin_tool, j2b.CmdIds.cmd_login, util.LOCALIPADDR, util.LOGINNAME, des_password, len(str(util.LOGINPASSWD)))
        self.sendbuf.appendleft(cmd_data)
        
    #接收渲染服务器对登录的返回。可能密码错误登录失败。
    def __process_login_response_cmd(self, cmd_data_len, cmd_msg_len):
        is_login_ok = j2b.rencmd_demux_login_response(self.recvbuf)
        if is_login_ok != 0:
            self.loginstatus = BaseAdminTool.status_login_ok
        else:
            self.loginstatus = BaseAdminTool.status_login_failed    
            self.close()
    
    #接收渲染发过来的所有渲染节点。
    def __process_render_nodes(self, cmd_data_len, cmd_msg_len):        
        node_info_len = j2b.cmd_get_node_info_len()
        node_num = cmd_data_len // node_info_len #整除运算　
        offset = j2b.cmd_header_len
        #先清空整个node
        self.rennodes_rwlock.write_acquire()
        self.rennodes.clear_render_nodes()
        self.rennodes_rwlock.write_release()
        #也清空所有的tasks
        self.rentasks_rwlock.write_acquire()
        self.rentasks.clear_tasks()
        self.rensubtasks.clear_subtasks()
        self.rentasks_rwlock.write_release()
        for i in range(node_num):
            info = j2b.rencmd_demux_render_node_info2(self.recvbuf, offset)
            offset += node_info_len
            node = RenNodes.Node(info)
            self.rennodes_rwlock.write_acquire() 
            self.rennodes.insert_render_node(node)
            self.rennodes_rwlock.write_release()
            
    def __process_tasks_cmd(self, task_status, cmd_data_len, cmd_msg_len):
        tasks = j2b.rencmd_demux_tasks(self.recvbuf, cmd_data_len, j2b.cmd_header_len)
        for task_info in tasks:
            task = RenTasks.Task(task_info[0])
            task.status = task_status
            task.username = task_info[2]
            for sub_info in task_info[1]:
                task.sub_tasks.insert_subtask(RenSubTasks.Subtask(sub_info))
            self.rentasks_rwlock.write_acquire()
            self.rentasks.insert_task(task)
            self.rentasks_rwlock.write_release()
            
    def __process_new_render_node(self, cmd_data_len, cmd_msg_len):
        info = j2b.rencmd_demux_render_node_info(self.recvbuf)
        node = RenNodes.Node(info)
        self.rennodes_rwlock.write_acquire()
        node_item = self.rennodes.find_render_node(node.ipv4addr)
        if node_item:
            self.rennodes.get_render_nodes().pop(node_item.ipv4addr)
        self.rennodes.get_render_nodes()[node.ipv4addr] = node
        self.rennodes_rwlock.write_release()
        
    def __process_add_render_task_notify(self, cmd_data_len, cmd_msg_len):
        username_len = struct.unpack_from('I', self.recvbuf, json2binary.cmd_header_len)[0]
        username = struct.unpack_from('{0}s'.format(username_len), self.recvbuf, json2binary.cmd_header_len + struct.calcsize('I'))[0]
        
        task_info, offset = j2b.rencmd_demux_render_task(self.recvbuf, j2b.cmd_header_len + struct.calcsize('I') + username_len)  
        #将任务添加到列表中
        task = RenTasks.Task(task_info)
        self.rentasks_rwlock.write_acquire()
        #如果任务已存在，则不处理
        if self.rentasks.find_task(task.id):
            self.rentasks_rwlock.write_release()
            return;#FIXME:是否应该更新现有render task
        task.change_task_status(RenTasks.status_pending)
        task.username = username
        self.rentasks.insert_task(task)
        self.rentasks_rwlock.write_release()
    
    def __process_sub_task_changed(self, cmd_data_len, cmd_msg_len):
        sub_task_info = j2b.rencmd_demux_one_sub_task(self.recvbuf, cmd_data_len)        
        sub_task = RenSubTasks.Subtask(sub_task_info)
        self.rentasks_rwlock.write_acquire()
        #跟据id找到主任务
        task = self.rentasks.find_task(sub_task.task_id)
        #更新task中的对应子任务
        old_sub_task, i = task.sub_tasks.find_subtask(sub_task.index)
        task.sub_tasks.get_subtasks()[i] = sub_task
        self.rentasks_rwlock.write_release()
        
    def __process_sub_tasks_of_task(self, cmd_data_len, cmd_msg_len):
        #命令主体是很多任务的子任务们
        sub_task_infos = j2b.rencmd_demux_sub_tasks_of_task(self.recvbuf, cmd_data_len)
        self.rentasks_rwlock.write_acquire()
        for task_id in sub_task_infos:
            task = self.rentasks.find_task(task_id)
            if task:
                #task的状态必须变为正在处理
                task.change_task_status(RenTasks.status_processing)
                #迭代所有子任务们
                sub_tasks = sub_task_infos[task_id]
                for sub_task_info in sub_tasks:
                    subtask = RenSubTasks.Subtask(sub_task_info)
                    task.sub_tasks.insert_subtask(subtask)
        self.rentasks_rwlock.write_release()
        
    def __process_node_status_changed(self, cmd_data_len, cmd_msg_len):
        #命令主体是某个render node的ipv4addr
        node_ip,node_status = j2b.rencmd_demux_render_node_status(self.recvbuf, cmd_data_len)
        self.rennodes_rwlock.write_acquire()
        #找到ip对应的node
        node = self.rennodes.find_render_node(node_ip)
        if node:
            node.change_node_status(node_status)
        self.rennodes_rwlock.write_release()
        
    def __process_sub_render_successed(self, cmd_data_len, cmd_msg_len):
        #记录下这个sub task的统计信息
        sub_task_info, sub_task_stat = j2b.rencmd_demux_sub_render_successed(self.recvbuf, cmd_data_len)        
        sub_task = RenSubTasks.Subtask(sub_task_info)
        #保存下stat
        sub_task.stat = sub_task_stat
        self.rentasks_rwlock.write_acquire()
        #跟据id找到主任务
        task = self.rentasks.find_task(sub_task.task_id)
        #更新task中的对应子任务
        old_sub_task, i = task.sub_tasks.find_subtask(sub_task.index)
        task.sub_tasks.insert_subtask(sub_task)
        self.rentasks_rwlock.write_release()
        
    def __process_render_successed(self, cmd_data_len, cmd_msg_len):
        #一个任务的所有子任务都成功完成了，改变其状态
        task_id = j2b.rencmd_demux_task_successed(self.recvbuf, cmd_data_len)   
        self.rentasks_rwlock.write_acquire()
        #找到old_id对应的任务
        task = self.rentasks.find_task(task_id)
        if task:
            #找到了，替换之
            task.change_task_status(RenTasks.status_processed)
        self.rentasks_rwlock.write_release()
        
    def __process_tasks_deleted(self, cmd_data_len, cmd_msg_len):
        #删除渲染任务
        task_list = j2b.rencmd_demux_delete_task_cmd_data(self.recvbuf)
        self.rentasks_rwlock.write_acquire()
        for task_id in task_list:
            self.rentasks.get_tasks().pop(task_id)
        self.rentasks_rwlock.write_release()
        
    def __process_response_add_render_task(self, cmd_data_len, cmd_msg_len):
        old_id, new_id = j2b.rencmd_demux_response_new_render_task(self.recvbuf)
        self.rentasks_rwlock.write_acquire()
        task = self.rentasks.find_task(old_id)
        self.rentasks.get_tasks().pop(old_id)
        task.id = new_id
        task.change_task_status(RenTasks.status_pending)
        self.rentasks.insert_task(task)
        self.rentasks_rwlock.write_release()
        
    def __process_render_task_invalid(self,cmd_data_len, cmd_msg_len):
        #收到提交的任务不合法的通知
        old_id, err_msg = j2b.rencmd_demux_render_task_invalid(self.recvbuf, cmd_data_len)
        self.rentasks_rwlock.write_acquire()
        task = self.rentasks.find_task(old_id)
        task.change_task_status(RenTasks.status_error)
        self.rentasks_rwlock.write_release()
        
if __name__ == '__main__':
    admintool = AdminTool((util.RENSERVERIP, util.RENSERVERPORT))
    asyncore.loop()
