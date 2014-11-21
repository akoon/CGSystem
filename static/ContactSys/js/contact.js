//tab标识当前页
sidebarWidth = 2;
$(".project-bar").width(sidebarWidth);

$(document).ready(function() {
	var _h = $(window).height();
	var _w = $(window).width();
	// 人员信息表格
	$('#people').datagrid({
		width: _w - sidebarWidth,
		height : _h - 45,
		url : '/ContactSys/people',
		method : 'get',
		idField : 'id',
		autoRowHeight : true,
		striped : true,
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
			width : 140
		}, {
			field : 'name',
			title : 'Name',
			sortable : true,
			editor : 'text',
			width : 110
		}, {
			field : 'sex',
			title : 'Sex',
			sortable : true,
			editor : 'text',
			formatter : onPeopleSex,
			width : 50
		}, {
			field : 'phone',
			title : 'Tel',
			sortable : true,
			editor : 'text',
			width : 130
		}, {
			field : 'email',
			title : 'Email',
			sortable : true,
			editor : 'text',
			width : 240
		}, {
			field : 'department',
			title : 'Department',
			sortable : true,
			editor : 'text',
			width : 120
		}, {
			field : 'position',
			title : 'Position',
			sortable : true,
			editor : 'text',
			width : 160
		}]],
		rownumbers : false
	});
	
});

// 人员管理头像显示
function onPeopleImg(value, rowData, rowIndex) {
	if (rowData.img) {
		return '<img id="peopleImg" class="thum" src="' + rowData.img + '" style="height:50px;">'
	} else {
		return '<img id="peopleImg" class="thum" src="/static/pillars/img/user.png" style="height:50px;">'

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
