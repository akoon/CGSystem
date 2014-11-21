//tab标识当前页
$('#typesLnk').addClass('active');
$('#projectSettingsLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化************************************** 

	//类型信息表格	
	$('#types').treegrid({
		width: _w - sidebarWidth,
	    height:_h - 40, 
	    url:'/ProjectManSys/typesDetail',  
	    method:'get',
	    idField:'id',  
	    treeField:'name',  
	    toolbar: '#typesTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    animate:false,
	    rownumbers:false,
	    expandAll:true,
	    columns:[[  
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'Name',editor:'text',width:($(window).width() - sidebarWidth) * 0.3},  
	        {field:'desc',title:'Description',editor:'text',width:_w - ($(window).width() - sidebarWidth) * 0.7}
	    ]],      
	    onLoadSuccess:onLoadSuccess
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//类型添加窗口
	$('#typesAddWin').window({  
	    width:320,  
	    height:245,  
	    title:'Add type',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onTypesAddOpen   
	});
	
	//类型添加combbox
	$('#newType').combobox({
	    editable:false,
	    panelHeight:80
	});
	//类型添加确定按钮
	$('#typesAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//类型添加取消按钮
	$('#typesAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//类型修改窗口
	$('#typesUpdateWin').window({  
	    width:320,  
	    height:240,
	    title:'Edit type',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onTypesUpdateOpen   
	});
	//类型修改combbox
	$('#oldType').combobox({
	    disabled:true,
	    panelHeight:80
	});
	//类型修改确定按钮
	$('#typesUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//类型修改取消按钮
	$('#typesUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//**************************************表单验证************************************** 
	$('.typesName').validatebox({  
	    required: true
	});

	//**************************************Toolbar操作**************************************
	//—--------------添加行
	$('#typesAdd').click( function() {			
		$('#typesAddWin').window('open');
	});
	$('#typesAddCancel').click( function() {
		$('#typesAddWin').window('close');
	});
	$('#typesAddOk').click( function() {
		var type = $('#newType').combobox('getValue')
		var name = $('#newName').val()
		var desc = $('#newDesc').val()
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/typesCreate/",
			data : {
				type:type,
				name:name,
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success){
					$('#typesAddWin').window('close');
					$('#types').treegrid('reload');
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
    $('#typesDelete').click( function() {  		
		var row = $('#types').treegrid('getSelected');
		if(row){
			if(row.id > 0)
			{
				$.messager.confirm('delete', 'Are you sure you want to delete this item？', function(r){
				if (r){
					$.ajax({
							type : "POST",
							url : "/ProjectManSys/typesDestroy",
							data : {
								id :row.id
							},
							datatype : "json",
							success : function(data) {
								var json = eval("(" + data + ")");				 
								if (json.success){
									$('#types').treegrid('reload');
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
				msg:'Delete not allowed',
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
				msg:'Please choose an item you want to delete',
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
	$('#typesUpdate').click( function() { 
		var row = $('#types').treegrid('getSelected');
		if (row){
			if(row.id > 0) {
				$('#typesUpdateWin').window('open');
			}
			else
			{
				$.messager.show({ 
				height:40,
				msg:'edit not allowed',
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
				msg:'please choose an item you want to edit',
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
	$('#typesUpdateCancel').click( function() {
		$('#typesUpdateWin').window('close');
	});
	$('#typesUpdateOk').click( function() {
		var row = $('#types').treegrid('getSelected');
		var type = $('#oldType').combobox('getValue')
		var name = $('#oldName').val()
		var desc = $('#oldDesc').val()
		
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/typesUpdate",
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
						$('#typesUpdateWin').window('close');
						$('#types').treegrid('reload');
						
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
function onTypesAddOpen(){
//	$('#departmentAddCombobox').combobox('reload','/BaseSys/departmentRead/0')
//	$('#departmentAddCombobox').combobox('clear');
	$('#newName').val('');
	$('#newDesc').val('');
};

//状态修改窗口打开
function onTypesUpdateOpen(){
	var row = $('#types').treegrid('getSelected');
	var parent = $('#types').treegrid('getParent',row.id);
	
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
	$('#types').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#types').datagrid('resize');
});
