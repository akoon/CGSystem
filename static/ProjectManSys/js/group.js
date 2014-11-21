//tab标识当前页
$('#groupLnk').addClass('active');
$('#projectSettingsLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化************************************** 
	//组信息表格	
	$('#group').datagrid({
		width: _w - sidebarWidth,
	    height:_h - 40, 
	    url:'/ProjectManSys/groupDetail',  
	    method:'get',
	    idField:'id', 
	    toolbar: '#groupTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    rownumbers:false,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'名称',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.3},
	        {field:'desc',title:'描述',sortable:false,editor:'text',width:_w - ($(window).width() - sidebarWidth) * 0.7}
		]]
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//组添加窗口
	$('#groupAddWin').window({  
	    width:280,  
	    height:250,  
	    title:'添加职位',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onGroupAddOpen   
	});
	
	//组添加确定按钮
	$('#groupAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//组添加取消按钮
	$('#groupAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//组修改窗口
	$('#groupUpdateWin').window({  
	    width:280,  
	    height:250,
	    title:'修改职位',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onGroupUpdateOpen
	});
	
	//组修改确定按钮
	$('#groupUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//组修改取消按钮
	$('#groupUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});

	//**************************************表单验证******************************************
	$('.groupName').validatebox({  
    	required: true
	}); 

	//**************************************Toolbar操作**************************************
	//—--------------添加行
	$('#groupAdd').click( function() {			
		$('#groupAddWin').window('open');
	});
	$('#groupAddCancel').click( function() {
		$('#groupAddWin').window('close');
	});
	$('#groupAddOk').click( function() {
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/groupCreate/",
			data : {
				name:$('#newName').val(),
				desc:$('#newDesc').val()
				
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");				 
				if (json.success){
					$('#groupAddWin').window('close');
					$('#group').datagrid('reload');
					$.messager.show({
						height:40,
						msg:'添加成功',
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
	$('#groupUpdate').click( function() { 
		var row = $('#group').datagrid('getSelected');
		if (row){				
			$('#groupUpdateWin').window('open');
		}else{
			$.messager.show({
				height:40,
				msg:'请选择要修改的数据',
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
	$('#groupUpdateCancel').click( function() {
		$('#groupUpdateWin').window('close');
	});
	$('#groupUpdateOk').click( function() {
		var row = $('#group').datagrid('getSelected');
		var name = $('#oldName').val();
		var desc = $('#oldDesc').val();
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/groupUpdate/",
			data : {
				id:row.id,
				name:name,
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$('#groupUpdateWin').window('close');
					$('#group').datagrid('reload');
					$.messager.show({
						height:40,
						msg:'修改成功',
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
	
	//—--------------删除行 
	$('#groupDelete').click( function() {  		
		var row = $('#group').datagrid('getSelected');
		if(row){
			$.messager.confirm('确认删除', '你确定要删除该数据？', function(r){
				if (r){
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/groupDestroy/",
						data : {
							id :row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#group').datagrid('reload');
								$.messager.show({
									height:40,
									msg:'删除成功',
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
				msg:'请选择要删除的数据',
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

});

//**************************************函数**************************************
//组添加窗口打开
function onGroupAddOpen(){
	$('#newName').val('');
	$('#newDesc').val('');
};

//组修改窗口打开
function onGroupUpdateOpen(){
	var row = $('#group').datagrid('getSelected');
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#group').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#group').datagrid('resize');
});