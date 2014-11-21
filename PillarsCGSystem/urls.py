# -*- coding: utf-8 -*-
'''
URL Router文件
'''
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PillarsCGSystem.views.home', name='home'),
    # url(r'^PillarsCGSystem/', include('PillarsCGSystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
     
#      url(r'^admin/', include(admin.site.urls)),
    
    
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#素材管理
urlpatterns += patterns('Initialization.views',
   #返回渲染管理主界面
    url(r'^Initialization/$', 'index'),
    url(r'^Initialization/validate$', 'validate'),
    url(r'^Initialization/0$', 'setup0'),
    url(r'^Initialization/1$', 'setup1'),
    url(r'^Initialization/2$', 'setup2'),
    url(r'^Initialization/3$', 'setup3'),
    
    url(r'^Initialization/skip$', 'initialization_skip'),
    url(r'^Initialization/finished$', 'finished'),
)

#基础功能子系统URL
urlpatterns += patterns('BaseSys.views',   
    
    url(r'^$', 'app'),
    
    url(r'^BaseSys/$', 'index'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^changepasswd/$', 'change_passwd'),
    
    #基础管理
    url(r'^BaseSys/department/$', 'department'),#部门管理
    url(r'^BaseSys/position/$', 'position'),#职位管理  
    url(r'^BaseSys/people/$', 'people'),#人员管理
    url(r'^BaseSys/permissions/$', 'permissions'),#人员管理
)

urlpatterns += patterns('BaseSys.views_ajax',   
    
    #部门管理
    url(r'^BaseSys/departmentRead/(?P<index>\w*)$', 'department_read'),
    url(r'^BaseSys/departmentDetail/$', 'department_detail'),
    url(r'^BaseSys/departmentCreate$', 'department_create'),
    url(r'^BaseSys/departmentUpdate$', 'department_update'),
    url(r'^BaseSys/departmentDestroy$', 'department_destroy'),
    #职位管理
    url(r'^BaseSys/positionRead/(?P<index>\w*)$', 'position_read'),
    url(r'^BaseSys/positionDetail/$', 'position_detail'),
    url(r'^BaseSys/positionCreate$', 'position_create'),
    url(r'^BaseSys/positionUpdate$', 'position_update'),
    url(r'^BaseSys/positionDestroy$', 'position_destroy'),
    #用户管理
    url(r'^BaseSys/peopleRead/(?P<index>\w*)$', 'people_read'),
    url(r'^BaseSys/peopleDetail/$', 'people_detail'),
    url(r'^BaseSys/peopleCreate$', 'people_create'),
    url(r'^BaseSys/peopleUpdate$', 'people_update'),
    url(r'^BaseSys/peopleDestroy$', 'people_destroy'),
    url(r'^BaseSys/peopleImg$', 'people_img'),
    #邮件相关
    url(r'^BaseSys/sendMail$', 'send_mail'),
    #系统环境
    url(r'^BaseSys/systemenvironmentdetail/$', 'systemenvironment_detail'),
    
    #提交反馈
    url(r'^report/$', 'report'),
    url(r'^myReport/$', 'my_report'),
    
)

#任务管理子系统URL
urlpatterns += patterns('ProjectManSys.views',   
    
#     url(r'^$', 'main'),
    url(r'^ProjectManSys/$', 'index'),
    url(r'^ProjectManSysProjectlist/$', 'index_projectlist'),
    url(r'^ProjectManSys/status/$', 'status'),
    url(r'^ProjectManSys/types/$', 'types'),
    url(r'^ProjectManSys/group/$', 'group'),
    url(r'^ProjectManSys/templ/$', 'templ'),
    url(r'^ProjectManSys/gantt/(?P<proj>\d*)/$', 'gantt'),
    
    #每个项目相关显示
    url(r'^ProjectManSys/(?P<index>\d*)/$', 'project_index'),
    url(r'^ProjectManSys/(?P<index>\d*)/group/$', 'project_group'),
    url(r'^ProjectManSys/(?P<index>\d*)/people/$', 'project_people'),
    url(r'^ProjectManSys/(?P<index>\d*)/task/$', 'project_task'),
    url(r'^ProjectManSys/(?P<index>\d*)/gantt/$', 'project_gantt'),
    url(r'^ProjectManSys/(?P<index>\d*)/notes/$', 'project_notes'),
    url(r'^ProjectManSys/(?P<index>\d*)/rel/$', 'project_rel'),
    url(r'^ProjectManSys/(?P<index>\d*)/performance/$', 'project_performance'),
    
)

urlpatterns += patterns('ProjectManSys.views_ajax',
    #状态管理
    url(r'^ProjectManSys/statusRead/(?P<index>\w*)$', 'status_read'),
    url(r'^ProjectManSys/statusDetail/$', 'status_detail'),
    url(r'^ProjectManSys/statusCreate/$', 'status_create'),
    url(r'^ProjectManSys/statusUpdate$', 'status_update'),
    url(r'^ProjectManSys/statusDestroy$', 'status_destroy'),
    #类型管理
    url(r'^ProjectManSys/typesRead/(?P<index>\w*)$', 'types_read'),
    url(r'^ProjectManSys/typesDetail/$', 'types_detail'),
    url(r'^ProjectManSys/typesCreate/$', 'types_create'),
    url(r'^ProjectManSys/typesDestroy$', 'types_destroy'),
    url(r'^ProjectManSys/typesUpdate$', 'types_update'),
    #组管理
    url(r'^ProjectManSys/groupRead/(?P<index>\w*)$', 'group_read'),
    url(r'^ProjectManSys/groupDetail/$', 'group_detail'),
    url(r'^ProjectManSys/groupCreate/$', 'group_create'),
    url(r'^ProjectManSys/groupDestroy/$', 'group_destroy'),
    url(r'^ProjectManSys/groupUpdate/$', 'group_update'),
    #模板管理
    url(r'^ProjectManSys/templRead/(?P<index>\w*)$', 'templ_read'),
    url(r'^ProjectManSys/templDetail/$', 'templ_detail'),
    url(r'^ProjectManSys/templCreate/$', 'templ_create'),
    url(r'^ProjectManSys/templDestroy/$', 'templ_destroy'),
    url(r'^ProjectManSys/templUpdate/$', 'templ_update'),
    #项目管理
    url(r'^ProjectManSys/projectRead/(?P<index>\w*)$', 'project_read'),
    url(r'^ProjectManSys/projectDetail/$', 'project_detail'),
    url(r'^ProjectManSys/projectCreate/$', 'project_create'),    
    url(r'^ProjectManSys/projectDestroy', 'project_destroy'),
    url(r'^ProjectManSys/projectUpdate/$', 'project_update'),
     url(r'^ProjectManSys/projectImg', 'project_img'),
    #资产管理
    url(r'^ProjectManSys/taskGroupRead/(?P<index>\w*)$', 'taskGroup_read'),
    url(r'^ProjectManSys/taskGroupDetail/$', 'taskGroup_detail'),
    url(r'^ProjectManSys/taskGroupCreate$', 'taskGroup_create'),
    url(r'^ProjectManSys/taskGroupDestroy$', 'taskGroup_destroy'),
    url(r'^ProjectManSys/taskGroupUpdate$', 'taskGroup_update'),
    url(r'^ProjectManSys/taskGroupImg$', 'taskGroup_img'),
    
    #项目人员管理
    url(r'^ProjectManSys/projectPeopleRead/(?P<index>\w*)$', 'projectPeople_read'),
    url(r'^ProjectManSys/projectPeopleDetail/', 'projectPeople_detail'),
    url(r'^ProjectManSys/projectPeopleCreate$', 'projectPeople_create'),
    url(r'^ProjectManSys/projectPeopleUpdate$', 'projectPeople_update'),
    url(r'^ProjectManSys/projectPeopleDestroy$', 'projectPeople_destroy'),
    
    #项目效率管理
    url(r'^ProjectManSys/projectPerformanceDetail/', 'projectPerformance_detail'),
    
    #项目任务管理
    url(r'^ProjectManSys/projectTaskRead/(?P<index>\w*)$', 'projectTask_read'),
    url(r'^ProjectManSys/projectTaskDetail/', 'projectTask_detail'),
    url(r'^ProjectManSys/projectTaskCreate$', 'projectTask_create'),
    url(r'^ProjectManSys/projectTaskDestroy$', 'projectTask_destroy'),    
    url(r'^ProjectManSys/projectTaskUpdate$', 'projectTask_update'),
    url(r'^ProjectManSys/projectTaskImg$', 'projectTask_img'),
    url(r'^ProjectManSys/issueFileUpload$', 'issueFileUpload'),
    url(r'^ProjectManSys/projectTaskIssue$', 'projectTask_issue'),
    url(r'^ProjectManSys/issueAuthorized$', 'issue_authorized'),
    
    url(r'^ProjectManSys/projectTaskDlTaskgroup/', 'projectTaskDl_taskgroup'),
    url(r'^ProjectManSys/projectTaskDlDetail/', 'projectTaskDl_detail'),
    
    #主页--项目
    url(r'^ProjectManSys/indexProject/', 'index_project'),
    #主页--我的任务
    url(r'^ProjectManSys/indexTask/', 'index_task'),
    #主页--甘特图
    url(r'^get_gantt_tasks/$', 'get_gantt_tasks'),
    url(r'^gantt_projlist/$', 'gantt_projlist'),
    
    #主页--项目汇总
    url(r'^ProjectManSys/project_summary/$', 'project_summary'),
    #主页--个人汇总
    url(r'^ProjectManSys/project_user_summary/$', 'project_user_summary'),
    
    #任务审核管理
    url(r'^ProjectManSys/notesGrouplist/$', 'notes_grouplist'),
    url(r'^ProjectManSys/notesTasklist/$', 'notes_tasklist'),
    url(r'^ProjectManSys/notesTaskDetails/$', 'notes_taskdetails'),
    url(r'^ProjectManSys/notesDetail/$', 'note_detail'),
    url(r'^ProjectManSys/notesCreate/$', 'note_create'),
    url(r'^ProjectManSys/imageUpload/$', 'image_upload'),
    
    #资产关联
    url(r'^ProjectManSys/taskGroupTree/(?P<index>[^/]+)$', 'taskGroup_tree'),
    url(r'^ProjectManSys/taskGroupTreeRelateable/(?P<proj>[^/]+)/(?P<src_tg>[^/]+)$', 'taskGroup_tree_relateable'),
    
    url(r'^ProjectManSys/srcTaskGroupRead/$', 'srcTaskGroup_read'),
    url(r'^ProjectManSys/descTaskGroupDetail/$', 'descTaskGroup_detail'),
    url(r'^ProjectManSys/descTaskGroupRead/(?P<id>[^/]+)$', 'descTaskGroup_read'),
    url(r'^ProjectManSys/descTaskGroupCreate/$', 'descTaskGroup_create'),
    url(r'^ProjectManSys/descTaskGroupDestroy/$', 'descTaskGroup_destroy'),
    
    #项目管理系统数据迁移
    #url(r'^ProjectManSys/data_transfer','data_transfer'),
    url(r'^ProjectManSys/task_test','task_test'),
    
)

#Timesheet子系统URL
urlpatterns += patterns('TimeSheetSys.views',
    url(r'^TimeSheetSys/$', 'index'),
    
    url(r'^TimeSheetSys/timesheet/$', 'timesheet'),
    url(r'^TimeSheetSys/timesheet_viewmode/$', 'timesheet_viewmode'),
    url(r'^TimeSheetSys/timesheet_viewedit/$', 'timesheet_viewedit'),
    
    #审核用户列表页面
    url(r'^TimeSheetSys/timesheet_users/$', 'timesheet_users'),
    
    #报表页面
    url(r'^TimeSheetSys/report/$', 'timesheet_report'),
    
    #统计页面
    url(r'^TimeSheetSys/statistic/$', 'timesheet_statistic'),
    url(r'^TimeSheetSys/taskStatistic/$', 'timesheet_taskstatistic'),
)

urlpatterns += patterns('TimeSheetSys.views_ajax',
                        
    url(r'^TimeSheetSys/adminlist/$', 'adminlist'),
    
    #Timesheet审核用户列表
    url(r'^TimeSheetSys/tsusersDetail/$', 'tsusers_detail'),
    
    #Timesheet相关
    url(r'^get_user_tasks/(?P<uid>[^/]+)/$','get_user_tasks'),
    url(r'^get_user_tasks_combo/(?P<uid>[^/]+)/$','get_user_tasks_combo'),
    
    url(r'^add_actual_task/(?P<uid>[^/]+)$','add_actual_task'),
    url(r'^update_actual_task/(?P<uid>[^/]+)$','update_actual_task'),
    url(r'^remove_actual_task/(?P<uid>[^/]+)$','remove_actual_task'),
    url(r'^get_actual_tasks/(?P<uid>[^/]+)$','get_actual_tasks'),

    url(r'^get_actual_daily_status','get_actual_daily_status'),
    url(r'^get_actual_daily_passed','get_actual_daily_passed'),
    url(r'^get_actual_status','get_actual_status'),
    url(r'^get_actual_daily_month/(?P<uid>[^/]+)$','get_actual_daily_month'),
    
    #timesheet 提交
    url(r'^confirm_actual_tasks$','confirm_actual_tasks'),
    url(r'^applychange_actual_tasks$','applychange_actual_tasks'),
    url(r'^restore_daily_status','restore_daily_status'),
    
    #timesheet审核
    url(r'^timesheet_judge','timesheet_judge'),
    
    #timesheet报表显示
    url(r'^TimeSheetSys/reportDetail/','report_detail'),
    
    #timesheet统计
    url(r'^TimeSheetSys/statisticDetail/','statistic_detail'),
    url(r'^TimeSheetSys/taskStatisticDetail/','taskStatistic_detail'),
    
    #timesheet数据迁移
    #url(r'^TimeSheetSys/data_transfer','data_transfer'),
    url(r'^TimeSheetSys/comfirm_change','comfirm_change'),
)

#日历子系统
urlpatterns += patterns('CalendarSys.views',
    url(r'^CalendarSys/$', 'calendar'),
    
)

urlpatterns += patterns('CalendarSys.views_ajax',
    
    url(r'^TimeSheetSys/getScheduleTasks/(?P<uid>[^/]+)$', 'get_schedule_tasks'),
    url(r'^TimeSheetSys/addScheduleTasks/(?P<uid>[^/]+)$', 'add_schedule_tasks'),
    url(r'^TimeSheetSys/UpdateScheduleTasks/(?P<uid>[^/]+)$', 'update_schedule_task'),
    url(r'^TimeSheetSys/RemoveScheduleTasks/(?P<uid>[^/]+)$', 'remove_schedule_task'),
    #日历状态列表
    url(r'^TimeSheetSys/getScheduleStatus/$', 'get_schedule_status'),
    
    url(r'^CalendarSys/get_user_combo/$', 'get_user_combo'),
    
)

#OA子系统URL
urlpatterns += patterns('OASys.views',
    #我的请假
    url(r'^OASys/$', 'leave'),
    #归档
    url(r'^OASys/leaveArchive/$', 'leave_archive'),
    
)

urlpatterns += patterns('OASys.views_ajax',   
    #假条查询
    url(r'^OASys/leaveDetail/$', 'leave_detail'),
    #请假类型查询
    url(r'^OASys/leavetypeRead/$', 'leavetype_read'),
    #创建假条
    url(r'^OASys/leaveCreate/$', 'leave_create'),
    #提交假条
    url(r'^OASys/leaveCommit/$', 'leave_commit'),
    #提交假条
    url(r'^OASys/leaveJudge/$', 'leave_judge'),
    #归档假条
    url(r'^OASys/archivedLeave/$', 'archived_leave'),
    #修改假条
    url(r'^OASys/leaveUpdate/$', 'leave_update'),
    #修改假条
    url(r'^OASys/leaveDestroy/$', 'leave_destroy'),
    
)

#webService接口
urlpatterns += patterns('InterfaceSys.views',

    #人员获取
    url(r'^InterfaceSys/peopleRead/$', 'people_read'),
    #获取项目
    url(r'^InterfaceSys/projectRead/$', 'project_read'),
    #获取资产
    url(r'^InterfaceSys/assetRead/$', 'asset_read'),
    #获取任务
    url(r'^InterfaceSys/taskRead/$', 'task_read'),
    #获取
    url(r'^InterfaceSys/allRead/(?P<index>\w*)$', 'all_read'),
    #资产发布
    url(r'^InterfaceSys/publishTask/$', 'publish_task'),
    #文件复制
    url(r'^InterfaceSys/onlyCopy/$', 'copy_file'),
)


#渲染系统
#请求页面
urlpatterns += patterns('RenderManSys.views',
   #返回渲染管理主界面
   url(r'^RenderManSys/$', 'render_admintool_index'),
   #返回运维工具界面
   url(r'^RenderManSys/operatetool/$', 'render_operate_tool'),
)
#渲染系统ajax接口
urlpatterns += patterns('RenderManSys.views_ajax',
   #改变链接的渲染服务器 
   url(r'^RenderManSys/connectRenderServer/$', 'connect_render_server'),
   #取admintool链接是否成功
   url(r'^RenderManSys/getConnectStatus/$', 'get_connect_status'),
   #获取所有的渲染节点
   url(r'^RenderManSys/getRenderNodes/$', 'get_render_nodes'),
   #获取所有的渲染任务
   url(r'^RenderManSys/getRenderTasks/$', 'get_render_tasks'),
   #提交的渲染命令
   url(r'^RenderManSys/putRenderCmd/$', 'put_process_cmd'),
   #提交渲染任务
   url(r'^RenderManSys/putRenderTask/$', 'put_render_task'),
   #获取文件树
   url(r'^RenderManSys/getFileTree/$', 'get_file_tree'),
)

#素材管理
urlpatterns += patterns('MaterialManSys.views',
   #返回渲染管理主界面
    url(r'^MaterialManSys/$', 'index'),
)

urlpatterns += patterns('ContactSys.views',
   #返回渲染管理主界面
    url(r'^ContactSys/$', 'index'),
)

urlpatterns += patterns('ContactSys.views_ajax',
   #返回渲染管理主界面
    url(r'^ContactSys/people$', 'people_detail'),
)