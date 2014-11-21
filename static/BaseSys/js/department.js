//tab标识当前页
$('#basePeopleLnk').addClass('active');
$('#departmentLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 157;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
	//**************************************页面初始化**************************************

	//部门信息表格
	$('#department').treegrid({
		width : _w - sidebarWidth,
		height : _h - 40,
		url : '/BaseSys/departmentDetail',
		method : 'get',
		idField : 'id',
		treeField : 'name',
		toolbar : '#departmentTb',
		autoRowHeight : true,
		striped : true,
		fitColumns : true,
		//scrollbarSize: 400,
		animate : false,
		rownumbers : true,
		columns : [[{
			title : 'id',
			field : 'id',
			hidden : true
		}, {
			field : 'name',
			title : 'Name',
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.3
		}, {
			field : 'desc',
			title : 'Description',
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.7
		}]],
		onLoadSuccess : onLoadSuccess,
		rownumbers : false
		//onDblClickRow:onDblClickRow,
		//onClickRow:onClickRow
	});
	//部门添加窗口
	$('#departmentAddWin').window({
		width : 320,
		height : 240,
		title : 'Add',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onDepartmentAddOpen
	});
	//部门添加combbox
	$('#departmentAddCombobox').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : true
	});
	//部门体那家确定按钮
	$('#departmentAddOk').linkbutton({
		iconCls : 'icon-ok'
	});
	//部门添加取消按钮
	$('#departmentAddCancel').linkbutton({
		iconCls : 'icon-cancel'
	});
	//部门修改窗口
	$('#departmentUpdateWin').window({
		width : 320,
		height : 240,
		title : 'Edit',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onDepartmentUpdateOpen
	});
	//部门修改combbox
	$('#departmentUpdateCombobox').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false
	});
	//部门修改确定按钮
	$('#departmentUpdateOk').linkbutton({
		iconCls : 'icon-ok'
	});
	//部门修改取消按钮
	$('#departmentUpdateCancel').linkbutton({
		iconCls : 'icon-cancel'
	});
	//**************************************表单验证**************************************
	$('.positionName').validatebox({
		required : true
		//validType: 'email'
	});
	//**************************************Toolbar操作**************************************
	//—--------------添加行
	$('#departmentAdd').click(function() {
		$('#departmentAddWin').window('open');
	});
	$('#departmentAddCancel').click(function() {
		$('#departmentAddWin').window('close');
	});
	$('#departmentAddOk').click(function() {
		var parent = $('#departmentAddCombobox').combobox('getValue')
		var name = $('#newDepartment').val()
		var desc = $('#newDepartmentDesc').val()
		if (name) {
			$.ajax({
				type : "POST",
				url : "/BaseSys/departmentCreate",
				data : {
					parent : parent,
					name : name,
					desc : desc
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");					if (json.success) {
						$('#departmentAddWin').window('close');
						$('#department').treegrid('reload');
						$.messager.show({
							height : 40,
							msg : 'Insert success',
							timeout : 2000,
							showType : 'slide',
							style : {
								right : '',
								top : 0,
								bottom : ''
							}
						});
					} else {
						$.messager.show({
							height : 40,
							msg : json.errors,
							timeout : 2000,
							showType : 'slide',
							style : {
								right : '',
								top : 0,
								bottom : ''
							}
						});
					}
				}
			});
		} else {
			$.messager.show({
				height : 40,
				msg : 'cannot be empty',
				timeout : 2000,
				showType : 'slide',
				style : {
					right : '',
					top : 0,
					bottom : ''
				}
			});
		}
	});
	//—--------------删除行
	$('#departmentDelete').click(function() {
		var row = $('#department').treegrid('getSelected');
		if (row) {
			$.messager.confirm('Delete', 'Are you sure you want to delete this item？', function(r) {
				if (r) {
					$.ajax({
						type : "POST",
						url : "/BaseSys/departmentDestroy",
						data : {
							id : row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");
							if (json.success) {
								$('#department').treegrid('reload');
								$.messager.show({
									height : 40,
									msg : 'Delete success',
									timeout : 2000,
									showType : 'slide',
									style : {
										right : '',
										top : 0,
										bottom : ''
									}
								});
							} else {
								$.messager.show({
									height : 40,
									msg : json.errors,
									timeout : 2000,
									showType : 'slide',
									style : {
										right : '',
										top : 0,
										bottom : ''
									}
								});
							}
						}
					});
				}
			});

		} else {
			$.messager.show({
				height : 40,
				msg : 'Please choose an item to delete',
				timeout : 2000,
				showType : 'slide',
				style : {
					right : '',
					top : 0,
					bottom : ''
				}
			});
		}
	});

	//—--------------修改行
	$('#departmentUpdate').click(function() {
		var row = $('#department').treegrid('getSelected');
		if (row) {
			$('#departmentUpdateWin').window('open');
		} else {
			$.messager.show({
				height : 40,
				msg : 'Please choose an item to edit',
				timeout : 2000,
				showType : 'slide',
				style : {
					right : '',
					top : 0,
					bottom : ''
				}
			});
		}
	});
	$('#departmentUpdateCancel').click(function() {
		$('#departmentUpdateWin').window('close');
	});
	$('#departmentUpdateOk').click(function() {
		var row = $('#department').treegrid('getSelected');
		var parent = $('#departmentUpdateCombobox').combobox('getValue')
		var name = $('#oldDepartment').val()
		var desc = $('#oldDepartmentDesc').val()
		$.ajax({
			type : "POST",
			url : "/BaseSys/departmentUpdate",
			data : {
				id : row.id,
				parent : parent,
				name : name,
				desc : desc
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success) {
					$('#departmentUpdateWin').window('close');
					$('#department').treegrid('reload');
					$.messager.show({
						height : 40,
						msg : 'Edit success',
						timeout : 2000,
						showType : 'slide',
						style : {
							right : '',
							top : 0,
							bottom : ''
						}
					});
				}
			}
		});
	});
});

