# -*- coding: utf-8 -*-
'''
Created on 2013-5-21

@author: hao.yu
'''
import struct
import util

class CmdIds(object):
    getid = util.GetID.get_id()
    cmd_node_register           = getid.next()
    cmd_response_node_register  = getid.next()
    cmd_login                   = getid.next()
    cmd_response_login          = getid.next()
    cmd_node_is_busy            = getid.next()
    cmd_new_node                = getid.next()
    cmd_render_log              = getid.next()
    cmd_sub_render_successed    = getid.next()
    cmd_render_successed        = getid.next()
    cmd_render_nodes            = getid.next()
    cmd_render_task             = getid.next()
    cmd_response_render_task    = getid.next()
    cmd_unprocess_tasks         = getid.next()
    cmd_processing_tasks        = getid.next()
    cmd_processed_tasks         = getid.next()
    cmd_render_task_invalid     = getid.next()
    cmd_node_status_changed     = getid.next()
    cmd_node_working            = getid.next()
    cmd_sub_task_changed        = getid.next()
    cmd_sub_tasks_of_task       = getid.next()
    cmd_sub_task_rerender       = getid.next()
    cmd_sub_task                = getid.next()
    cmd_delete_tasks            = getid.next()
    cmd_tasks_deleted           = getid.next()
    cmd_stop_render_task        = getid.next()
    cmd_derive_task_created     = getid.next()
    cmd_render_hodini_hip       = getid.next()
    cmd_render_ifd              = getid.next()
    cmd_render_maya             = getid.next()
    cmd_render_3dmax            = getid.next()
    cmd_render_calc             = getid.next()
    cmd_stop_rendernode         = getid.next()
    cmd_select_tasks            = getid.next()
    cmd_response_select_tasks   = getid.next()
    cmd_intervention            = getid.next()
    cmd_response_intervention   = getid.next()
    
#根据命令串查找对应的ID
def get_cmd_index(cmd):
    if CmdIds.__dict__.has_key(cmd):
        return CmdIds.__dict__.get(cmd)
    else:
        return -1
    
#定义的报文头的格式和长度
cmd_header_fmt='4I128s2I'
cmd_header_len=struct.calcsize(cmd_header_fmt)
INVALIDE_ID = 0
devtype_admin_tool = 2 #在渲染服务端认为是admintool

#打包二进制数据，以下编写打包各个命令函数
#给命令加上报文头，形成一条完整的命令
def rencmd_mux_cmd(dev_type,cmdid,sender_id,ipv4addr,username,cmd_data,cmd_extra_data):
    global cmd_header_fmt
    #先打包基本数据（标准头）
    cmd_data_len=0
    cmd_extra_data_len=0
    if cmd_data:
        cmd_data_len=len(cmd_data)
    if cmd_extra_data:
        cmd_extra_data_len=len(cmd_extra_data)

    print username
    cmd_buf = struct.pack(cmd_header_fmt,dev_type,cmdid,sender_id,ipv4addr,str(username),cmd_data_len,cmd_extra_data_len)
    if cmd_data:
        cmd_buf+=cmd_data
    if cmd_extra_data:
        cmd_buf+=cmd_extra_data
    return cmd_buf

#形成登录命令
def rencmd_mux_login_cmd(dev_type,cmdid,ipv4addr,user,passwd,len_pwd):
    global INVALIDE_ID    
    #形成私有结构
    fmt="II{0}s{1}sB".format(len(user),len(passwd))
    cmd_buf=struct.pack(fmt,len(user),len(passwd),user,passwd,len_pwd)
    return rencmd_mux_cmd(dev_type,cmdid,INVALIDE_ID,ipv4addr,str(user),cmd_buf,None)

#拆分二进制数据，变成元组，拆解函数都写在以下位置
#分析命令的基本信息（头部）,返回 dev_type,cmd_id,client_id,ipv4addr,cmd_priv_data_len,cmd_param_len
def rencmd_demux_basecmd(cmdbuf):
    global cmd_header_fmt
    return struct.unpack_from(cmd_header_fmt,cmdbuf)

#登录渲染服务器返回
def rencmd_demux_login_response(cmdbuf):
    global cmd_header_len
    return struct.unpack_from('I',cmdbuf,cmd_header_len)[0]

render_node_info_fmt='IIIHIBBBI'
def rencmd_demux_render_node_info(cmd_buf):
    global render_node_info_fmt
    global cmd_header_len
    return struct.unpack_from(render_node_info_fmt,cmd_buf,cmd_header_len)

def cmd_get_node_info_len():
    global render_node_info_fmt
    return struct.calcsize(render_node_info_fmt)  

def rencmd_demux_render_node_info2(cmd_buf,offset):
    global render_node_info_fmt
    global cmd_header_len
    return struct.unpack_from(render_node_info_fmt,cmd_buf,offset)

#获取tasks
#task info/sub task count/sub task info/sub task inf/.../task info/sub task count/sub task info/... ...
def rencmd_demux_tasks(cmd_buf,cmd_data_len,offset):
    sub_fmt='8I'
    sub_info_len=struct.calcsize(sub_fmt)
    max_len = cmd_data_len+offset
    tasks = []
    while offset < max_len:
        sub_tasks = []
        
        username_len = struct.unpack_from('I', cmd_buf, offset)[0]
        offset+=struct.calcsize('I')
        username = struct.unpack_from('{0}s'.format(username_len), cmd_buf, offset)[0]
        offset += username_len
        
        #解出task info
        task_info, offset = rencmd_demux_render_task(cmd_buf, offset)
        #解出sub task count
        sub_count = struct.unpack_from('I',cmd_buf,offset)[0]
        offset += struct.calcsize('I')
        #解出各sub task
        for i in range(sub_count):
            sub_info = struct.unpack_from(sub_fmt, cmd_buf, offset);
            sub_tasks.append(sub_info)
            offset += sub_info_len
        tasks.append((task_info,sub_tasks,username))
    return tasks

