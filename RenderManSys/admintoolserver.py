# -*- coding: utf-8 -*-
'''
Created on 2013-5-20

@author: hao.yu
'''
import threading, asyncore
import util
from admintool import AdminTool

class AdminToolSvr(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.__admintools = {}
        #用于同步__admintools
        self.__synadmintools = threading.Condition()
    
    #如果没有链接此渲染服务器的admintool则新建一个然后保存在admintools里
    def create_admintool(self, address):
        self.__synadmintools.acquire()
        #如果没有则建立
        if not self.__admintools.has_key(address[0]):
            at = AdminTool(address)
            self.__admintools[address[0]] = at
            self.__synadmintools.notifyAll()
        #如果有但是没有登录成功，先把之前的admintool删除，然后重新新建。
        elif self.__admintools.get(address[0]).loginstatus != AdminTool.status_login_ok:
            self.__admintools.pop(address[0])
            at = AdminTool(address)
            self.__admintools[address[0]] = at
            self.__synadmintools.notifyAll()
        self.__synadmintools.release()
    
    #如果admintools里面有此admintool则删除之，没有的话什么都不做
    def delete_admintool(self, address):
        self.__synadmintools.acquire()
        if self.__admintools.has_key(address[0]):
            self.__admintools.pop(address[0])
        self.__synadmintools.release()   
    
    #在前台界面首此请求，并发送完链接的渲染服务器地址,该如何同步登录状态呢？
    def connect_render_server(self, address = (util.RENSERVERIP, util.RENSERVERPORT)):
        self.create_admintool(address)
        return 1
    
    def get_connect_status(self, address = (util.RENSERVERIP, util.RENSERVERPORT)):
        loginstatus = self.__admintools[address[0]].get_login_status()
        return loginstatus
     
    def insert_process_cmd(self, cmds, username = 'admin', address = (util.RENSERVERIP, util.RENSERVERPORT)):
        return self.__admintools.get(address[0]).store_send_data(cmds, username)
    
    def request_rennodes(self, address):
        return self.__admintools.get(address[0]).get_render_nodes()
    
    def request_rentasks(self, address):
        return self.__admintools.get(address[0]).get_render_tasks()
    
    def request_rensubtasks(self):
        pass
    
    def request_reninfos(self):
        pass
    
    def request_all_element(self):
        pass
        
    def run(self):
        while True:
            self.__synadmintools.acquire()
            while len(self.__admintools) <= 0:
                self.__synadmintools.wait()
            self.__synadmintools.release()   
            asyncore.loop()
            
if __name__ == '__main__':
    ats = AdminToolSvr()
    ats.start()
    ats.connect_render_server(('172.16.253.201', 44331))
