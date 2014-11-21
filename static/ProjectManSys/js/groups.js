$(document).ready(function() {
//**************************************页面初始化************************************** 
	var _h = $(window).height();
	var _w = $(window).width();
	//组信息表格	
	$('#group').treegrid({
		//width:auto,  
	    height:_h - 40, 
	    url:'/ProjectManSys/groupDetail',  
	    method:'get',
	    idField:'id', 
	    treeField:'name',  
	    toolbar: '#groupTb',
	    autoRowHeight: true,
	    striped:true,
	    //scrollbarSize: 400,
	    animate:false,
	    rownumbers:false,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'name',title:'Name',sortable:true,editor:'text',width:400},
	        {field:'project',title:'Project',sortable:false,editor:'text',width:260},
	        {field:'desc',title:'Description',sortable:false,editor:'text',width:350}
		]]
	});
	
	//组添加窗口
	$('#groupAddWin').window({  
	    width:280,  
	    height:255,  
	    title:'添加职位',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onGroupAddOpen   
	});
	
	//组添加父类combbox
	$('#groupAddCombobox').combotree({  
    	method:'get',
    	valueField:'id',  
    	textField:'name',
    	editable:false,
    	panelHeight:230,
    	onSelect:onFartherSeleect
	}); 

	//组添加项目combbox
	$('#groupAddProjectCombobox').combobox({  
   		method:'get',
    	valueField:'id',  
    	textField:'name',
    	editable:false,
    	panelHeight:'auto'
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
	    height:230,
	    title:'修改职位',  
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onGroupUpdateOpen
	});
	
	//组添加修改combbox
	$('#groupUpdateProjectCombobox').combobox({  
   		method:'get',
    	valueField:'id',  
    	textField:'name',
    	editable:false,
    	panelHeight:'auto',
    	disabled:true  
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
				parent:$('#groupAddCombobox').combotree('getValue'),
				name:$('#newName').val(),
				project:$('#groupAddProjectCombobox').combobox('getValue'),
				desc:$('#newDesc').val()				
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");				 
				if (json.success){
					$('#groupAddWin').window('close');
					$('#group').treegrid('reload');
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
		
    } );
    
	//—--------------修改行
	$('#groupUpdate').click( function() { 
		var row = $('#group').treegrid('getSelected');
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
		var row = $('#group').treegrid('getSelected');
		var name = $('#oldName').val();
		var desc = $('#oldDesc').val();
		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/groupUpdate/",
			data : {
				id:row.id,
				name:name,
				project:$('#groupUpdateProjectCombobox').combobox('getValue'),
				desc:desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$('#groupUpdateWin').window('close');
					$('#group').treegrid('reload');
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
	
	//—--------------删除行 
	$('#groupDelete').click( function() {  		
		var row = $('#group').treegrid('getSelected');
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
								$('#group').treegrid('reload');
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

//
function onFartherSeleect(node){	
	$('#groupAddProjectCombobox').combobox('disable');
	$('#groupAddProjectCombobox').combobox('clear')
};
//组添加窗口打开
function onGroupAddOpen(){
	$('#groupAddCombobox').combotree('reload','/ProjectManSys/groupRead/');	
	$('#groupAddProjectCombobox').combobox('reload','/ProjectManSys/projectRead/');
	$('#groupAddProjectCombobox').combobox('enable');
	$('#groupAddCombobox').combotree('setValue','');
	$('#groupAddProjectCombobox').combobox('setValue','');
	$('#newName').val('');
	$('#newDesc').val('');
};

//组修改窗口打开
function onGroupUpdateOpen(){
	var row = $('#group').treegrid('getSelected');
	$('#oldName').val(row.name);
	$('#oldDesc').val(row.desc);
	if(row.project){
		$('#groupUpdateProjectCombobox').combobox('setValue',row.project);
	}else{
		$('#groupUpdateProjectCombobox').combobox('setValue','');
	};
	p = $('#group').treegrid('getParent',row.id);
	if (p == null){
		$('#groupUpdateProjectCombobox').combobox('reload','/ProjectManSys/projectRead/');
		$('#groupUpdateProjectCombobox').combobox('enable');
	}else(
		$('#groupUpdateProjectCombobox').combobox('disable')
	);
};