#返回task info和cmd_buf中的当前位置
def rencmd_demux_render_task(cmd_buf, offset):
    #需将bytes转换为str
    task_info = []
    #id
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #type
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #ipv4 addr
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #Priority
    item=struct.unpack_from('B',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('B')
    #StartFrame
    item=struct.unpack_from('H',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('H')
    #FrameCount
    item=struct.unpack_from('H',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('H')
    #Step
    item=struct.unpack_from('H',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('H')
    #AddTime
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #RenderStartTime
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #RenderStopTime
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #Group
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #FileType
    item=struct.unpack_from('I',cmd_buf,offset)[0]
    task_info.append(item)
    offset+=struct.calcsize('I')
    #task name len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #task name
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    #RenderName len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #RenderName
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    #ProjFile len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #ProjFile
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    #InputFileName len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #InputFileName
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    #OutputPath len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #OutputPath
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    #Misc len
    length=struct.unpack_from('H',cmd_buf,offset)[0]
    offset+=struct.calcsize('H')
    #Misc
    item=struct.unpack_from('{0}s'.format(length),cmd_buf,offset)[0]
    task_info.append(item.decode('utf-8'))
    offset+=length
    return (task_info,offset)

def rencmd_demux_one_sub_task(cmd_buf,cmd_data_len):
    global cmd_header_len
    fmt='6I'
    return struct.unpack_from(fmt,cmd_buf,cmd_header_len)

#返回{task_id:[(task info..),(task_info...),...],task_id:[(task info..),(task_info...),...],...}
def rencmd_demux_sub_tasks_of_task(cmd_buf,cmd_data_len):
    global cmd_header_len
    fmt='6I'
    sub_tasks={}
    info_len=struct.calcsize(fmt)
    offset=cmd_header_len
    while cmd_data_len+cmd_header_len > offset:
        task_info=struct.unpack_from(fmt, cmd_buf, offset)
        offset+=info_len
        if not task_info[1] in sub_tasks:
            sub_tasks[task_info[1]]=[]
        sub_tasks[task_info[1]].append(task_info)
    return sub_tasks

#node ip + node status
def rencmd_demux_render_node_status(cmd_buf,cmd_data_len):
    global cmd_header_len
    return struct.unpack_from('2I',cmd_buf,cmd_header_len)

def rencmd_demux_sub_render_successed(cmd_buf,cmd_data_len):
    #cmd_data 是 RenderTaskInfo + TaskRenderStat
    global cmd_header_len
    fmt='6I'
    sub_info = struct.unpack_from(fmt,cmd_buf,cmd_header_len)
    render_stat = struct.unpack_from('2I',cmd_buf,cmd_header_len+struct.calcsize(fmt))
    return (sub_info,render_stat)

def rencmd_demux_task_successed(cmd_buf,cmd_data_len):
    global cmd_header_len
    return struct.unpack_from('I',cmd_buf,cmd_header_len)[0]

def rencmd_demux_delete_task_cmd_data(cmd_buf):
    global cmd_header_len
    offset=cmd_header_len
    task_number=struct.unpack_from('I',cmd_buf,cmd_header_len)
    offset+=struct.calcsize('I')
    fmt=task_number[0]*'I'
    task_list=struct.unpack_from(fmt,cmd_buf,offset)
    return task_list

def rencmd_demux_response_new_render_task(cmd_buf):
    global cmd_header_len
    return struct.unpack_from('II', cmd_buf,cmd_header_len)

def rencmd_demux_render_task_invalid(cmd_buf,cmd_data_len):
    global cmd_header_len
    fmt='I{0}s'.format(cmd_data_len-struct.calcsize('I'))
    return struct.unpack_from(fmt, cmd_buf, cmd_header_len)

#形成添加任务命令的数据部分   
def rencmd_mux_add_task_cmd_data(task_id,
                                 type,
                                 OwnerIpv4Addr,
                                 Priority,
                                 StartFrame,
                                 FrameCount,
                                 Step,
                                 AddTime,
                                 RenderStartTime,
                                 RenderStopTime,
                                 Groups,
                                 FileType,
                                 TaskName,
                                 RenderName,
                                 InputPath,
                                 InputFileName,
                                 OutputPath,
                                 Misc):
    
    #打包的方式是，如果是字符串，则先是其长度，后跟随字符串；如果是数字，则都按4字节处理  
    #以=开头是为了防止对齐
    fmt='=IIIBHHHIIIIIH{0}sH{1}sH{2}sH{3}sH{4}sH{5}s'.format(len(TaskName),
                                                 len(RenderName),                                                
                                                 len(InputPath),
                                                 len(InputFileName),
                                                 len(OutputPath),
                                                 len(Misc))
    
    return struct.pack(fmt,
                       task_id,
                       type,
                       OwnerIpv4Addr,
                       Priority,
                       StartFrame,
                       FrameCount,
                       Step,
                       AddTime,
                       RenderStartTime,
                       RenderStopTime,
                       Groups,
                       FileType,
                       len(TaskName),TaskName,
                       len(RenderName),RenderName,
                       len(InputPath),InputPath,
                       len(InputFileName),InputFileName,
                       len(OutputPath),OutputPath,
                       len(Misc),Misc)
