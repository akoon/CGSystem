//tab标识当前页
$('#projectManSysLnk').addClass('active');
$('#myTasksLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化**************************************	
	$('#myTask').treegrid({
		width:	_w - sidebarWidth,  
	    height:	_h - 90, 
	    url:'/ProjectManSys/indexTask/',  
	    //method:'get',
	    idField:'id',
	    treeField:'name',
	    //toolbar: '#projectTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    animate:false,
	    rownumbers:false,
	    columns:[[
	        {title:'id',field:'id',hidden:true},
	        {field:'name',title:'name',width:($(window).width() - sidebarWidth) * 0.1,formatter:onFormatterTask}, 
			{field:'user',title:'user',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'status',title:'status',width:($(window).width() - sidebarWidth) * 0.1}, 
	        {field:'startTime',title:'start time',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'endTime',title:'end time',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'finishTime',title:'Finished Time',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'desc',title:'description',width:($(window).width() - sidebarWidth) * 0.1},
	        //{field:'percent',title:'完成比',sortable:false,width:($(window).width() - sidebarWidth) * 0.04},
	        //{field:'publishStatus',title:'发布状态',sortable:false,width:($(window).width() - sidebarWidth) * 0.04},
	        //{field:'version',title:'版本',sortable:false,width:($(window).width() - sidebarWidth) * 0.04},
	        //{field:'qc',title:'QC',sortable:false,width:25,styler:onQCStyle,formatter:onFormatterQC},
	        //{field:'review_status',title:'审核状态',sortable:false,width:($(window).width() - sidebarWidth) * 0.04}
	    ]],
	    rowStyler:onTaskRowStyle,
	    onLoadSuccess: function (row, data)
		{
			$.each(data, function (i, val) { $('#myTask').treegrid('collapseAll', data[i].id)})
		}
	});
	
	$('#myTask').treegrid('collapseAll');
	
	//任务发布窗口
	$('#projectTaskIssueWin').window({  
	    width:410,  
	    height:480,  
	    title:'Issue',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false
	});
	//任务发布确定按钮
	$('#projectTaskIssueOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//任务发布取消按钮
	$('#projectTaskIssueCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
//**************************************表单验证****************************************

//**************************************Toolbar操作*************************************
	//—--------------修改QC	
$('#myeditQC').tooltip({  
    showEvent: 'click', 
    content: $('<div></div>'),
	onUpdate: function(content){
		content.panel({  
        	width: 100,  
            border: false,  
            title: 'QC Settings',  
            content: '<div style="padding:5px;">\
						<div style="padding:5px 10px">\
							<div><input type="checkbox" id="checkQC" onchange="checkQC()" value="">QC</div>\
						</div>\
					</div>',   
        });  
	},
    onShow: function(){    
    	var row = $('#myTask').treegrid('getSelected');	             	
		var c = document.getElementById("checkQC");
		if(row){			
			if (row.qc=='是'){
				c.checked = true;
			}else{
				c.checked = false;
			};
		}
        var t = $(this);
        t.tooltip('tip').unbind().bind('mouseenter', function(){  
            t.tooltip('show');    
        }).bind('mouseleave', function(){ 
        	 t.tooltip('hide'); 
        });
    }  
});
	//—--------------图片上传	
$('#mytaskImg').tooltip({  
    showEvent: 'click', 
    content: $('<div></div>'),
    position:'right',
	onUpdate: function(content){
		content.panel({  
        	width: 300,  
            border: false,  
            title: 'Upload',  
            content: '<div style="padding:5px;">\
						<div style="padding:5px 10px">\
							<input type="file" name="mytaskImage" id="mytaskImage"> \
						</div>\
						<div style="padding:5px 10px;text-align:center">\
							<a id="mytaskOk" href="#" class="easyui-linkbutton">上传</a>\
							<a id="mytaskCancel" href="#" class="easyui-linkbutton">取消</a>\
						</div>\
					</div>',   
        });  
	},
    onShow: function(){
        var t = $(this);
        t.tooltip('tip').unbind().bind('mouseenter', function(){  
            t.tooltip('show');    
        }).bind('mouseleave', function(){ 
        	//t.tooltip('show'); 
        });        
    	$("#mytaskOk").unbind().bind('click',taskImg);
    	$("#mytaskCancel").unbind().bind('click',function(){t.tooltip('hide');});
    }  
});	
	
});
//**************************************函数**************************************
//任务图片上传
function taskImg(){
	var row = $('#myTask').treegrid('getSelected');
	var file = $("#mytaskImage").val();
	if(!row){
		//$('#mytaskImg').tooltip('hide'); 
		$.messager.show({ 
			height:40,
			msg:'Please select the task to be upload',
			timeout:2000,
			showType:'slide',
			style:{
				right:'',
				top:0,
				bottom:''
			}
		});
	}else{
		var id = row.id;
		var type = id.substring(0,1);
		if (type!='t') {
			$.messager.show({ 
				height:40,
				msg:'Upload denied',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		} else {
			$.ajaxFileUpload({
						url : '/ProjectManSys/projectTaskImg',
						secureuri : false,
						fileElementId : "mytaskImage", // file的id
						dataType : "json",
						data : {
							id : id.substring(1)
						}, // 返回数据类型为文本
						success : function(data, status) {
							if (data.sucess) {
								$('#mytaskImg').tooltip('hide');
								$('#myTask').treegrid('reload');
								$.messager.show({
											height : 40,
											msg : 'upload success',
											timeout : 2000,
											showType : 'slide',
											style : {
												right : '',
												top : 0,
												bottom : ''
											}
										});
		
							}else{
								$.messager.show({
									height:40,
									msg:data.errors,
									timeout:2000,
									showType:'slide',
									style:{
										right:'',
										top:0,
										bottom:''
									}
								});
							}
						}
					});
		}
	}
};
//QC修改
function checkQC(){
	var c = document.getElementById("checkQC");
	var row = $('#myTask').treegrid('getSelected');	 
	if(!row){
		$('#editQC').tooltip('hide'); 
		$.messager.show({ 
			height:40,
			msg:'Please select the data to be edit',
			timeout:2000,
			showType:'slide',
			style:{
				right:'',
				top:0,
				bottom:''
			}
		});
	}else{
		var id = row.id;
		var type = id.substring(0,1);
		if(type=='t'){
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/projectTaskUpdate",
				data : {
					type:'qc',
					id:id.substring(1),
					qc:c.checked,
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");	
					if (json.success){
						if(c.checked){
							qc = '是';
						}else{
							qc = '否';
						}
						$('#myTask').treegrid('update',{
							id: row.id,
							row:{
							qc: qc,
							}
						});	
						$.messager.show({
							height:40,
							msg:'edit success',
							timeout:2000,
							showType:'slide',
							style:{
								right:'',
								top:0,
								bottom:''
							}
						});
					}else{
						$.messager.show({
							height:40,
							msg:json.errors,
							timeout:2000,
							showType:'slide',
							style:{
								right:'',
								top:0,
								bottom:''
							}
						});
					}			 
				}
			});
		}else{
			$.messager.show({ 
				height:40,
				msg:'Edit QC denied',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
		
	}
};
//QC单元格颜色
function onQCStyle(value,row,index){
	var id = row.id;
	var type = id.substring(0,1);
	if(type=='t'){
		if (value=='是'){
			return 'background-color:#009900';
		}else{
			return 'background-color:#999999';
		}
	}	
};
//我的任务行区分
function onTaskRowStyle(row){
	if(row.dis){		
		return 'color:#AAAAAA;';
	}
};
//
function onFormatterQC(value,row,index){
	return '';
};
//我的任务醒目名字连接
function onFormatterTask(value,row,index){
	id = row.id;
	var type = id.substring(0,1);
	if(type=='p'){
		var html = null;
		var id = id.substring(1);
		html = "<a href='/ProjectManSys/"+id+"/'>"+value+"</a>";
		return html	;
	}else{
		if(type=='t'){
			if(row.thum){
				return value+"<a href='"+row.thum+"' class='icon-img' style='margin-left:15px;' target='_blank'></a>"	;
			}else{
				return value;
			}		
		}else{			
			return value;
		}
	}
}
//名称可点击
function onFormatterName(value,row,index){
	id = row.id;
	var type = id.substring(0,1);
	var html = null;
	if (type =='a'){
		var id = id.substring(1);
		html = "<a href='/ProjectManSys/"+id+"/'>"+value+"</a>";
	}else{
		html = value;
	}
	return html;
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#myTask').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#myTask').datagrid('resize');
});

// 显示发布窗口
function onTaskIssueWinOpen(){
	var row = $('#myTask').datagrid('getSelected');
	
	if(row != null && row.id.substring(0,1) == 't'){
		console.log("projectTaskIssueWin");
		$("#issueTaskSelected").html(row.id.substring(1));
		
		//判定是否有权限发布
		$.ajax({
			type: "post",
			url: "/ProjectManSys/issueAuthorized",
			data:
			{
				'taskId'	: $('#issueTaskSelected').html()
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$("#projectTaskIssueWin").window('open');
					$(function() {
						$('#file_upload').uploadify({
							'formData'     : {
								'sessionId' : $('#sessionId').html(),
								'session' : $('#sessionData').html(),
								//'projectId'	: $('#projectId').html(),
								'taskId'	: $('#issueTaskSelected').html()
							},
							'swf'      : '/static/extraneous/uploadify/uploadify.swf',
							'uploader' : '/ProjectManSys/issueFileUpload',//;jsessionid='+$('#sessionId').html(),
							'onQueueComplete' : function(queueData) {
								//所有文件上传成功
								$.ajax({
									type: "post",
									url: "/ProjectManSys/projectTaskIssue",
									data:
									{
										'sessionId' : $('#sessionId').html(),
										//'projectId'	: $('#projectId').html(),
										'taskId'	: $('#issueTaskSelected').html(),
										'fileCount' : queueData.uploadsSuccessful
									},
									datatype : "json",
									success : function(data) {
										var json = eval("(" + data + ")");	
										if (json.success){
											$('#myTask').datagrid('reload');
											$.messager.show({
												height:40,
												msg:'Upload success',
												timeout:2000,
												showType:'slide',
												style:{
													right:'',
													top:0,
													bottom:''
												}
											});
											
										}else{
											$.messager.show({
												height:40,
												msg:"Upload failed"+'\n'+json.msg,
												timeout:2000,
												showType:'slide',
												style:{
													right:'',
													top:0,
													bottom:''
												}
											});
										}
										$("#projectTaskIssueWin").window('close');
									}
								});
								
					            //alert(queueData.uploadsSuccessful + ' files were successfully uploaded.');
					        }
						});
					});
				}
				else
				{
					$.messager.show({
						height:40,
						msg:"Only publish user's own task",
						timeout:2000,
						showType:'slide',
						style:{
							right:'',
							top:0,
							bottom:''
						}
					});
				}			 
			}
		});
		
		
			
	}
	else
	{
		$.messager.show({ 
			height:40,
			msg:'Please select the task to be submitted',
			timeout:2000,
			showType:'slide',
			style:{
				right:'',
				top:0,
				bottom:''
			}
		});
	}
}
