//tab标识当前页
$('#projectPerformanceLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
	//**************************************页面初始化************************************** 	
	
	//项目人员信息表格
	$('#projectPeople').datagrid({
		width: _w - sidebarWidth,
	    height:_h - 40, 
	    url:'/ProjectManSys/projectPerformanceDetail/',
	    //method:'get',
	    idField:'id', 
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    rownumbers:false,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'img',title:'Thumb',formatter:onPeopleImg}, 
	        {field:'user',title:'Username',sortable:true,width:($(window).width() - sidebarWidth) * 0.1}, 
	        {field:'name',title:'Name',sortable:true,width:($(window).width() - sidebarWidth) * 0.1}, 
	        {field:'efficiency',title:'Efficiency',sortable:true,width:($(window).width() - sidebarWidth) * 0.1}, 
	    
		]],	  
		queryParams: {
			projectId:$('#projectId').html()
		},  
		onDblClickRow:onDblClickRow,
    	onClickRow:onClickRow,
	});
		
	//项目人员选择
	$('#projectPeopleAddCombo').combobox({  
		//url: '/BaseSys/peopleRead/0',
		method: 'get',
		valueField: 'id',  
		textField: 'name',  
		multiple: true,  
		panelHeight: 210,
		onShowPanel:onShowPanel,
		onHidePanel:onHidePanel
		});
	
	//隐藏添加框
	$('#projectPeopleSelect').hide();
		
	//**************************************Toolbar操作************************************** 
	//—--------------项目人员添加
	$('#projectPeopleAdd').click( function() {
		$('#projectPeopleSelect').show();
		$('#projectPeopleAdd').hide();		
		$('#projectPeopleAddCombo').combobox('clear');
		$('#projectPeopleAddCombo').combobox('reload','/BaseSys/peopleRead/0');	
	});
	
	$('#projectPeopleDelete').click( function() {		
		var row = $('#projectPeople').datagrid('getSelected');		
		if(row){			
			$.messager.confirm('Delete', 'Are you sure you want to delete this item？', function(r){
				if (r){
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/projectPeopleDestroy",
						data : {
							projectId:$('#projectId').html(),
							id :[row.id]
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#projectPeople').datagrid('unselectAll');
								$('#projectPeople').datagrid('reload');
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

	$('#dd').panel('close');
	$('#projectPeopleEdit').click(function(){
		$('#dd').panel('open');
		projpeople();	
	});
	

	function projpeople(){
		//已在项目中人员表格处理
		$('#projpeoplein').datagrid({
		    url:'/ProjectManSys/projectPeopleDetail/',
		    idField:'id', 
		    autoRowHeight: true,
		    striped:true,
		    //scrollbarSize: 400,
		    rownumbers:true,
		    singleSelect:true,
		    columns:[[ 
			{title:'id',field:'id',hidden:true},
			{field:'user',title:'Username',sortable:true,width:140}, 
			{field:'name',title:'Name',sortable:true,width:110}, 
			{field:'email',title:'Email',sortable:true,width:240}, 
			]],	  
			queryParams: {
				projectId:$('#projectId').html()
			},  
		    onDblClickRow:function(rowIndex, rowData){
				$('#projpeopleout').datagrid('insertRow',{
					row: {
						id: rowData.id,
						user: rowData.user,
						name: rowData.name,
						email: rowData.email
					}
					});
				$(this).datagrid('deleteRow', rowIndex);
			},
		});

		//未在项目中人员表格处理
		$('#projpeopleout').datagrid({
		    url:'/BaseSys/peopleRead/' + $('#projectId').html(),
		    method:'get',
		    idField:'id', 
		    autoRowHeight: true,
		    striped:true,
		    //scrollbarSize: 400,
		    rownumbers:true,
		    singleSelect:true,
		    columns:[[ 
			{title:'id',field:'id',hidden:true},
			{field:'user',title:'Username',sortable:true,width:140}, 
			{field:'name',title:'Name',sortable:true,width:110}, 
			{field:'email',title:'Email',sortable:true,width:240}, 
			]],
		    onDblClickRow:function(rowIndex, rowData){
				$('#projpeoplein').datagrid('insertRow',{
					row: {
						id: rowData.id,
						user: rowData.user,
						name: rowData.name,
						email: rowData.email
					}
					});
				$(this).datagrid('deleteRow', rowIndex);
			},
		});
	
		$('#projpeoplecancle').click(function(){
			$('#dd').panel('close');
	
		});
	
		$('#projpeopleok').click(function(){
			var rows = $('#projectPeople').datagrid('getRows');
			var rowids = new Array();
			for(var index in rows){
				rowids.push(rows[index].id);
			}
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/projectPeopleDestroy",
				data : {
					projectId:$('#projectId').html(),
					id :rowids
					},
				datatype : "json",
				success : function(data){
						var rows = $('#projpeoplein').datagrid('getRows');
						var rowids = new Array();
						for(var index in rows){
							rowids.push(rows[index].id);
						}
						$.ajax({
							type : "POST",
							url : "/ProjectManSys/projectPeopleCreate",
							data : {
								projectId:$('#projectId').html(),
								id :rowids
							},
							datatype : "json",
							success : function(data) {
								var json = eval("(" + data + ")");				 
								if (json.success){
									$('#projectPeople').datagrid('reload');
									$('#dd').panel('close');
									$.messager.show({
										height:40,
										msg:'Operation success',
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
		});

	}
		
}); 
//**************************************函数************************************** 
//项目人员管理头像显示
function onPeopleImg(value,rowData,rowIndex){
	if (rowData.img) {
		return '<img id="peopleImg" class="thum" src="' + rowData.img+ '" style="height:50px;">'
	} else {
		return '<img id="peopleImg" class="thum" src="/static/pillars/img/user.png" style="height:50px;">'		
	}
};

//项目人员管理性别显示
function onPeopleSex(value,rowData,rowIndex){
	if (value == 0){
		return 'Female'
	}else{
		return 'Male'
	}	
};

var peopleSelect = false
//人员选择显示
function onShowPanel(){
	peopleSelect = true;
};

//人员选择隐藏
function onHidePanel(){
	if(peopleSelect){
		var people = $('#projectPeopleAddCombo').combobox('getValues');
		if(people){
			onAddProejectPeople(people)
			$('#projectPeopleSelect').hide();
			$('#projectPeopleAdd').show();
			peopleSelect = false;
		}		
	}	
};

function onAddProejectPeople(people){
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/projectPeopleCreate",
						data : {
							projectId:$('#projectId').html(),
							id :people
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");				 
							if (json.success){
								$('#projectPeople').datagrid('reload');
								$.messager.show({
									height:40,
									msg:'Insert success',
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

//正在编辑的表格
var editIndex = undefined;
//单击表格行事件
function onClickRow(rowIndex, field, value){
	if(editIndex != rowIndex){
		endEditing();
	}
	
};
//双击表格行事件
function onDblClickRow(rowIndex, field, value){
	if(editIndex != rowIndex){
		if (editIndex == undefined){
			if (endEditing()){
				$('#projectPeople').datagrid('selectRow', rowIndex);
				$('#projectPeople').datagrid('beginEdit', rowIndex);
				editIndex = rowIndex;	
				//var eds = $('#projectPeople').datagrid('getEditors', editIndex);
				//$(eds[0].target).combotree('loadData',json);
				//$(eds[1].target).combobox('reload','/BaseSys/positionRead');
			}		 
		}else{
			$('#projectPeople').datagrid('selectRow', editIndex);
		}		
	}
};
function endEditing(){
	if (editIndex == undefined){return true} 
	if ($('#projectPeople').datagrid('validateRow', editIndex)){  
		var eds = $('#projectPeople').datagrid('getEditors', editIndex);
		updateTask(editIndex,eds);	
		$('#projectPeople').datagrid('updateRow',{
			index: editIndex,
			row:{
				department: $(eds[0].target).combotree('getText'),
				position:$(eds[1].target).combobox('getText'),
			}
		});			
		$('#projectPeople').datagrid('endEdit', editIndex);
		editIndex = undefined;
		return true;
	} else {  
		 return false;
	}
};
function updateTask(id,editor){
		var rows = $('#projectPeople').datagrid('getRows');
		var row = rows[id]		
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/projectPeopleUpdate",
			data : {
				pid:$('#projectId').html(),
				id:row.id,
				department:$(editor[0].target).combotree('getValue'),
				position:$(editor[1].target).combobox('getValues'),
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");	
				if (json.success){
					$.messager.show({
						height:40,
						msg:'Edit success',
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

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#projectPeople').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#projectPeople').datagrid('resize');
});