//**************************************函数**************************************
//部门添加窗口打开
function onDepartmentAddOpen() {
	$('#departmentAddCombobox').combobox('reload', '/BaseSys/departmentRead/0')
	$('#departmentAddCombobox').combobox('clear');
	$('#newDepartment').val('');
	$('#newDepartmentDesc').val('');
};
//部门修改窗口打开
function onDepartmentUpdateOpen() {
	$('#departmentUpdateCombobox').combobox('reload', '/BaseSys/departmentRead/0')
	var row = $('#department').treegrid('getSelected');
	var parent = $('#department').treegrid('getParent', row.id);
	if (parent) {
		$('#departmentUpdateCombobox').combobox('enable');
		$('#departmentUpdateCombobox').combobox('select', parent.name);
		$('#departmentUpdateCombobox').combobox('setValue', parent.id);
	} else {
		$('#departmentUpdateCombobox').combobox('disable');
	};
	$('#oldDepartment').val(row.name);
	$('#oldDepartmentDesc').val(row.desc);
};

//正在编辑的表格var editIndex = undefined;
//表格数据加载完成
function onLoadSuccess(row, data) {

};
//单击表格行事件
function onClickRow(row) {
	if (editIndex != undefined) {
		if (editIndex != row) {
			$('#department').treegrid('endEdit', editIndex.id);
			editIndex = undefined;
		}
	}
};
//双击表格行事件
function onDblClickRow(row) {
	if (editIndex != row) {
		if (editIndex == undefined) {
			editIndex = row;
			$('#department').treegrid('beginEdit', editIndex.id);
		} else {
			if ($('#department').treegrid('validateRow', editIndex.id)) {
				$('#department').treegrid('endEdit', editIndex.id);
				editIndex = row;
				$('#department').treegrid('beginEdit', editIndex.id);
			}
		}
	}

};

// 动态改变表格大小
$(window).resize(function() {
	//	console.log($(window).height() + ' , ' + $(window).width());
	$('#department').datagrid("resize", {
		height : $(window).height() - 90,
		width : $(window).width() - sidebarWidth
	});
	$('#department').datagrid('resize');
});
