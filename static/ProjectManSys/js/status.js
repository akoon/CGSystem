//tab标识当前页
$('#statusLnk').addClass('active');
$('#projectSettingsLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化************************************** 
	//状态信息表格	
	$('#status').treegrid({
		width: _w - sidebarWidth,
	    height:_h - 40, 
	    url:'/ProjectManSys/statusDetail',  
	    method:'get',
	    idField:'id',  
	    treeField:'name',  
	    toolbar: '#statusTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    animate:false,
	    rownumbers:false,
	    expandAll:true,
	    columns:[[  
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'name',editor:'text',width:($(window).width() - sidebarWidth) * 0.3},  
	        {field:'desc',title:'description',editor:'text',width:_w - ($(window).width() - sidebarWidth) * 0.7}
	    ]],      
	    onLoadSuccess:onLoadSuccess
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//状态添加窗口
	$('#statusAddWin').window({  
	    width:320,  
	    height:245,  
	    title:'Add status',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onStatusAddOpen   
	});
	
	//状态添加combbox
	$('#newType').combobox({
	    editable:false,
	    panelHeight:80
	});
	//状态添加确定按钮
	$('#statusAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//状态添加取消按钮
	$('#statusAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//状态修改窗口
	$('#statusUpdateWin').window({  
	    width:320,  
	    height:240,
	    title:'Edit status',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onStatusUpdateOpen   
	});
	//状态修改combbox
	$('#oldType').combobox({
	    disabled:true,
	    panelHeight:80
	});
	//状态修改确定按钮
	$('#statusUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//状态修改取消按钮
	$('#statusUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});

	//**************************************表单验证************************************** 
	$('.statusName').validatebox({  
	    required: true
	});
	//**************************************Toolbar操作**************************************
	//—--------------添加行
	$('#statusAdd').click( function() {			
		$('#statusAddWin').window('open');
	});
	$('#statusAddCancel').click( function() {
		$('#statusAddWin').window('close');
	});
	$('#statusAddOk').click( function() {
		var type = $('#newType').combobox('getValue')
		var name = $('#newName').val()
		var desc = $('#newDesc').val()
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/statusCreate/",
			data : {
				type:type,
				name:name,
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");

				if (json.success){
					$('#statusAddWin').window('close');
					$('#status').treegrid('reload');
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

			}
		});	
	
    } );
    
    //—--------------删除行
    $('#statusDelete').click( function() {  		
		var row = $('#status').treegrid('getSelected');
		if(row){
			if(row.id > 0)
			{
				$.messager.confirm('delete', 'Are you sure you want to delete this item？', function(r){
				if (r){
					$.ajax({
							type : "POST",
							url : "/ProjectManSys/statusDestroy",
							data : {
								id :row.id
							},
							datatype : "json",
							success : function(data) {
								var json = eval("(" + data + ")");				 
								if (json.success){
									$('#status').treegrid('reload');
									$.messager.show({
										height:40,
										msg:'delete success',
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
				msg:'delete not allowed',
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
				msg:'choose an item to delete',
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
	//—--------------修改行
	$('#statusUpdate').click( function() { 
		var row = $('#status').treegrid('getSelected');
		if (row){
			if(row.id > 0) {
				$('#statusUpdateWin').window('open');
			}
			else
			{
				$.messager.show({ 
				height:40,
				msg:'edit not allow',
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
				msg:'choose an line you want to edit',
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
	$('#statusUpdateCancel').click( function() {
		$('#statusUpdateWin').window('close');
	});
	$('#statusUpdateOk').click( function() {
		var row = $('#status').treegrid('getSelected');
		var type = $('#oldType').combobox('getValue')
		var name = $('#oldName').val()
		var desc = $('#oldDesc').val()
		
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/statusUpdate",
				data : {
					id:row.id,
					type:type,
					name:name,
					desc:desc
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");
					if (json.success){
						$('#statusUpdateWin').window('close');
						$('#status').treegrid('reload');
						
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

				}
			});
	});
}); 
//**************************************函数**************************************

//状态添加窗口打开
function onStatusAddOpen(){
//	$('#departmentAddCombobox').combobox('reload','/BaseSys/departmentRead/0')
//	$('#departmentAddCombobox').combobox('clear');
	$('#newName').val('');
	$('#newDesc').val('');
};

//状态修改窗口打开
function onStatusUpdateOpen(){
	var row = $('#status').treegrid('getSelected');
	var parent = $('#status').treegrid('getParent',row.id);
	
	$('#oldType').combobox('select',parent.name);
	$('#oldType').combobox('setValue',parent.id);
	
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
};

function onLoadSuccess(row, data){
	
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#status').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#status').datagrid('resize');

});
