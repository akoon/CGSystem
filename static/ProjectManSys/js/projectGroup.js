//tab标识当前页
$('#projectGroupLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
groupWidth = 265;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

var thumview = $.extend({}, $.fn.datagrid.defaults.view, {
	render : function(target, container, frozen) {
		var state = $.data(target, 'datagrid');
		var rows = state.data.rows;
		var data = state.data;
		var view = [];
		view.push('<ul id="layoutTarget" class="layout newview">');
		for (var i = 0; i < rows.length; i++) {
			view.push('<li id="group-thum-' + rows[i].id + '" class="project-img" row-id=' + rows[i].id + '>');
			if (rows[i].img) {
				view.push('<img src="' + rows[i].img + '">');
			} else {
				view.push('<img src="/static/pillars/img/unload.jpg">');
			}
			view.push('<span class="project-name">' + rows[i].name + '</span>');
			view.push('</li>');
		}
		view.push('</ul>');
		$(container).html(view.join(''));
	},
	onAfterRender : function(target) {
		var view = $.data(target, 'datagrid').dc.view;
		view.find('li').bind('click', {}, function(e) {
			if ($(this).hasClass('datagrid-row-selected')) {
				$(this).removeClass('datagrid-row-selected');
			} else {
				view.find('li.datagrid-row-selected').removeClass('datagrid-row-selected');
				$(this).addClass('datagrid-row-selected');
			}
		});
		view.find('li').bind('dblclick', {}, function(e) {
			if ($(this).hasClass('datagrid-row-selected')) {

			} else {
				view.find('li.datagrid-row-selected').removeClass('datagrid-row-selected');
				$(this).addClass('datagrid-row-selected');
			}
			$('#groupImgWin').window('open');
		});
		var s = $('#projectGroup').datagrid('getSelected');
		if (s) {
			$(target).datagrid('selectThum', s.id);
		}
	}
	,

});
var listview = $.extend({}, $.fn.datagrid.defaults.view, {
	renderRow : function(target, fields, frozen, rowIndex, rowData) {
		var v = [];
		for (var i = 0; i < fields.length; i++) {
			if (i < 2) {
				v.push('<td  style="display:none;" field="' + fields[i] + '">');
			} else {
				v.push('<td   field="' + fields[i] + '">');
			}
			v.push('<div class="datagrid-cell datagrid-cell-c1-' + fields[i] + '" style=";height:auto;">' + rowData[fields[i]] + '</div>')
			v.push('</td>');
		}
		return v.join('')
	},
	onAfterRender : function(target) {
		var view = $.data(target, 'datagrid').dc.view;

	}
	,
});
$.extend($.fn.datagrid.methods, {
	selectThum : function(jq, thumIndex) {
		return jq.each(function() {
			var view = $.data(this, 'datagrid').dc.view;
			var li = view.find('li.project-img')
			for ( i = 0; i < li.length; i++) {
				var id = li[i].getAttribute('row-id');
				if (id == thumIndex) {
					li[i].className = 'project-img datagrid-row-selected'
				}
			}
		});
	}
	,
});
$.extend($.fn.datagrid.methods, {
	deleteOne : function(jq, Index) {
		return jq.each(function() {
			var view = $.data(this, 'datagrid').dc.view;
			if ($("#display .l-btn-empty").hasClass('icon-display-list')) {
				view.find('#datagrid-row-r1-2-' + Index).remove();
			};
		});
	}
	,
});
$.extend($.fn.datagrid.methods, {
	updateOne : function(jq, info) {
		return jq.each(function() {
			var view = $.data(this, 'datagrid').dc.view;
			if ($("#display .l-btn-empty").hasClass('icon-display-list')) {
				var rindex = info['index'];
				var row = info['row'];
				var tr = view.find('#datagrid-row-r1-2-' + rindex);
				var td = tr.children();
				for (var i = 2; i < td.length; i++) {
					var field = td[i].getAttribute('field');
					var div = td.find('div.datagrid-cell-c1-' + field);
					div.html(row[field]);
				};
			};
		});
	}
	,
});

$(document).ready(function() {
	// **************************************视图转换**************************************
	$("#display").click(function() {
		if ($("#display .l-btn-empty").hasClass('icon-display-list')) {
			$("#display .l-btn-empty").removeClass('icon-display-list');
			$("#display .l-btn-empty").addClass('icon-display-thumbnail');
			var sg = $('#groupTree').tree('getSelected');
			$('#projectGroup').datagrid('options').view = thumview;
			if (sg) {
				onLoad(sg.id);
			};
		} else {
			$("#display .l-btn-empty").removeClass('icon-display-thumbnail');
			$("#display .l-btn-empty").addClass('icon-display-list');
			var s2 = $('li.datagrid-row-selected').attr('row-id');
			var sg2 = $('#groupTree').tree('getSelected');
			$('#projectGroup').datagrid('options').view = listview;
			if (sg2) {
				onLoad(sg2.id);
			};
			if (s2) {
				$('#projectGroup').datagrid('selectRecord', s2);
			};
		}
	});
	// **************************************页面初始化**************************************
	var _h = $(window).height();
	var _w = $(window).width();

	$('.assets-sider-bar').css({
		height : _h - 72
		,
	});

	// 资产信息表格
	$('#projectGroup').datagrid({
		width : _w - sidebarWidth - groupWidth,
		height : _h - 90,
		method : 'post',
		idField : 'id',
		toolbar : '#projectGroupTb',
		autoRowHeight : true,
		striped : true,
		animate : false,
		singleSelect : true,
		fitColumns : true,
		columns : [[{
			title : 'id',
			field : 'id',
			hidden : true
		}, {
			title : 'img',
			field : 'img',
			hidden : true
		}, {
			field : 'name',
			title : 'Name',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}, {
			field : 'namedesc',
			title : 'Chinese Name',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}, {
			field : 'status',
			title : 'Status',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}, {
			field : 'type',
			title : 'Type',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}, {
			field : 'templ',
			title : 'Template',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}, {
			field : 'desc',
			title : 'Description',
			editor : 'text',
			width : ($(window).width() - sidebarWidth - groupWidth) * 0.2
		}]],
		view : listview
	});
	// 左侧选择树
	$('#groupTree').tree({
		method : 'get',
		url : '/ProjectManSys/groupRead/' + $('#projectId').html(),
		valueField : 'id',
		textField : 'name',
		panelHeight : 230,
		onSelect : onGroupSelect
		,
	});
	// 资产添加窗口
	$('#projectGroupAddWin').window({
		width : 340,
		height : 320,
		title : 'Add',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onprojectGroupAddOpen
	});

	// 类型combbox
	$('#newTypes').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto'
	});

	// 状态combbox
	$('#newStatus').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto'
	});

	// 模板combbox
	$('#newTempl').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		panelHeight : 'auto'
	});

	// 资产组combbox
	$('#newGroup').combotree({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 170
	});

	// 资产添加确定按钮
	$('#projectGroupAddOk').linkbutton({
		iconCls : 'icon-ok'
	});

	// 资产添加取消按钮
	$('#projectGroupAddCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	// 资产修改窗口
	$('#projectGroupUpdateWin').window({
		width : 340,
		height : 320,
		title : 'Edit',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onprojectGroupUpdateOpen
	});

	// 类型combbox
	$('#oldTypes').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto'
	});

	// 状态combbox
	$('#oldStatus').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto'
	});

	// 模板combbox
	$('#oldTempl').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		panelHeight : 'auto'
	});

	// 资产修改确定按钮
	$('#projectGroupUpdateOk').linkbutton({
		iconCls : 'icon-ok'
	});

	// 资产修改取消按钮
	$('#projectGroupUpdateCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	// 图片上传窗口
	$('#groupImgWin').window({
		width : 280,
		height : 170,
		title : 'Image Upload',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onClose : onGroupImgClose
	});
	// 图片上传确定按钮
	$('#groupImgOk').linkbutton({
		iconCls : 'icon-ok'
	});
	// 图片上传取消按钮
	$('#groupImgCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	//资产组添加窗口
	$('#groupAddWin').window({
		width : 290,
		height : 250,
		title : 'Add',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onGroupAddOpen
	});
	//资产组添加combobox
	$('#newParentGroup').combotree({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : false,
		panelHeight : 170
	});

	//资产组添加确定按钮
	$('#groupAddOk').linkbutton({
		iconCls : 'icon-ok'
	});
	//资产组添加取消按钮
	$('#groupAddCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	//资产组修改窗口
	$('#groupUpdateWin').window({
		width : 290,
		height : 250,
		title : 'Edit',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onGroupUpdateOpen
	});

	//资产组修改combobox
	$('#oldParentGroup').combotree({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : false,
		panelHeight : 170
	});

	//资产组修改确定按钮
	$('#groupUpdateOk').linkbutton({
		iconCls : 'icon-ok'
	});
	//资产组修改取消按钮
	$('#groupUpdateCancel').linkbutton({
		iconCls : 'icon-cancel'
	});

	// **************************************表单验证**************************************
	$('.NameInput').validatebox({
		required : true
	});

	// **************************************Toolbar操作**************************************
	// —--------------添加资产
	$('#projectGroupAdd').click(function() {
		$('#projectGroupAddWin').window('open');
	});
	$('#projectGroupAddCancel').click(function() {
		$('#projectGroupAddWin').window('close');
	});
	$('#projectGroupAddOk').click(function() {
		var name = $('#newName').val();
		var namedesc = $('#newNameDesc').val();
		var type = $('#newTypes').combobox('getValue');
		var status = $('#newStatus').combobox('getValue');
		var templ = $('#newTempl').combobox('getValue');
		var group = $('#newGroup').combotree('getValue');
		var desc = $('#newDesc').val();

		$.ajax({
			type : "POST",
			url : "/ProjectManSys/taskGroupCreate",
			data : {
				name : name,
				namedesc : namedesc,
				type : type,
				status : status,
				templ : templ,
				group : group,
				desc : desc,
				project : $('#projectId').html()

			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success) {
					$('#projectGroupAddWin').window('close');
					var gt = $('#groupTree').tree('getSelected');
					if (gt != null && gt.id == group) {
						onLoad(gt.id);
					}
					$.messager.show({
						height : 40,
						msg : json.message,
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
						msg : json.message,
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

	// —--------------删除资产
	$('#projectGroupDelete').click(function() {
		if ($("#display .l-btn-empty").hasClass('icon-display-list')) {
			var row = $('#projectGroup').datagrid('getSelected');
		}
		if (row) {
			try {
				id = parseInt(row.id);
			} catch (e) {
				id = 0
			};
			if (id > 0) {
				$.messager.confirm('delete', 'Are you sure you want to delete this item？', function(r) {
					if (r) {
						$.ajax({
							type : "POST",
							url : "/ProjectManSys/taskGroupDestroy",
							data : {
								id : row.id
							},
							datatype : "json",
							success : function(data) {
								var json = eval("(" + data + ")");
								if (json.success) {
									var index = $('#projectGroup').datagrid('getRowIndex', row);
									$('#projectGroup').datagrid('deleteOne', index);
									$('#projectGroup').datagrid('unselectAll');
									$.messager.show({
										height : 40,
										msg : 'delete success',
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
					msg : 'delete not allowed',
					timeout : 2000,
					showType : 'slide',
					style : {
						right : '',
						top : 0,
						bottom : ''
					}
				});
			}
		} else {
			$.messager.show({
				height : 40,
				msg : 'Please select the data to be deleted',
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

	// —--------------修改资产
	$('#projectGroupUpdate').click(function() {
		var row = $('#projectGroup').datagrid('getSelected');
		if (row) {
			try {
				id = parseInt(row.id);
			} catch (e) {
				id = 0
			};
			if (id > 0) {
				if ($("#display .l-btn-empty").hasClass('icon-display-list')) {
					$('#projectGroupUpdateWin').window('open');
				}
			} else {
				$.messager.show({
					height : 40,
					msg : 'delete not allowed',
					timeout : 2000,
					showType : 'slide',
					style : {
						right : '',
						top : 0,
						bottom : ''
					}
				});
			}

		} else {
			$.messager.show({
				height : 40,
				msg : 'Please select the data to be edit',
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
	$('#projectGroupUpdateCancel').click(function() {
		$('#projectGroupUpdateWin').window('close');
	});
	$('#projectGroupUpdateOk').click(function() {
		var row = $('#projectGroup').datagrid('getSelected');
		var name = $('#oldName').val();
		var namedesc = $('#oldNameDesc').val();
		var type = $('#oldTypes').combobox('getValue');
		var status = $('#oldStatus').combobox('getValue');
		var templ = $('#oldTempl').combobox('getValue');
		// var group = $('#oldGroup').combobox('getValue');
		var desc = $('#oldDesc').val();

		$.ajax({
			type : "POST",
			url : "/ProjectManSys/taskGroupUpdate",
			data : {
				name : name,
				namedesc : namedesc,
				type : type,
				status : status,
				templ : templ,
				// group: group,
				desc : desc,
				// project: $('#projectId').html(),
				id : row.id
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (json.success) {
					$('#projectGroupUpdateWin').window('close');
					var index = $('#projectGroup').datagrid('getRowIndex', row);
					$('#projectGroup').datagrid('updateOne', {
						index : index,
						row : {
							name : name,
							namedesc : namedesc,
							type : $('#oldTypes').combobox('getText'),
							status : $('#oldStatus').combobox('getText'),
							templ : $('#oldTempl').combobox('getText'),
							desc : desc
							,
						}
					});
					$('#projectGroup').datagrid('unselectAll');
					$.messager.show({
						height : 40,
						msg : 'edit success',
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
	});

	$('#groupImgCancel').click(function() {
		$('#groupImgWin').window('close');
	});

	$("#groupImgOk").click(function() {
		var id = $('li.datagrid-row-selected').attr('row-id');
		var file = $("#groupImage").val();
		if (file == "") {
			alert("Please select an image to upload");
			return;
		} else {
			$.ajaxFileUpload({
				url : '/ProjectManSys/taskGroupImg',
				secureuri : false,
				fileElementId : "groupImage", // file的id
				dataType : "json",
				data : {
					id : id
				}, // 返回数据类型为文本
				success : function(data, status) {
					if (data.sucess) {
						$('#groupImgWin').window('close');
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
	});

	// —--------------添加资产组
	$('#groupAdd').click(function() {
		$('#groupAddWin').window('open');
	});
	$('#groupAddCancel').click(function() {
		$('#groupAddWin').window('close');
	});
	$('#groupAddOk').click(function() {
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/groupCreate/",
			data : {
				project : $('#projectId').html(),
				parent : $('#newParentGroup').combotree('getValue'),
				name : $('#newGroupName').val()
				//				desc:		$('#newGroupDesc').val()

			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (true) {
					$('#groupAddWin').window('close');
					$('#groupTree').tree('reload');
					$.messager.show({
						height : 40,
						msg : json.message,
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
	// —--------------修改资产组
	$('#groupUpdate').click(function() {
		var row = $('#groupTree').tree('getSelected');
		if (row) {
			$('#groupUpdateWin').window('open');
		} else {
			$.messager.show({
				height : 40,
				msg : 'Please select the data to be edit',
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
	$('#groupUpdateCancel').click(function() {
		$('#groupUpdateWin').window('close');
	});
	$('#groupUpdateOk').click(function() {
		$.ajax({
			type : "POST",
			url : "/ProjectManSys/groupUpdate/",
			data : {
				id : $('#groupTree').tree('getSelected').id,
				parent : $('#oldParentGroup').combotree('getValue'),
				name : $('#oldGroupName').val()
				//				desc:		$('#oldGroupDesc').val()

			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				if (true) {
					$('#groupUpdateWin').window('close');
					$('#groupTree').tree('reload');
					$.messager.show({
						height : 40,
						msg : json.message,
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
	// —--------------删除资产组
	$('#groupDelete').click(function() {
		var row = $('#groupTree').tree('getSelected');
		if (row) {
			$.messager.confirm('delete', 'Are you sure you want to delete this item？', function(r) {
				if (r) {
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/groupDestroy/",
						data : {
							id : row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");
							if (json.success) {
								$('#groupTree').tree('reload');
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
				msg : 'Please select the data to be deleted',
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

});
// **************************************函数**************************************
// 资产添加窗口打开
function onprojectGroupAddOpen() {
	$('#newTypes').combobox('reload', '/ProjectManSys/typesRead/2');
	$('#newTypes').combobox('clear');

	$('#newStatus').combobox('reload', '/ProjectManSys/statusRead/2');
	$('#newStatus').combobox('clear');

	$('#newTempl').combobox('reload', '/ProjectManSys/templRead/0');
	$('#newTempl').combobox('clear');

	$('#newGroup').combotree('reload', '/ProjectManSys/groupRead/' + $('#projectId').html());
	$('#newGroup').combotree('clear');

	$('#newName').val('');
	$('#newDesc').val('');
};

// 资产修改窗口打开
function onprojectGroupUpdateOpen() {
	var row = $('#projectGroup').datagrid('getSelected');

	$('#oldTypes').combobox('reload', '/ProjectManSys/typesRead/2');
	$('#oldTypes').combobox('select', row.type);

	$('#oldStatus').combobox('reload', '/ProjectManSys/statusRead/2');
	$('#oldStatus').combobox('select', row.status);

	$('#oldTempl').combobox('reload', '/ProjectManSys/templRead/0');
	$('#oldTempl').combobox('select', row.templ);

	$('#oldName').val(row.name);
	$('#oldNameDesc').val(row.namedesc)
	$('#oldDesc').val(row.desc);
};

function onGroupImgClose() {
	var gt = $('#groupTree').tree('getSelected');
	onLoad(gt.id);
};

function onGroupSelect(node) {
	onLoad(node.id);
};

function onLoad(id) {
	$.ajax({
		type : "POST",
		url : "/ProjectManSys/taskGroupDetail/",
		data : {
			id : -id
			,
		},
		datatype : "json",
		success : function(data) {
			var json = eval("(" + data + ")");
			$('#projectGroup').datagrid('loadData', {
				total : 0,
				rows : json
			});
		}
	});
}

//资产组添加窗口打开
function onGroupAddOpen() {
	$('#newGroupName').val('');
	//	$('#newDesc').val('');
	$('#newParentGroup').combotree('reload', '/ProjectManSys/groupRead/' + $('#projectId').html());
	$('#newParentGroup').combotree('clear');
};

//资产组修改窗口打开
function onGroupUpdateOpen() {
	var row = $('#groupTree').tree('getSelected');

	console.log(row);

	$('#oldParentGroup').combotree('reload', '/ProjectManSys/groupRead/' + $('#projectId').html());
	$('#oldParentGroup').combotree('clear');

	//	$('#oldParentGroup').combotree('setValue', row.id);
	$('#oldGroupName').val(row.text);
	//	$('#oldGroupDesc').val(row.desc);
};

// 动态改变表格大小
$(window).resize(function() {
	console.log($(window).height() + ' , ' + $(window).width());
	$('.project-content').width($(window).width() - sidebarWidth);
	$('.project-content').height($(window).height() - 90);

	$('#projectGroup').datagrid("resize", {
		height : $(window).height() - 90,
		width : $(window).width() - sidebarWidth - groupWidth
	});
});
