//tab标识当前页
$('#projectManSysLnk').addClass('active');
$('#projectListLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化**************************************
	$('#project').treegrid({
		width:	_w - sidebarWidth,  
	    height:	_h-90, 
	    url:'/ProjectManSys/indexProject/',  
	    // method:'get',
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
	        {field:'name',title:'name',editor:'text',width:($(window).width() - sidebarWidth) * 0.1,formatter:onFormatterName},  
	        {field:'status',title:'status',editor:'combobox',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'status_id',title:'status_id',editor:'text',width:100,hidden:true},
	        {field:'types',title:'type',editor:'combobox',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'types_id',title:'types_id',editor:'text',width:100,hidden:true},
	        {field:'user',title:'user',editor:'combobox',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'user_id',title:'user_id',editor:'text',width:100,hidden:true},
	        {field:'startTime',title:'start time',editor:'datebox',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'endTime',title:'end time',editor:'datebox',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'desc',title:'description',editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	    ]],
	});
	
	//项目添加窗口
	$('#projectAddWin').window({
	    width:320,  
	    height:340,  
	    title:'add project',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onProjectAddOpen   
	});

	//项目添加类型combbox
	$('#newType').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',
	    editable:false,  
		panelHeight: 'auto', 
	});
	
	//项目添加状态combbox
	$('#newStatus').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false,  
		panelHeight: 'auto',  
	});
	
	//项目添加用户combbox
	$('#newUser').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false,  
		panelHeight: 230,  
	});
	
	//项目添加开始时间DateBox
	$('#newStartTime').datebox({
	    editable:false  
	});
	//项目添加结束时间DateBox
	$('#newEndTime').datebox({
	    editable:false  
	});
	//项目添加确定按钮
	$('#projectAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//项目添加取消按钮
	$('#projectAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//项目修改窗口
	$('#projectUpdateWin').window({
	    width:320,  
	    height:340,  
	    title:'edit project',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onPeopleUpdateOpen   
	});
	
	//项目修改类型combbox
	$('#oldType').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false  
	});
	
	//项目修改状态combbox
	$('#oldStatus').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false  
	});
	
	//项目修改用户combbox
	$('#oldUser').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false  
	});
	
	//项目修改开始时间DateBox
	$('#oldStartTime').datebox({
	    editable:false  
	});
	//项目修改结束时间DateBox
	$('#oldEndTime').datebox({
	    editable:false  
	});
	//项目修改确定按钮
	$('#projectUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//项目修改取消按钮
	$('#projectUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
//**************************************表单验证****************************************

//**************************************Toolbar操作*************************************

	//—--------------添加项目
	$('#projectAdd').click( function() {			
		$('#projectAddWin').window('open');
	});
	$('#projectAddCancel').click( function() {
		$('#projectAddWin').window('close');
	});
	$('#projectAddOk').click( function() {
		var type = $('#newType').combobox('getValue');
		var status = $('#newStatus').combobox('getValue');
		var user = $('#newUser').combobox('getValue');
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectCreate/",
			data : {
				name: $('#newName').val(),
				types: type,
				status: status,
				user: user,
				start_time: $('#newStartTime').datebox('getValue'),
				end_time:   $('#newEndTime').datebox('getValue'),
				desc:		$('#newDesc').val()
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				
				if (json.success){
					$('#projectAddWin').window('close');
					$('#project').treegrid('reload');
				}
				
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
					
//				if (json.success){
//					$('#projectAddWin').window('close');
//					$('#project').treegrid('reload');
//					$.messager.show({
//						height:40,
//						msg:'添加成功',
//						timeout:2000,
//						showType:'slide',
//						style:{
//							right:'',
//							top:0,
//							bottom:''
//						}
//					});
//				}else{
//					$.messager.show({
//						height:40,
//						msg:json.errors,
//						timeout:2000,
//						showType:'slide',
//						style:{
//							right:'',
//							top:0,
//							bottom:''
//						}
//					});
//				}
			}
		});
		
    } );
    
    //—--------------修改项目
	$('#projectUpdate').click( function() { 
		var row = $('#project').datagrid('getSelected');

		if (row != null){
			var level = $('#project').treegrid('getLevel', row.id);
				
			if( parseInt(level) == 1){
				$('#projectUpdateWin').window('open');
			}				
			else{
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
			}
		}else{
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
		}	
	});	
	$('#projectUpdateCancel').click( function() {
		$('#projectUpdateWin').window('close');
	});
	$('#projectUpdateOk').click( function() {
		var row = $('#project').datagrid('getSelected');
		var type = $('#oldType').combobox('getValue');
		var status = $('#oldStatus').combobox('getValue');
		var user = $('#oldUser').combobox('getValue');
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectUpdate/",
			data : {
				id: row.id,
				name: $('#oldName').val(),
				types: type,
				status: status,
				user: user,
				start_time: $('#oldStartTime').datebox('getValue'),
				end_time:   $('#oldEndTime').datebox('getValue'),
				desc:		$('#oldDesc').val()
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success){
					$('#projectUpdateWin').window('close');
					$('#project').treegrid('reload');
					$.messager.show({
						height:40,
						msg:'update sucess',
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
	});
	//—--------------刷新项目列表
	$('#projectRefresh').click( function() { 
		$('#project').treegrid('reload');		
	});	
	
	//—--------------删除项目
	$('#projectDelete').click( function() {  		
		var row = $('#project').datagrid('getSelected');
		
		console.log('selected id is : ' + row.id.charAt(0));
		
		if(row){
			if(row.id.charAt(0) == 'a')
			{
				$.messager.confirm('delete', 'Are you sure you want to delete？', function(r){
					if (r){
						$.ajax({
							type : "POST",
							url : "/ProjectManSys/projectDestroy",
							data : {
								id :row.id
							},
							datatype : "json",
							success : function(data) {
								var json = eval("(" + data + ")");				 
								if (json.success){
									$('#project').treegrid('reload');
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
			}
			else
			{
				$.messager.show({ 
					height:40,
					msg:'Delete only Projects',
					timeout:1000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
			}
		}
		else
		{
			$.messager.show({ 
					height:40,
					msg:'Please select the data to be deleted',
					timeout:1000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
		}
		
//		if(row){
//			$.messager.confirm('确认删除', '你确定要删除该数据？', function(r){
//				if (r){
//					$.ajax({
//						type : "POST",
//						url : "/ProjectManSys/projectTaskDestroy",
//						data : {
//							id :row.id
//						},
//						datatype : "json",
//						success : function(data) {
//							var json = eval("(" + data + ")");				 
//							if (json.success){
//								$('#projectTask').datagrid('reload');
//								$.messager.show({
//									height:40,
//									msg:'删除成功',
//									timeout:2000,
//									showType:'slide',
//									style:{
//										right:'',
//										top:0,
//										bottom:''
//									}
//								});
//							}else{
//								$.messager.show({
//									height:40,
//									msg:json.errors,
//									timeout:2000,
//									showType:'slide',
//									style:{
//										right:'',
//										top:0,
//										bottom:''
//									}
//								});
//							}
//						}
//					});
//				}
//			});
//			
//		}else{
//			$.messager.show({ 
//				height:40,
//				msg:'请选择要删除的数据',
//				timeout:2000,
//				showType:'slide',
//				style:{
//					right:'',
//					top:0,
//					bottom:''
//				}
//			});
//		}
	});
	
});
//**************************************函数**************************************

//名称可点击
function onFormatterName(value,row,index){
	id = row.id
	var type = id.substring(0,1)
	var html = null
	if (type =='a'){
		var id = id.substring(1)
		html = "<a href='/ProjectManSys/"+id+"/'>"+value+"</a>"
	}else{
		html = value
	}
	return html
};

//项目添加窗口打开
function onProjectAddOpen(){
	$('#newType').combobox('reload','/ProjectManSys/typesRead/1');
	$('#newStatus').combobox('reload','/ProjectManSys/statusRead/1');
	$('#newUser').combobox('reload','/BaseSys/peopleRead/0');
	$('#newName').val('');
};

//项目修改窗口打开
function onPeopleUpdateOpen(){
	$('#oldType').combobox('reload','/ProjectManSys/typesRead/1');
	$('#oldStatus').combobox('reload','/ProjectManSys/statusRead/1');
	$('#oldUser').combobox('reload','/BaseSys/peopleRead/0');
	
	var row = $('#project').treegrid('getSelected');			

	$('#oldName').val(row.name);


	//因前台报错，故临时解决
//	$('#oldType').combobox('select', null);
//	$('#oldStatus').combobox('select', null);
//	$('#oldUser').combobox('select', null);

	 $('#oldType').combobox('select',row.types_id);
	 $('#oldStatus').combobox('select',row.status_id);
	 $('#oldUser').combobox('select',row.user_id);
	
	$('#oldStartTime').datebox('setValue', row.startTime);
	$('#oldEndTime').datebox('setValue', row.endTime);
	$('#oldDesc').val(row.desc);
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#project').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#project').datagrid('resize');
});

