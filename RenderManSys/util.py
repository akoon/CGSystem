# -*- coding: utf-8 -*-
'''
Created on 2013-5-20

@author: hao.yu
'''
import socket, struct, threading, os
import pyDes

#渲染服务器默认IP地址
RENSERVERIP = '172.16.253.246'
#渲染服务器默认端口号
RENSERVERPORT = 44331
#渲染系统登录默认用户名和密码
LOGINNAME = 'admin'
LOGINPASSWD = 12345678
DES_KEY = pyDes.des("DESDYLAN", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad = None, padmode = pyDes.PAD_PKCS5)
#本机ip地址
LOCALIPADDR = None

# LOGINUSERNAME = 'admin'

#用于获取连续的序列 0,1,2,3,4,5,6
class GetID:
    @staticmethod
    def get_id():
        cur_id = 0
        while True:
            yield cur_id
            cur_id += 1

#本机IP地址
if 'posix' == os.name:
    def get_local_ip():
        import fcntl
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', 'eth0'))[20:24])
    global LOCALIPADDR
    LOCALIPADDR = struct.unpack('I', socket.inet_aton(get_local_ip()))[0]
else:
    global LOCALIPADDR
    LOCALIPADDR = struct.unpack('I', socket.inet_aton(socket.gethostbyname(socket.getfqdn(socket.gethostname()))))[0]

#读写锁,多读一写
class RWLock:
    def __init__(self):
        self.__readers = 0
        self.__haswriter = False
        self.__rwcond = threading.Condition()
    
    def read_acquire(self):
        self.__rwcond.acquire()
        self.__readers += 1
        while self.__haswriter:
            self.__rwcond.wait()
        self.__rwcond.release()
    
    def read_release(self):
        self.__rwcond.acquire()
        self.__readers -= 1
        if self.__readers == 0:
            self.__rwcond.notify()
        self.__rwcond.release()
    
    def write_acquire(self):
        self.__rwcond.acquire()
        self.__haswriter = True
        while self.__readers >= 1:
            self.__rwcond.wait()
        self.__rwcond.release()
    
    def write_release(self):
        self.__rwcond.acquire()
        self.__haswriter = False
        self.__rwcond.notifyAll()
        self.__rwcond.release()
        

