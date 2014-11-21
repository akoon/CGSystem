//放置处理Dom事件函数
$(document).ready(function(){
	//更改需要链接的渲染
	$('#commit-server').bind('click', function(){
		 var svrIP = $('#SrvIP').val() || '172.16.253.246';
		 var svrPort = $('#SvrPort').val() || '44331';
		 $.admintool.commitServer(svrIP, svrPort)
		 .success(function(data){
		 	 if(data.status == '1'){
		 	 	$.admintool.getConnectStatus()
		 	 	.success(function(data){
		 	 		if(data.connectstatus == '2'){
		 	 			$.admintool.getRenderNodes()
		 	 			.success(function(data){
		 	 				insertnodes(data);
		 	 			});
		 	 			$.admintool.getRenderTasks()
		 	 			.success(function(data){
		 	 				inserttasks(data);
		 	 			});
		 	 			$.admintool.getIntervalRenderNodes(insertnodes);
		 	 			$.admintool.getIntervalRenderTasks(inserttasks);
		 	 		}else{
		 	 			$.messager.show({
							height:40,
							msg:'连接渲染服务器失败',
							timeout:2000,
							showType:'slide',
							style:{
								right:'',
								top:0,
								bottom:''
							}
						});
		 	 		}
		 	 	})
		 	 }else{
		 	 	$.messager.show({
					height:40,
					msg:'数据发送失败',
					timeout:2000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
		 	 }
		 })
		 .complete(function(){
			 $('#setRenderSvr').modal('hide');
		 });
	});
	
	//向渲染节点表格添加数据
	function insertnodes(data){
		var $nodestbody = $('#nodes').children('tbody');
		$nodestbody.children('tr').remove();
		for(var key in data){
			var node = data[key];
			var $tr = $('<tr></tr>');
			$tr.append($('<td></td>').append(parseInt(key) + 1));
			$tr.append($('<td></td>').append($('<i></i>').addClass($.admintool.nodestatus[node[8]])))
			$tr.append($('<td></td>').append(node[1]));
			$tr.append($('<td></td>').append(node[0]));
			$tr.append($('<td></td>').append(node[5] == 0 ? 'no' : 'yes'));
			$tr.append($('<td></td>').append(node[6] == 0 ? 'no' : 'yes'));
			$tr.append($('<td></td>').append(node[7] == 0 ? 'no' : 'yes'));
			$nodestbody.append($tr);
		}
	}
	
	//向表格中插入任务数据
	function inserttasks(data){
		$('#tasks').data('tasks', data);
		var $taskstbody = $('#tasks').children('tbody');
		$taskstbody.children('tr').remove();
		for(var key in data){
			var task = data[key];
			var $tr = $('<tr></tr>');
			$tr.data('id', task[0]);
			//$tr.append($('<td></td>').append(parseInt(key) + 1));
			$tr.append($('<td></td>').append(task[0]))
			$tr.append($('<td></td>').append($('<i></i>').addClass($.admintool.taskstatus[task[18]])))
			$tr.append($('<td></td>').append(task[2]));
			$tr.append($('<td></td>').append(task[19]));
			$tr.append($('<td></td>').append(task[12]));
			$tr.append($('<td></td>').append(task[13]));
			$tr.append($('<td></td>').append(task[3]));			
			$tr.append($('<td></td>').append(task[4]));
			$tr.append($('<td></td>').append(parseInt(task[5]) + parseInt(task[4]) - 1));
			$tr.append($('<td></td>').append((new Date(parseFloat(task[7]))).toLocaleTimeString()));
			$taskstbody.append($tr);
		}
	}
	
	//表格单选
	$('tbody').delegate('tr', 'click', function(){
		if ($(this).hasClass('selectTable')){
			$(this).removeClass('selectTable');
			if($(this).parent().parent().attr('id') == 'tasks')
				$('#subtasks').children('tbody').children('tr').remove();
		}else{
			$(this).addClass('selectTable').siblings().removeClass('selectTable');
			selecttable($(this));
		}
	});
	
	function selecttable($tr){
		var $table = $tr.parent().parent();
		if($table.attr('id') == 'tasks'){
			var data = $table.data('tasks');
			var taskid = $tr.data('id');
			for(var key in data){
				if(data[key][0] == taskid){
					var $subtaskstbody = $('#subtasks').children('tbody');
					$subtaskstbody.children('tr').remove();
					var subtasks = data[key][20];
					for(var i in subtasks){
						var subtask = subtasks[i];
						var $tr = $('<tr></tr>');
						$tr.data('index', subtask[0]);
						//$tr.append($('<td></td>').append(parseInt(i) + 1));
						$tr.append($('<td></td>').append(subtask[0]))
						$tr.append($('<td></td>').append($('<i></i>').addClass($.admintool.subtaskstatus[subtask[5]])))
						$tr.append($('<td></td>').append(subtask[4]));
						$tr.append($('<td></td>').append(subtask[2]));
						$tr.append($('<td></td>').append(subtask[3]));
						$subtaskstbody.append($tr);
					}
					break;
				}
			}
		}else if($table.attr('id') == 'subtasks'){
			//alert('1');	
		}
	}
	
	//进入渲染工具页面就自动触发click事件
	!function(){
		var e = $.Event('click');
		$('#commit-server').trigger(e);
	}()
	
	//搜索提示框
	$('#mysearch').typeahead({
		source: function(query, process){
			var tasks = $('#tasks').data('tasks');
			var sourcedata = new Array();
			for(var key in tasks){
				var task = tasks[key];
				var subtasks = task[19];
				//任务ID				
				sourcedata.push(task[0].toString());
				//任务IP
				sourcedata.push(task[2].toString());
				//任务名字
				sourcedata.push(task[12].toString());
				//子任务格式：任务ID-子任务ID
				for(var subkey in subtasks){
					var item = task[0] + '-' + subtasks[subkey][0];
					sourcedata.push(item);
				}
			}
			process(sourcedata);
		},
		matcher: function(item){
			var myquery = this.query;
			var patt = new RegExp('.');
			patt.compile('^' + myquery + '\d*');
			if(patt.test(item)){
				return true;
			}
			patt.compile('^' + myquery + '\w*');
			if(patt.test(item)){
				return true;
			}
			return false;
		}
	}).keyup(function(e){
		if(e.keyCode == 13){
			//向搜索结果模态对话框写入结果
			//1.呈现结果的表格
			$('#selectResult').css({ left:'38%', width:'1000px'});
			$('#selectResult').modal('show');
			$table = $('#myResult');
			$table.children('tbody').empty();
			$tbody = $table.children('tbody');
			//2.搜索框的值和为了匹配的正则表达式
			var tasks = $('#tasks').data('tasks');
			for(var key in tasks){
				var item = $(this).val();
				var task = tasks[key];
				var subtasks = task[19];
				var sourcedata = new Array();
				//任务ID				
				sourcedata.push(task[0].toString());
				//任务IP
				sourcedata.push(task[2].toString());
				//任务名字
				sourcedata.push(task[12].toString());
				//子任务格式：任务ID-子任务ID
				for(var subkey in subtasks){
					var subtask = task[0] + '-' + subtasks[subkey][0];
					sourcedata.push(subtask);
				}
				for(var key in sourcedata){
					var patt = new RegExp('.');
					patt.compile('^' + item + '\d*');
					if(patt.test(sourcedata[key])){
						var $tr = $('<tr></tr>');
						$tr.append($('<td></td>').append(task[0]));
						$tr.append($('<td></td>').append($('<i></i>').addClass($.admintool.taskstatus[task[18]])));
						$tr.append($('<td></td>').append(task[2]));
						$tr.append($('<td></td>').append(task[19]));
						$tr.append($('<td></td>').append(task[12]));
						$tr.append($('<td></td>').append(task[13]));
						$tr.append($('<td></td>').append(task[3]));			
						$tr.append($('<td></td>').append(task[4]));
						$tr.append($('<td></td>').append(parseInt(task[5]) + parseInt(task[4]) - 1));
						$tr.append($('<td></td>').append((new Date(parseFloat(task[7]))).toLocaleTimeString()));
						$tbody.append($tr);
						break;
					}
					patt.compile('^' + item + '\w*');
					if(patt.test(sourcedata[key])){
						var $tr = $('<tr></tr>');
						$tr.append($('<td></td>').append(task[0]));
						$tr.append($('<td></td>').append($('<i></i>').addClass($.admintool.taskstatus[task[18]])));
						$tr.append($('<td></td>').append(task[2]));
						$tr.append($('<td></td>').append(task[12]));
						$tr.append($('<td></td>').append(task[13]));
						$tr.append($('<td></td>').append(task[3]));			
						$tr.append($('<td></td>').append(task[4]));
						$tr.append($('<td></td>').append(parseInt(task[5]) + parseInt(task[4]) - 1));
						$tr.append($('<td></td>').append((new Date(parseFloat(task[7]))).toLocaleTimeString()));
						$tbody.append($tr);
						break;
					}
				}
			}
		}
	});
	
	//用于获取服务器目录树
	$('.file_browser, .path_browser').click(function(){
		var $input = $(this).parent().children(':text');
		var $filetree = $(this).parent().parent().find('.filetree');
		$filetree.fileTree({
            				root: '/Pillars/',
            				script: '/RenderManSys/getFileTree/',
            				expandSpeed: 500,
            				collapseSpeed: 500,
            				multiFolder: false,
            				folderProcess : function(folder){
            					$input.val(folder);
            				}
        				}, function(file) {
            				$input.val(file);
            			});
	});
	
	//提交任务
	$('.submittask').click(function(){
		var $taskform = $(this).parent().siblings('.modal-body');
		var taskname = $taskform.find('input[name="task_name"]').val();
		var rendername = $taskform.find('select[name="render_name"]').val();
		var priority = $taskform.find('select[name="priority"]').val();
		var outfiletype = $taskform.find('select[name="outfile_type"]').val();
		var start_frame = $taskform.find('input[name="start_frame"]').val();
		var end_frame = $taskform.find('input[name="end_frame"]').val();
		var file_name = $taskform.find('input[name="file_name"]').val();
		var render_step = $taskform.find('input[name="render_step"]').val();
		var render_node_path = $taskform.find('input[name="render_node_path"]').val();
		var group = $taskform.find('input[name="group"]').val();
		var input_file = $taskform.find('input[name="input_file"]').val();
		var output_path = $taskform.find('input[name="output_path"]').val();
		
		var taskdata = {
			'cmd': 'cmd_render_task',
			'type': $.admintool.tasktype[rendername],
			'Priority': priority,
			'StartFrame': start_frame,
			'FrameCount': $.admintool.tasktype[rendername] == 3 ? 1 : (end_frame - start_frame + 1),
			'Step': render_step,
			'Groups': group,
			'FileType': outfiletype,
			'TaskName': taskname,
			'RenderName': rendername,
			'InputPath': input_file,
			'InputFileName': file_name,
			'OutputPath': output_path,
			'Misc': render_node_path
		};
		var tasks = new Array(); 
		tasks.push(taskdata);
		console.log(JSON.stringify(tasks));
		$.admintool.putRenderTasks({cmds: JSON.stringify(tasks)});
		$(this).parent().parent().modal('hide');
	});
})

//把admintoo加入到jquery全局变量中
$.extend({admintool : new Admintool()})

//用于处理ajax的类
function Admintool(){
	this.svrip = '172.16.253.201';
	this.svrport = '44331';
	this.connectstatus = null; //连接渲染服务器状态
	this.intervalnodes = null;  //获取渲染节点的定时器
    this.intervaltasks = null; //获取渲染任务的定时器
	
	this.nodestatus = {'0': 'icon-remove',
    				   '1': 'icon-ok',
    				   '2': 'icon-time'};
    				   
    this.taskstatus = {'0': 'icon-remove',
    				   '1': 'icon-time',
    				   '2': 'icon-play',
    				   '3': 'icon-ok',
    				   '4': 'icon-remove',
    				   '5': 'icon-remove'};	   
   	
   	this.subtaskstatus = {'0': 'icon-remove',
    				   	  '1': 'icon-time',
    				      '2': 'icon-play',
    				      '3': 'icon-ok',
    				      '4': 'icon-remove'};
    				      
    this.tasktype = {'houdini project render': 1,
    				 'houdini ifd render': 0,
    				 'Nuke project render': 5,
    				 'houdini simulation render':3};				      
}
Admintool.prototype.constructor = Admintool
Admintool.prototype.commitServer = function(svrip, svrport){
	var ip = svrip || this.svrip;
	var port = svrport || this.svrport;
	return $.getJSON('/RenderManSys/connectRenderServer/', {svrip : ip, svrport : port});
}
Admintool.prototype.getConnectStatus = function(){
	return $.getJSON('/RenderManSys/getConnectStatus/');
}
Admintool.prototype.getRenderNodes = function(){
	return $.getJSON('/RenderManSys/getRenderNodes/');
}
Admintool.prototype.getRenderTasks = function(){
	return $.getJSON('/RenderManSys/getRenderTasks/');
}
Admintool.prototype.putRenderTasks = function(cmds){
	return $.getJSON('/RenderManSys/putRenderCmd/', cmds);
}

Admintool.prototype.getIntervalRenderNodes = function(opdom){
	var myself = this;
	var delaytime = 15000;
	this.intervalnodes = setInterval(mycallback, delaytime);
	function mycallback(){
		myself.getRenderNodes()
		.success(function(data){
			opdom(data);
		});
	}
}
Admintool.prototype.getIntervalRenderTasks = function(opdom){
	var myself = this;
	var delaytime = 6000;
	this.intervaltasks = setInterval(mycallback, delaytime);
	function mycallback(){
		myself.getRenderTasks()
		.success(function(data){
			opdom(data);
		});
	}
}

