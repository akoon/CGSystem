//tab标识当前页
$('#templLnk').addClass('active');
$('#projectSettingsLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
	//**************************************页面初始化**************************************
	//模板信息表格
	$('#templ').treegrid({
		width: _w - sidebarWidth,
	    height:_h -40, 
	    url:'/ProjectManSys/templDetail/',  
	    method:'get',
	    idField:'id',
	    treeField:'name',
	    toolbar: '#templTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    animate:false,
	    rownumbers:false,
	    columns:[[  
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'Name',editor:'text',width:($(window).width() - sidebarWidth) * 0.3},
			{field:'desc',title:'Description',editor:'text',width:_w - ($(window).width() - sidebarWidth) * 0.7}
	    ]],
	    onLoadSuccess:onLoadSuccess
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//模板添加窗口
	$('#templAddWin').window({  
	    width:340,  
	    height:260,  
	    title:'Add Template',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onTemplAddOpen   
	});
	//父模板combbox
	$('#parentNewCombobox').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',
	    editable:false  
	});
	
	//模板添加确定按钮
	$('#templAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//模板添加取消按钮
	$('#templAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//模板修改窗口
	$('#templUpdateWin').window({  
	    width:340,  
	    height:260,
	    title:'Edit Template',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onTemplUpdateOpen   
	});
	//父模板combbox
	$('#parentOldCombobox').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',
	    editable:false  
	});
	
	//模板修改确定按钮
	$('#templUpdateOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//模板修改取消按钮
	$('#templUpdateCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});

	//**************************************表单验证************************************** 
	$('.newName').validatebox({  
	    required: true
	});

	//**************************************Toolbar操作************************************** 
	//—--------------添加行
		$('#templAdd').click( function() {
			$('#templAddWin').window('open');
		});
		$('#templAddCancel').click( function() {
			$('#templAddWin').window('close');
		});
		$('#templAddOk').click( function() {
			var parent = $('#parentNewCombobox').combobox('getValue');
			var name = $('#newName').val();
			var desc = $('#newDesc').val();
			
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/templCreate/",
				data : {
					parent:parent,
					name:name,
					desc:desc
					},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");				 
					if (json.success){
						$('#templAddWin').window('close');
						$('#templ').treegrid('reload');

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
    	
    //—--------------删除行  
	$('#templDelete').click( function() {  		
		var row = $('#templ').treegrid('getSelected');
		if(row){
			var msg = '';
			
			var children = $('#templ').treegrid('getChildren', row.id);
			
			//alert(children);
			//console.log(children);
			
			if(children == '' || children == null)
			{
				msg = 'Are you sure you want to delete this item？';
			}
			else
			{
				msg = 'Are you sure to delete this template together with the following template？';
			}
			
			$.messager.confirm('Are you sure you want to delete this item?', msg, function(r){
				if (r){
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/templDestroy/",
						data : {
							id :row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#templ').treegrid('reload');
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
	$('#templUpdate').click( function() { 
		var row = $('#templ').treegrid('getSelected');
		if (row){				
			$('#templUpdateWin').window('open');
		}else{
			$.messager.show({
				height:40,
				msg:'Please choose an item you want to edit',
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
	$('#templUpdateCancel').click( function() {
		$('#templUpdateWin').window('close');
	});
	$('#templUpdateOk').click( function() {
		var row = $('#templ').treegrid('getSelected');
		
		var parent = $('#parentOldCombobox').combobox('getValue');
		var name = $('#oldName').val();
		var desc = $('#oldDesc').val();
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/templUpdate/",
			data : {
				id:row.id,
				parent:parent,
				name:name,
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$('#templUpdateWin').window('close');
					$('#templ').treegrid('reload');
					
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
//正在编辑的表格
var editIndex = undefined;
//表格数据加载完成
function onLoadSuccess(row, data){
	
};

//模板添加窗口打开
function onTemplAddOpen(){
	$('#parentNewCombobox').combobox('reload','/ProjectManSys/templRead/0');
	$('#parentNewCombobox').combobox('clear');
	
	$('#newName').val('');
	$('#newDesc').val('');
};

//部门修改窗口打开
function onTemplUpdateOpen(){
	$('#parentOldCombobox').combobox('reload','/ProjectManSys/templRead/0');
	
	var row = $('#templ').treegrid('getSelected');
	var parent = $('#templ').treegrid('getParent',row.id);
	
	if (parent){
		$('#parentOldCombobox').combobox('enable');
		$('#parentOldCombobox').combobox('select',parent.name);
		$('#parentOldCombobox').combobox('setValue',parent.id);
	}else{	
		$('#parentOldCombobox').combobox('disable');
	};
	
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#templ').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#templ').datagrid('resize');
});