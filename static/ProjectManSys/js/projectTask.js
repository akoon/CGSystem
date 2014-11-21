//tab标识当前页
$('#projectTaskLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化**************************************
	
	$(".task-review .content").css({
	    height:_h - 205, 
	});
	
	$(".task-review .chat-body").css({
        height:_h - 365, 
    });
	
	//组信息表格	
	$('#projectTask').datagrid({
		width:	_w - sidebarWidth,  
	    height:	_h - 100, 
	    url:'/ProjectManSys/projectTaskDetail/',  
	    //method:'get',
	    idField:'id', 
	    autoRowHeight: true,
	    striped:true,
	    //scrollbarSize: 400,
	    rownumbers:false,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},
	        {field:'thum',title:'Thumb',formatter:onTaskThumbImg}, 
	        {title:'taskGroup',field:'taskGroup',hidden:true},
	        {field:'name',title:'Name',sortable:true,width:_w * 0.05,editor:'text',formatter:onFormatterName}, 
	        {field:'status',title:'Status',sortable:true,width:_w * 0.04,
				editor:{
	        		type:'combobox',
	        		options:{ 
	        			panelHeight:'auto',
	        			method:'get',
	        			valueField:'id',
	        			textField:'name',
	        			editable : false,
	        			url:'/ProjectManSys/statusRead/3',
	        		}
	        	}},
	        // {field:'type',title:'类型',sortable:true,width:300,
	       		// editor:{
	        		// type:'combobox',
	        		// options:{ 
	        			// panelHeight:'auto',
	        			// method:'get',
	        			// valueField:'id',
	        			// textField:'name',
	        			// url:'/ProjectManSys/typesRead/3',
	        			// required:true 
	        		// }
	        	// }},
	        {field:'user',title:'User',sortable:true,width:_w * 0.05,
	        	editor:{
	        		type:'combobox',
	        		options:{ 
	        			valueField:'id',
	        			textField:'name',
	        			//multiple: true,
	        			editable : false,
	        			panelHeight:158,
	        		}
	        	}},
	        {field:'startTime',title:'Start Time',sortable:true,editable:false,editor:'datebox',width:_w * 0.05},
	        {field:'endTime',title:'End Time',sortable:true,editable:false,editor:'datebox',width:_w * 0.05},
	        {field:'finishTime',title:'Finished Time',sortable:true,editable:false,editor:'datebox',width:_w * 0.05},
	        {field:'useTime',title:'Scheduled Time',sortable:true,editor:'text',width:_w * 0.05}, 
	        {field:'desc',title:'Description',sortable:false,editor:'text',width:_w * 0.2},
	        {field:'percent',title:'Percent',sortable:false,editable:false,width:_w * 0.04,
	        editor:{
	        		type:'combobox',
	        		options:{
	        			valueField:'value',
	        			textField:'label',
	        			data: [{
							label: '0',
							value: 0
						},{
							label: '10',
							value: 10
						},{
							label: '20',
							value: 20
						},{
							label: '30',
							value: 30
						},{
							label: '40',
							value: 40
						},{
							label: '50',
							value: 50
						},{
							label: '60',
							value: 60
						},{
							label: '70',
							value: 70
						},{
							label: '80',
							value: 80
						},{
							label: '90',
							value: 90
						},{
							label: '100',
							value: 100
						}]
	        		}
	        		
	        	}}  
	        //{field:'publishStatus',title:'发布状态',sortable:false,width:_w * 0.04},  
	        //{field:'version',title:'版本',sortable:false,width:_w * 0.05},   
	        //{field:'qc',title:'QC',sortable:false,width:_w * 0.02},
	        //{field:'reviewStatus',title:'审核状态',sortable:false,width:_w * 0.04}
		]],
		queryParams: {
			projectId:$('#projectId').html()
		}, 
		collapsible:false,
		fitColumns:true,
		view:groupview,  
        groupField:'taskGroup',  
        groupFormatter:function(value,rows){  
        	return value + ' - '+ 'Item('+rows.length+')';  
        },
        onDblClickRow:onDblClickRow,
    	onClickRow:onClickRow,
    	// onRowContextMenu: onRowContextMenu,
	});
	
	//组添加窗口
	$('#projectTaskAddWin').window({  
	    width:320,  
	    height:250,  
	    title:'Add',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onprojectTaskAddOpen   
	});
	//组添加确定按钮
	$('#projectTaskCom').combotree({  
		panelHeight:200,
	});
	//组添加确定按钮
	$('#projectTaskAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//组添加取消按钮
	$('#projectTaskAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//任务发布窗口
	$('#projectTaskIssueWin').window({  
	    width:410,  
	    height:480,  
	    title:'Task Issue',
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
	
	//**************************************表单验证******************************************
	$('.projectTaskName').validatebox({  
    	required: true
	}); 

	//**************************************Toolbar操作**************************************
	//—--------------审核	
$('#projectTaskReview').tooltip({  
    showEvent: 'click', 
    content: $('<div></div>'),
	onUpdate: function(content){
		content.panel({  
        	width: 180,  
            border: false,  
            title: 'Audit',  
            content: '<div style="padding:5px;">\
						<div style="padding:5px 10px">\
							<div><input type="radio"  name="review" value="0">Not Issued</div>\
						</div>\
						<div style="padding:5px 10px">\
							<div><input type="radio"  name="review" value="1">Issued</div>\
						</div>\
						<div style="padding:5px 10px">\
							<div><input type="radio"  name="review" value="2">Passed</div>\
						</div>\
						<div style="padding:5px 10px">\
							<div><input type="radio"  name="review" value="3">Not Passed</div>\
						</div>\
						<div style="padding:5px 10px;text-align:center">\
							<a id="reviewOk" href="#" class="easyui-linkbutton">OK</a>\
							<a id="reviewCancel" href="#" class="easyui-linkbutton">Cancel</a>\
						</div>\
					</div>',   
        });  
	},
    onShow: function(){  
        var t = $(this)  
        t.tooltip('tip').unbind().bind('mouseenter', function(){  
            t.tooltip('show');    
        }).bind('mouseleave', function(){ 
        	//t.tooltip('hide'); 
        }); 
        $('#reviewOk').unbind().bind('click',taskReview);
        $('#reviewCancel').unbind().bind('click',function(){t.tooltip('hide');});
    }  
});
	//—--------------修改QC	
$('#editQC').tooltip({  
    showEvent: 'click', 
    content: $('<div></div>'),
	onUpdate: function(content){
		content.panel({  
        	width: 100,  
            border: false,  
            title: 'QC Setting',  
            content: '<div style="padding:5px;">\
						<div style="padding:5px 10px">\
							<div><input type="checkbox" id="checkQC" onchange="checkQC()" value="">QC</div>\
						</div>\
					</div>',   
        });  
	},
    onShow: function(){    
    	var row = $('#projectTask').datagrid('getSelected');
    	if(row){
    		var c = document.getElementById("checkQC")
    		if (row.qc=='是'){
    			c.checked = true
    		}else{
    			c.checked = false
    		};
            var t = $(this)
            t.tooltip('tip').unbind().bind('mouseenter', function(){  
                t.tooltip('show');    
            }).bind('mouseleave', function(){ 
            	 t.tooltip('hide'); 
            });
    	}else{
    		$.messager.show({ 
    			height:40,
    			msg:'Please select the status you want to modify',
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
	//—--------------发布任务图片	
$('#taskImg').tooltip({  
    showEvent: 'click', 
    content: $('<div></div>'),
	onUpdate: function(content){
		content.panel({  
        	width: 300,  
            border: false,  
            title: 'Upload',  
            content: '<div>\
						<div>\
							<input type="file" name="mytaskImage" id="mytaskImage"> \
						</div>\
						<div style="padding:5px 10px;text-align:center">\
							<a id="taskOk" href="#" class="easyui-linkbutton">上传</a>\
							<a id="taskCancel" href="#" class="easyui-linkbutton">取消</a>\
						</div>\
					</div>',   
        });  
	},
    onShow: function(){  
        var t = $(this)  
        t.tooltip('tip').unbind().bind('mouseenter', function(){  
            t.tooltip('show');    
        }).bind('mouseleave', function(){ 
        	// t.tooltip('hide'); 
        }); 
        $("#taskOk").unbind().bind('click',taskImg);
    	$("#taskCancel").unbind().bind('click',function(){t.tooltip('hide');});
    }  
});
	//—--------------添加行
	$('#projectTaskAdd').click( function() {			
		$('#projectTaskAddWin').window('open');
	});
	$('#projectTaskAddCancel').click( function() {
		$('#projectTaskAddWin').window('close');
	});
	$('#projectTaskAddOk').click( function() {
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectTaskCreate",
			data : {
				projectId:$('#projectId').html(),
				taskGroup:$('#projectTaskCom').combotree('getValue'),
				name:$('#newName').val(),
				desc:$('#newDesc').val()				
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");				 
				if (json.success){
					$('#projectTaskAddWin').window('close');
					$('#projectTask').datagrid('reload');
					$.messager.show({
						height:40,
						msg:json.message,
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
						msg:json.message,
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
		
    } );
    
	//—--------------修改行
				//单击修改最后
	//—--------------删除行 
	$('#projectTaskDelete').click( function() {  		
		var row = $('#projectTask').datagrid('getSelected');
		if(row){
			$.messager.confirm('Delete', 'Are you sure you want to delete this item？', function(r){
				if (r){
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/projectTaskDestroy",
						data : {
							id :row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#projectTask').datagrid('reload');
								$('#projectTask').datagrid('unselectAll');
								$.messager.show({
									height:40,
									msg:'Delete success',
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
				}
			});
			
		}else{
			$.messager.show({ 
				height:40,
				msg:'Please select the data to be deleted',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
	});
	
	//在线编辑器初始化
	KindEditor.ready(function(K) {
		editor = K.create('#note-content',{
			uploadJson : '/ProjectManSys/imageUpload/',
			//fileManagerJson : '/ProjectManSys/imageUpload/',
			extraFileUploadParams : {
	        	task : $("#task-id").html()
	    	},
	    	//编辑器工具栏
	    	items : [ 'fontname', 'fontsize','bold', 'italic', 'underline', 'emoticons', 'image', 'hr', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist', 'insertunorderedlist',  'preview','fullscreen', ]
	    	
		});
		//console.log(editor);
			
	    });
	
	//提交审核信息
	$(".reply-button").click(function(){
		$(".left-messages").toggleClass("slow");
		// $(".left-messages").slideToggle();
		
		editor.sync();
		var con = $("#note-content").val();
		var task = $("#taskId").val();
		
		if(con == null || con == '')
		{
			$.messager.show({ 
				height:40,
				msg:'Issue data cannot be empty',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
		else
		{
			$.ajax({
				type : "post",
				url : "/ProjectManSys/notesCreate/",
				datatype : "json",
				data: {
					task : task,
					content : con
				}, 
				success: function(data){
					//清空编辑器
					editor.text('');
					//刷新审核列表
					notesLoad(task);
					
				}
			});
		}
	});

});

//**************************************函数**************************************

//任务缩略图显示
function onTaskThumbImg(value,rowData,rowIndex){
	if (rowData.thum) {
		return '<img id="peopleImg" class="thum" src="' + rowData.thum+ '" style="height:50px;">'
	} else {
		return '<img id="peopleImg" class="thum" src="/static/pillars/img/unload.jpg" style="height:50px;">'		
	}
};

//
function onFormatterName(value,row,index){
	if(row.thum){
		return value+"<a href='"+row.thum+"' class='icon-img' style='margin-left:15px;' target='_blank'></a>"	
	}else{
		return value
	}		
}
function taskReview(){
	l = document.getElementsByName("review");
	var c = null
	for(var i=l.length;i--;){
	    if(l[i].checked){
	      	c = l[i].value
	    }
	};
	if (!c){
		$.messager.show({ 
			height:40,
			msg:'Please select the state you want to modify',
			timeout:2000,
			showType:'slide',
			style:{
				right:'',
				top:0,
				bottom:''
			}
		});
		return false
	}
	var row = $('#projectTask').datagrid('getSelected');
	if(!row){
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
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectTaskUpdate",
			data : {
				type:'review',
				id:row.id,
				review:c,
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$('#projectTaskReview').tooltip('hide');
					var rowIndex = $('#projectTask').datagrid('getRowIndex',row);
					if(c==0){ct = 'Issued';}
					else if(c==1){ct = 'Not Issued';}
					else if(c==2){ct = 'Passed';}
					else if(c==3){ct = 'Not Passed';}
					$('#projectTask').datagrid('updateRow',{
						index: rowIndex,
						row:{
						reviewStatus: ct,
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
	}
};
//任务图片上传
function taskImg(){
	var row = $('#projectTask').datagrid('getSelected');
	var file = $("#mytaskImage").val();
	if(!row){
		//$('#taskImg').tooltip('hide'); 
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
		$.ajaxFileUpload({
			url : '/ProjectManSys/projectTaskImg',
			secureuri : false,
			fileElementId : "mytaskImage", // file的id
			dataType : "json",
			data : {
				id : row.id
			}, // 返回数据类型为文本
			success : function(data, status) {
				if (data.sucess) {
					$('#taskImg').tooltip('hide');
					$('#projectTask').datagrid('reload');
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
		})
	}
};
//修改QC
function checkQC(){
	var c = document.getElementById("checkQC");
	var row = $('#projectTask').datagrid('getSelected');
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
	$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectTaskUpdate",
			data : {
				type:'qc',
				id:row.id,
				qc:c.checked,
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					var rowIndex = $('#projectTask').datagrid('getRowIndex',row);
					if(c.checked){
						qc = '是'
					}else{
						qc = '否'
					}
					$('#projectTask').datagrid('updateRow',{
						index: rowIndex,
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
	}
};
//组添加窗口打开
function onprojectTaskAddOpen(){
	$('#newName').val('');
	$('#newDesc').val('');
	//$('#projectTaskCom').combotree('reload',"/ProjectManSys/taskGroupRead/")
	$.ajax({
		type : "POST",
		url : "/ProjectManSys/taskGroupRead/",
		data : {
			projectId:$('#projectId').html()				
		},
		datatype : "json",
		success : function(data) {
			var json = eval("(" + data + ")");
			$('#projectTaskCom').combotree('loadData',json);
		}
	});
};

//组修改窗口打开
function onprojectTaskUpdateOpen(){
	var row = $('#projectTask').datagrid('getSelected');
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
};

//正在编辑的表格
var editIndex = undefined;
//单击表格行事件
function onClickRow(rowIndex, field, value){
	if(editIndex != rowIndex){
		endEditing();
	}
	var row = $('#projectTask').datagrid('getSelected');
	$("#taskId").val(row.id);
	notesLoad(row.id);
};

function onEditBtClickRow(){
	var row = $('#projectTask').datagrid('getSelected');
	rowIndex = $('#projectTask').datagrid('getRowIndex',row);
	// row.beginEdit();
	
	if(editIndex != rowIndex){
		if (editIndex == undefined){
			if (endEditing()){
				$('#projectTask').datagrid('selectRow', rowIndex);
				$('#projectTask').datagrid('beginEdit', rowIndex);
				editIndex = rowIndex;	
				$.ajax({
					type : "POST",
					url : "/ProjectManSys/projectPeopleRead/",
					data : {
						projectId:$('#projectId').html()				
					},
					datatype : "json",
					success : function(data) {
						var json = eval("(" + data + ")");
						var eds = $('#projectTask').datagrid('getEditors', editIndex);
						$(eds[2].target).combobox('loadData',json);
					}
				});
			}		 
		}else{
			$('#projectTask').datagrid('selectRow', editIndex);
		}		
	}
	
}

//双击表格行事件
function onDblClickRow(rowIndex, field, value){
	if($('#has_op').val()=='False'){
		return;
	}
	if(editIndex != rowIndex){
		if (editIndex == undefined){
			if (endEditing()){
				$('#projectTask').datagrid('selectRow', rowIndex);
				$('#projectTask').datagrid('beginEdit', rowIndex);
				editIndex = rowIndex;	
				$.ajax({
					type : "POST",
					url : "/ProjectManSys/projectPeopleRead/",
					data : {
						projectId:$('#projectId').html()				
					},
					datatype : "json",
					success : function(data) {
						var json = eval("(" + data + ")");
						var eds = $('#projectTask').datagrid('getEditors', editIndex);
						$(eds[2].target).combobox('loadData',json);
					}
				});
			}		 
		}else{
			$('#projectTask').datagrid('selectRow', editIndex);
		}		
	}
};
function endEditing(){
	if (editIndex == undefined){return true} 
	if ($('#projectTask').datagrid('validateRow', editIndex)){  
		var eds = $('#projectTask').datagrid('getEditors', editIndex);
		var stime = $(eds[3].target).datebox('getValue');
		var etime = $(eds[4].target).datebox('getValue');
		var ftime = $(eds[5].target).datebox('getValue');
		var tstime = new Date(stime.replace(/-/g, "\/"));
		var tetime = new Date(etime.replace(/-/g, "\/"));
		var ttime = ((tetime-tstime)/(1000*60*60*24)+1)*24;
		if (ttime<=0){
			$.messager.show({
				height:40,
				msg:'Start time can not be less than the end of time！',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}else if(ttime<$(eds[6].target).val()){
			$.messager.show({
				height:40,
				msg:'Time not correct',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}else{
			updateTask(editIndex,eds);
			$('#projectTask').datagrid('updateRow',{
				index: editIndex,
				row:{
					name: $(eds[0].target).val(),
					status:$(eds[1].target).combobox('getText'),
					user:$(eds[2].target).combobox('getText'),
					startTime:stime,
					endTime:etime,
					finishTime:ftime,
					useTime:$(eds[6].target).val(),
					desc:$(eds[7].target).val(),
					percent:$(eds[8].target).combobox('getText')
				}
			});	
		}		
		$('#projectTask').datagrid('endEdit', editIndex);
		editIndex = undefined;
		return true;
	} else {  
		 return false;
	}
};
function updateTask(id,editor){
		var rows = $('#projectTask').datagrid('getRows');
		var row = rows[id]		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectTaskUpdate",
			data : {
				id:row.id,
				name:$(editor[0].target).val(),
				status:$(editor[1].target).combobox('getValue'),
				user:$(editor[2].target).combobox('getValues'),
				startTime:$(editor[3].target).datebox('getValue'),
				endTime:$(editor[4].target).datebox('getValue'),
				finishTime:$(editor[5].target).datebox('getValue'),
				useTime:$(editor[6].target).val(),
				desc:$(editor[7].target).val(),
				percent:$(editor[8].target).datebox('getValue')
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
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
};


//读取审核信息
function notesLoad(rowId)
{
	$.ajax({
		type : "POST",
		url : "/ProjectManSys/notesDetail/",
		data : {
			task: rowId,
			
		},
		datatype : "json",
		success : function(data) {
			var json = eval("(" + data + ")");
				//console.log(json);
				if(json.length == 0)
				{
					$("#taskReview .chat-line").html("No comment yet");
				}
				else
				{
					$("#taskReview .chat-line").html("");
					for(var i=0; i<json.length; i++)
					{
						//console.log(json[i].important);
						switch(json[i].important)
						{
							case 1:
								$("#taskReview .chat-line").append("<li class=\"highlight\">"+
					                    "<span class=\"message\">"+json[i].content+"</span>"+
					                    "<div class=\"author\">Time<span class=\"author-time\">"+json[i].time+"</span>By<span class=\"author-name\">"+json[i].author+"</span></div>"+
					                "</li>");
								break;
								
							default:
								$("#taskReview .chat-line").append("<li>"+
				                    "<span class=\"message\">"+json[i].content+"</span>"+
				                    "<div class=\"author\">Time<span class=\"author-time\">"+json[i].time+"</span>By<span class=\"author-name\">"+json[i].author+"</span></div>"+
				                "</li>");
								break;
						}
						
					}
				}
			
		}
	});
}

//审核关闭按钮
function chatWindowClose()
{	
	$("#taskReview").hide();
}

//绑定右键菜单
// function onRowContextMenu(e, rowIndex, rowData){
//     
    // $('#projectTask').datagrid('selectRow',rowIndex);
//     
    // $("#showNotes").one("click", function(){
    	// $("#taskId").val(rowData.id);
		// notesLoad(rowData.id);
	// }); 
    // e.preventDefault();
    // $('#mm').menu('show', {
        // left:e.pageX,
        // top:e.pageY
    // });
//             
// }

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#projectTask').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});

});

// 显示评论窗口
function onShowComment(){
	console.log('show comment');
	
	var row = $('#projectTask').datagrid('getSelected');
	if(row){
		console.log('row selected:    ' + row.id);
		$("#taskId").val(row.id);
		notesLoad(row.id);
		$("#taskReview").show();
	}
	else
	{
		$.messager.show({ 
			height:40,
			msg:'Select a task to show comments',
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


// 显示发布窗口
function onTaskIssueWinOpen(){
	var row = $('#projectTask').datagrid('getSelected');
	
	if(row){
		console.log("projectTaskIssueWin");
		$("#issueTaskSelected").html(row.id);
		$("#projectTaskIssueWin").window('open');
		
		$(function() {
				$('#file_upload').uploadify({
					'formData'     : {
						'sessionId' : $('#sessionId').html(),
						//'projectId'	: $('#projectId').html(),
						'taskId'	: $('#issueTaskSelected').html()
					},
					'swf'      : '/static/extraneous/uploadify/uploadify.swf',
					'uploader' : '/ProjectManSys/issueFileUpload',
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
									$('#projectTask').datagrid('reload');
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


