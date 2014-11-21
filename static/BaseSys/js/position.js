//tab标识当前页
$('#basePeopleLnk').addClass('active');
$('#positionlLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 157;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化************************************** 
	var _h = $(window).height();
	var _w = $(window).width();
	//职位信息表格	
	$('#position').datagrid({
		width: _w - sidebarWidth,
	    height:_h - 40, 
	    url:'/BaseSys/positionDetail/',  
	    method:'get',
	    idField:'id', 
	    toolbar: '#positionTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    rownumbers:true,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'Name',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.3},
	        {field:'desc',title:'Description',sortable:false,editor:'text',width:($(window).width() - sidebarWidth) * 0.7}
		]],
		rownumbers : false
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//职位添加窗口
	$('#positionAddWin').window({  
	    width:320,  
	    height:220,  
	    title:'Add',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onPositionAddOpen   
	});
	
	//职位添加确定按钮
	$('#positionAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//职位添加取消按钮
	$('#positionAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//职位修改窗口
	$('#positionUpdateWin').window({  
	    width:320,  
	    height:220,
	    title:'Edit',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onPositionUpdateOpen
	});
	
	//职位修改确定按钮
	$('#positionUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//职位修改取消按钮
	$('#positionUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});

	//**************************************表单验证******************************************
	$('.positionName').validatebox({  
    	required: true
	}); 
	
	//**************************************Toolbar操作**************************************
	//—--------------添加行
	$('#positionAdd').click( function() {			
		$('#positionAddWin').window('open');
	});
	$('#positionAddCancel').click( function() {
		$('#positionAddWin').window('close');
	});
	$('#positionAddOk').click( function() {
		$.ajax({
			type : "POST",
			url : "/BaseSys/positionCreate",
			data : {
				name:$('#newName').val(),
				desc:$('#newDesc').val()
				
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");				 
				if (json.success){
					$('#positionAddWin').window('close');
					$('#position').datagrid('reload');
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
				else{
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
	$('#positionUpdate').click( function() { 
		var row = $('#position').datagrid('getSelected');
		if (row){				
			$('#positionUpdateWin').window('open');
		}else{
			$.messager.show({
				height:40,
				msg:'Please choose an item to edit',
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
	$('#positionUpdateCancel').click( function() {
		$('#positionUpdateWin').window('close');
	});
	$('#positionUpdateOk').click( function() {
		var row = $('#position').datagrid('getSelected');
		var name = $('#oldName').val();
		var desc = $('#oldDesc').val();
		
		$.ajax({
			type : "POST",
			url : "/BaseSys/positionUpdate",
			data : {
				id:row.id,
				name:name,
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$('#positionUpdateWin').window('close');
					$('#position').datagrid('reload');
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
				}			 
			}
		});
	});
	
	//—--------------删除行 
	$('#positionDelete').click( function() {  		
		var row = $('#position').datagrid('getSelected');
		if(row){
			$.messager.confirm('Delete', 'Are you sure you want to delete this item？', function(r){
				if (r){
					$.ajax({
						type : "POST",
						url : "/BaseSys/positionDestroy",
						data : {
							id :row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#position').datagrid('reload');
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
							}
						}
					});
				}
			});
			
		}else{
			$.messager.show({ 
				height:40,
				msg:'Please choose an item to delete',
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
//职位添加窗口打开
function onPositionAddOpen(){
	$('#newName').val('');
	$('#newDesc').val('');
};

//职位修改窗口打开
function onPositionUpdateOpen(){
	var row = $('#position').datagrid('getSelected');
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#position').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#position').datagrid('resize');
	
});
