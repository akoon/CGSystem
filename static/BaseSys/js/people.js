//tab标识当前页
$('#basePeopleLnk').addClass('active');
$('#peopleLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 157;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
	// **************************************页面初始化**************************************
	// 人员信息表格
	$('#people').datagrid({
		width: _w - sidebarWidth,
		height : _h - 90,
		url : '/BaseSys/peopleDetail',
		method : 'get',
		idField : 'id',
//		toolbar : '#peopleTb',
		autoRowHeight : true,
		striped : true,
		fitColumns: true,
		// scrollbarSize: 400,
		rownumbers : true,
		singleSelect : true,
		columns : [[{
			title : 'id',
			field : 'id',
			hidden : true
		}, {
			field : 'img',
			title : 'Avatar',
			formatter : onPeopleImg
		}, {
			field : 'user',
			title : 'Username',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'name',
			title : 'Name',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'sex',
			title : 'Sex',
			sortable : true,
			editor : 'text',
			formatter : onPeopleSex,
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'phone',
			title : 'Tel',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'email',
			title : 'Email',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'department',
			title : 'Department',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'position',
			title : 'Position',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'seatnumber',
			title : 'Seat',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'birthday',
			title : 'DOB',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'bloodtype',
			title : 'Blood Type',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'constellation',
			title : 'Constellation',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}, {
			field : 'hobby',
			title : 'Hobby',
			sortable : true,
			editor : 'text',
			width : ($(window).width() - sidebarWidth) * 0.1
		}
		]],
		onLoadSuccess : onLoadSuccess,
		onDblClickCell : onClickCell,
		rownumbers : false
		// onDblClickRow:onDblClickRow,
		// onClickRow:onClickRow
	});
	// 人员添加窗口
	$('#peopleAddWin').window({
		width : 340,
		height : 440,
		title : 'Add',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onPeopleAddOpen
	});
	// 人员添加性别combbox
	$('#newSex').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto',
		data : [{
			id : 1,
			name : 'Male'
		}, {
			id : 0,
			name : 'Female'
		}]
	});
	// 人员添加部门combotree
	$('#newDepartment').combotree({
		method : 'get',
		editable : false,
		required : true,
		animate : true
	});
	// 人员添加职位combbox
	$('#newPosition').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		required : true,
		editable : false
	});
	// 人员生日
	$('#newBirthday').datebox({
	    required: false
	});
	
	// 人员血型
	$('#newBloodType').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		panelHeight : 'auto',
		data : [{
			id : 0,
			name : 'O'
		}, {
			id : 1,
			name : 'A'
		}, {
			id : 2,
			name : 'B'
		}, {
			id : 3,
			name : 'AB'
		}, {
			id : 4,
			name : 'Others'
		}]
	});
	
	$('#newConstellation').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		panelHeight : 'auto',
		data : [{
			id : 0,
			name : 'Aries'
		}, {
			id : 1,
			name : 'Taurus'
		}, {
			id : 2,
			name : 'Gemini'
		}, {
			id : 3,
			name : 'Cancer'
		}, {
			id : 4,
			name : 'Leo'
		}, {
			id : 5,
			name : 'Virgo'
		}, {
			id : 6,
			name : 'Libra'
		}, {
			id : 7,
			name : 'Scorpio'
		}, {
			id : 8,
			name : 'Sagittarius'
		}, {
			id : 9,
			name : 'Capricorn'
		}, {
			id : 10,
			name : 'Aquarius'
		}, {
			id : 11,
			name : 'Pisces'
		}]
	});
	
	// 人员体那家确定按钮
	$('#peopleAddOk').linkbutton({
		iconCls : 'icon-ok'
	});
	// 人员添加取消按钮
	$('#peopleAddCancel').linkbutton({
		iconCls : 'icon-cancel'
	});
	// 人员修改窗口
	$('#peopleUpdateWin').window({
		width : 340,
		height : 440,
		title : 'Edit',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onPeopleUpdateOpen
	});
	// 人员修改性别combobox
	$('#oldSex').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto',
		data : [{
			id : 1,
			name : 'Male'
		}, {
			id : 0,
			name : 'Female'
		}]
	});
	// 人员修改部门combotree
	$('#oldDepartment').combotree({
		method : 'get',
		editable : false,
		required : true,
		animate : true
	});
	// 人员修改职位combobox
	$('#oldPosition').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		required : true,
		editable : false
	});
	
	// 人员生日
	$('#oldBirthday').datebox({
	    required: false
	});
	// 人员血型
	$('#oldBloodType').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : false,
		panelHeight : 'auto',
		data : [{
			id : 0,
			name : 'O'
		}, {
			id : 1,
			name : 'A'
		}, {
			id : 2,
			name : 'B'
		}, {
			id : 3,
			name : 'AB'
		}, {
			id : 4,
			name : 'Other'
		}]
	});
	
	$('#oldConstellation').combobox({
		valueField : 'id',
		textField : 'name',
		editable : false,
		panelHeight : 'auto',
		data : [{
			id : 0,
			name : 'Aries'
		}, {
			id : 1,
			name : 'Taurus'
		}, {
			id : 2,
			name : 'Gemini'
		}, {
			id : 3,
			name : 'Cancer'
		}, {
			id : 4,
			name : 'Leo'
		}, {
			id : 5,
			name : 'Virgo'
		}, {
			id : 6,
			name : 'Libra'
		}, {
			id : 7,
			name : 'Scorpio'
		}, {
			id : 8,
			name : 'Sagittarius'
		}, {
			id : 9,
			name : 'Capricorn'
		}, {
			id : 10,
			name : 'Aquarius'
		}, {
			id : 11,
			name : 'Pisces'
		}]
	});
	
	// 人员修改确定按钮
	$('#peopleUpdateOk').linkbutton({
		iconCls : 'icon-ok'
	});
	// 人员修改取消按钮
	$('#peopleUpdateCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	// 图片上传窗口
	$('#peopleImgWin').window({
		width : 280,
		height : 170,
		title : 'Image Upload',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onPeopleImgWinOpen
	});
	// 图片上传确定按钮
	$('#peopleImgOk').linkbutton({
		iconCls : 'icon-ok'
	});
	// 图片上传取消按钮
	$('#peopleImgCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	// **************************************表单验证**************************************
	$('.peopleUser').validatebox({
		required : true
	});
	$('.peopleName').validatebox({
		required : true
	});
	$('.peopleEmail').validatebox({
		required : true,
		validType : 'email'
	});
	$.extend($.fn.validatebox.defaults.rules, {
		phone : {
			validator : function(value, param) {
				var patrn = eval("/^[1][0-9]{" + (param[0] - 1) + "}$/");
				if (patrn.exec(value)) {
					return true
				} else {
					return false
				};
			},
			message : '请输入正确的电话号码'
		}
	});
	// **************************************Toolbar操作**************************************
	// —--------------添加行
	$('#peopleAdd').click(function() {
		$('#peopleAddWin').window('open');
	});
	$('#peopleAddCancel').click(function() {
		$('#peopleAddWin').window('close');
	});
	$('#peopleAddOk').click(function() {
		var sex = $('#newSex').combobox('getValue')
		var department = $('#newDepartment').combobox('getValue')
		var position = $('#newPosition').combobox('getValue')
		var birthday = $('#newBirthday').datebox('getValue');
		var bloodtype = $('#newBloodType').combobox('getValue');
		var constellation = $('#newConstellation').combobox('getValue');
		var hobby = $('#newHobby').val();
		$.ajax({
			type : "POST",
			url : "/BaseSys/peopleCreate",
			data : {
				user : $('#newUser').val(),
				name : $('#newName').val(),
				sex : sex,
				phone : $('#newPhone').val(),
				email : $('#newEmail').val(),
				department : department,
				position : position,
				seatnumber: $('#newSeatnumber').val(),
				birthday:birthday,
				bloodtype:bloodtype,
				constellation:constellation,
				hobby:hobby
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success) {
					$('#peopleAddWin').window('close');
					$('#people').datagrid('reload');
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
				}else{
					$.messager.show({
						height : 40,
						msg : 'Insert Failed',
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
	// —--------------删除行
	$('#peopleDelete').click(function() {
		var row = $('#people').datagrid('getSelected');
		if (row) {
			$.messager.confirm('Delete', 'Are you sure you want to delete this item？', function(r) {
				if (r) {
					$.ajax({
						type : "POST",
						url : "/BaseSys/peopleDestroy",
						data : {
							id : row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");
							if (json.success) {
								$('#people').datagrid('reload');
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
							}
						}
					});
				}
			});

		} else {
			$.messager.show({
				height : 40,
				msg : 'Choose an item you want to detele',
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

	// —--------------修改行
	$('#peopleUpdate').click(function() {
		var row = $('#people').datagrid('getSelected');
		if (row) {
			$('#peopleUpdateWin').window('open');
		} else {
			$.messager.show({
				height : 40,
				msg : 'Choose an item you want to edit',
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
	$('#peopleUpdateCancel').click(function() {
		$('#peopleUpdateWin').window('close');
	});
	$('#peopleUpdateOk').click(function() {
		var row = $('#people').datagrid('getSelected');
		var sex = $('#oldSex').combobox('getValue');
		var department = $('#oldDepartment').combobox('getValue');
		var position = $('#oldPosition').combobox('getValue');
		var user = $('#oldUser').val();
		var name = $('#oldName').val();
		var phone = $('#oldPhone').val();
		var email = $('#oldEmail').val();
		var seatnumber = $('#oldSeatnumber').val();
		var birthday = $('#oldBirthday').datebox('getValue');
		var bloodtype = $('#oldBloodType').combobox('getValue');
		var constellation = $('#oldConstellation').combobox('getValue');
		var hobby = $('#oldHobby').val();
		$.ajax({
			type : "POST",
			url : "/BaseSys/peopleUpdate",
			data : {
				id : row.id,
				user : user,
				name : name,
				sex : sex,
				phone : phone,
				email : email,
				department : department,
				position : position,
				'seatnumber' : seatnumber,
				birthday:birthday,
				bloodtype:bloodtype,
				constellation:constellation,
				hobby:hobby
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success) {
					$('#peopleUpdateWin').window('close');
					$('#people').datagrid('reload');
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
				else{
					$.messager.show({
						height : 40,
						msg : 'Insert incorrect',
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

	$('#peopleImgCancel').click(function() {
		$('#peopleImgWin').window('close');
	});

	$("#peopleImgOk").click(function() {
		var row = $('#people').datagrid('getSelected');
		var file = $("#peopleImage").val();
		if (file == "") {
			alert("Please choose an image you want to upload");
			return;
		} else {
			$.ajaxFileUpload({
				url : '/BaseSys/peopleImg',
				secureuri : false,
				fileElementId : "peopleImage", // file的id
				dataType : "json",
				data : {
					id : row.id
				}, // 返回数据类型为文本
				success : function(data, status) {
					if (data.sucess) {
						$('#peopleImgWin').window('close');
						$('#people').datagrid('reload');
						$.messager.show({
							height : 40,
							msg : 'Image upload success',
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
			})
		}
	})
});

// **************************************函数**************************************
// 人员管理头像显示
function onPeopleImg(value, rowData, rowIndex) {
	if (rowData.img) {
		return '<img id="peopleImg" class="thum" src="' + rowData.img + '" style="height:50px;">';
	} else {
		return '<img id="peopleImg" class="thum" src="/static/pillars/img/user.png" style="height:50px;">';

	}

};
// 人员管理性别显示
function onPeopleSex(value, rowData, rowIndex) {
	if (value == 0) {
		return 'Female'
	} else {
		return 'Male'
	}
};
// 人员添加窗口打开
function onPeopleAddOpen() {
	$('#newDepartment').combobox('clear');
	$('#newPosition').combobox('clear');
	$('#newDepartment').combotree('reload', '/BaseSys/departmentRead');
	$('#newPosition').combobox('reload', '/BaseSys/positionRead');
	$('#newSex').combobox('clear');
	$('#newUser').val('');
	$('#newName').val('');
	$('#newPhone').val('');
	$('#newEmail').val('');
	$('#newSeatnumber').val('');
	$('#newBirthday').datebox('clear');
	$('#newBloodType').combobox('clear');
	$('#newConstellation').combobox('clear');
	$('#newHobby').val('');
};
// 人员修改窗口打开
function onPeopleUpdateOpen() {
	$('#oldDepartment').combotree('reload', '/BaseSys/departmentRead');
	$('#oldPosition').combobox('reload', '/BaseSys/positionRead');
	var row = $('#people').datagrid('getSelected');
	$('#oldUser').val(row.user);
	$('#oldName').val(row.name);
	$('#oldPhone').val(row.phone);
	$('#oldEmail').val(row.email);
	$('#oldSeatnumber').val(row.seatnumber);
	if (row.sex == 0) {
		$('#oldSex').combobox('select', 'Female');
	} else {
		$('#oldSex').combobox('select', 'Male');
	};
	$('#oldDepartment').combotree('setValue', row.department);
	$('#oldPosition').combobox('select', row.position);
	$('#oldBirthday').datebox('clear');
	$('#oldBloodType').combobox('clear');
	$('#oldConstellation').combobox('clear');
	$('#oldHobby').val(row.hobby);
};

// 正在编辑的表格
var editIndex = undefined;
// 表格数据加载完成
function onLoadSuccess(row, data) {

};
function onClickCell(rowIndex, field, value) {
	if (field == 'img') {
		// $('#peopleImgWin').window('open');
		// 图片上传窗口 chuanqing.wu
		var row = $('#people').datagrid('getSelected');
		if (row != null) {

			$('#peopleImgWin').window('open');
		} else {
			$.messager.show({
				height : 40,
				msg : 'Choose an item to upload avatar image',
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
};
// 单击表格行事件
function onClickRow(row) {
	if (editIndex != undefined) {
		if (editIndex != row) {
			$('#people').datagrid('endEdit', editIndex.id);
			editIndex = undefined;
		}
	}
};
// 双击表格行事件
function onDblClickRow(row) {
	if (editIndex != row) {
		if (editIndex == undefined) {
			editIndex = row;
			$('#people').datagrid('beginEdit', editIndex.id);
		} else {
			if ($('#people').datagrid('validateRow', editIndex.id)) {
				$('#people').datagrid('endEdit', editIndex.id);
				editIndex = row;
				$('#people').datagrid('beginEdit', editIndex.id);
			}
		}
	}

};

// 图片上传窗口打开
function onPeopleImgWinOpen() {

};

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#people').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth
		});
	$('#people').datagrid('resize');
});