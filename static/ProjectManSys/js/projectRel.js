//tab标识当前页
$('#projectRelLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

var listview = $.extend({}, $.fn.datagrid.defaults.view, {
	renderRow : function(target, fields, frozen, rowIndex, rowData) {
		var v = [];
		for (var i = 0; i < fields.length; i++) {
			if (i < 2) {
				v.push('<td  style="display:none;" field="' + fields[i] + '">');
			} else {
				v.push('<td   field="' + fields[i] + '">');
			}
			v.push('<div class="datagrid-cell datagrid-cell-c1-' + fields[i]
					+ '" style=";height:auto;">' + rowData[fields[i]]
					+ '</div>')
			v.push('</td>');
		}
		return v.join('')
	},
	onAfterRender : function(target) {
		var view = $.data(target, 'datagrid').dc.view;

	}

});

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w);

$(document).ready(function() {
	//**************************************页面初始化**************************************
	
	
	$('.assets-sider-bar').css({
		height : _h - 70
	});

	$('.panel.datagrid').css({
		width : "auto"
	});
	
	// 左侧选择树
	$('#groupTree').tree({
				method : 'get',
				url : '/ProjectManSys/taskGroupTree/' + $('#projectId').html(),
				valueField : 'id',
				textField : 'name',
				panelHeight : 230,
				onSelect : onGroupSelect
			});
	// 关联资产表格
	$('#RelTaskGroup').datagrid({
		width : "auto",
		height : _h - 40,
		method : 'post',
		idField : 'id',
		autoRowHeight : true,
		striped : true,
		animate : true,
		singleSelect : false,
		columns : [[{
					title : 'id',
					field : 'id',
					hidden : true
				}, {
					title : 'relId',
					field : 'relId',
					hidden : true
				}, {
					field : 'name',
					title : '名称',
					editor : 'text',
					width : 200
				}, {
					field : 'status',
					title : '状态',
					editor : 'text',
					width : 200
				}, {
					field : 'types',
					title : '类型',
					editor : 'text',
					width : 200
				}, {
					field : 'templ',
					title : '模板',
					editor : 'text',
					width : 200
				}, {
					field : 'desc',
					title : '描述',
					editor : 'text',
					width : _w - 1072
				}]]
	});
	
	//关联资产表格
//	$('#RelGroups').datagrid({
//		//width:auto,  
//	    height:_h - 202,
//	    toolbar: '',
//	    //url:'/ProjectManSys/srcTaskGroupRead/',
//	    method:'get',
//	    idField:'id',
//	    autoRowHeight: true,
//	    striped:true,
//	    rownumbers:true,
//	    singleSelect:true,
//	    columns:[[ 
//	        {title:'id',field:'id',hidden:true},  
//	        {field:'name',title:'资产',width:230}
//	        
//		]],	  
//		queryParams: {
//			projectId:$('#projectId').html()
//		},
//    	onClickRow:onSrcGroupSelect
//	});
	
	
//	
	// 资产添加窗口
	$('#prelTaskGroupAddWin').window({
		width : 300,
		height : 400,
		title : '添加关联资产',
		modal : true,
		closed : true,
		resizable : false,
		collapsible : false,
		minimizable : false,
		maximizable : false,
		onOpen : onPrelTaskGroupAddWinOpen
	});

	// 关联资产combobox
	$('#relTaskGroupCombo').combobox({
		method : 'get',
		valueField : 'id',
		textField : 'name',
		editable : false,
		required : true,
		panelHeight : 'auto'
	});
	
	// 资产添加确定按钮
	$('#relTaskGroupAddOk').linkbutton({
		iconCls : 'icon-ok'
	});

	// 资产添加取消按钮
	$('#relTaskGroupAddCancel').linkbutton({
		iconCls : 'icon-cancel'
	});
	
	// **************************************Toolbar操作**************************************
	// —--------------添加行
	$('#RelTaskGroupAdd').click(function() {
		
		row = $('#groupTree').tree('getSelected');
		
		if(row != null)
		{
			console.log(row.id)
			if(row.id.split('_')[0] == 'tg')
			{
				$('#prelTaskGroupAddWin').window('open');
			}
			else
			{
				$.messager.show({
					height : 40,
					msg : '请选择资产',
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
		else
		{
			$.messager.show({
				height : 40,
				msg : '未选择源资产',
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
	
	$('#relTaskGroupAddCancel').click(function() {
		$('#prelTaskGroupAddWin').window('close');
	});
	
	$('#relTaskGroupAddOk').click(function() {
		
		var srcTg = $('#groupTree').tree('getSelected').id;
		
//		var refTg = $('#relTaskGroupCombo').combobox('getValue');
		var refTgs = $('#relTaskGroupTree').tree('getChecked');
		//js对象转换为json
		refTgs = JSON.stringify(refTgs);
		console.log(refTgs);
		
		if (refTgs.length == 0)
		{
			$.messager.show({
				height : 40,
				msg : '未选择关联资产',
				timeout : 1000,
				showType : 'slide',
				style : {
					right : '',
					top : 0,
					bottom : ''
				}
			});
		}
		else
		{
			$.ajax({
				type : "POST",
				url : "/ProjectManSys/descTaskGroupCreate/",
				data : {
					src : srcTg,
					refs : refTgs
				},
				datatype : "json",
				success : function(data) {
					
					var json = eval("(" + data + ")");
					
					$('#prelTaskGroupAddWin').window('close');
					row = $('#groupTree').tree('getSelected');
					onRelGroupLoad(row.id);
		
					$.messager.show({
						height : 40,
						msg : '成功添加 '+json.successCount+' 条记录',
						timeout : 2000,
						showType : 'slide',
						style : {
							right : '',
							top : 0,
							bottom : ''
						}
					});
					
					
					$('#RelTaskGroup').datagrid('reload');
				}
			});
		}
		
		
		
		
	});
	
	// —--------------删除行
	$('#RelTaskGroupDelete').click(function() {
		
		selectedRows = $('#RelTaskGroup').datagrid('getSelections');
		
		console.log();
		
		if(selectedRows.length != 0)
		{
			console.log();
			
			//js对象转换为json
			selectedRows = JSON.stringify(selectedRows);
		
			$.messager.confirm('确认删除', '你确定要删除该关联？', function(r) {
				if(r) 
				{
					$.ajax({
						type : "POST",
						url : "/ProjectManSys/descTaskGroupDestroy/",
						data : {
							rows : selectedRows
						},
						datatype : "json",
						success : function(data) {
							onRelGroupLoad($('#groupTree').tree('getSelected').id);
							$('#RelTaskGroup').datagrid('reload');
							
							var json = eval("(" + data + ")");
							$.messager.show({
								height : 40,
								msg : "成功删除 "+json.successCount+" 条记录",
								timeout : 1000,
								showType : 'slide',
								style : {
									right : '',
									top : 0,
									bottom : ''
								}
							});
							
						}
					});
				}
			});
			
		}
		else
		{
			$.messager.show({
				height : 40,
				msg : '未选择关联资产',
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


function onPrelTaskGroupAddWinOpen(){
	$('#relTaskGroupCombo').combobox('reload', '/ProjectManSys/descTaskGroupRead/' + $('#projectId').html());
	$('#relTaskGroupCombo').combobox('clear');
	
	initRelTaskGroupTree($('#groupTree').tree('getSelected').id);
}

//源资产点击
//function onSrcGroupSelect(node) {
//	row = $('#groupTree').tree('getSelected');
//	
//	onRelGroupLoad(row.id);
//};

//读取关联资产
function onRelGroupLoad(id) {
	$.ajax({
		type : "GET",
		url : "/ProjectManSys/descTaskGroupDetail/",
		data : {
			id : id
		},
		datatype : "json",
		success : function(data) {
			var json = eval("(" + data + ")");
			$('#RelTaskGroup').datagrid('loadData', {
				total : 0,
				rows : json
			});
		}
	});
}

//读取资产组下的资产
function onGroupSelect(node) {
	var gt = $('#groupTree').tree('getSelected');
	
	$.ajax({
		type : "GET",
		url : "/ProjectManSys/descTaskGroupDetail/",
		data : {
			id : gt.id
		},
		datatype : "json",
		success : function(data) {
			var json = eval("(" + data + ")");
			$('#RelTaskGroup').datagrid('loadData', {
				total : 0,
				rows : json
			});
			
			
		}
	});
	
};

function initRelTaskGroupTree(srcTg)
{
	console.log(srcTg);
	// 关联资产tree
	$('#relTaskGroupTree').tree({
		method : 'get',
		url : '/ProjectManSys/taskGroupTreeRelateable/' + $('#projectId').html() + '/' + srcTg,
		idField:'id',
		treeField:'name',
		width : 300,
		height : 300,
		checkbox : true,
		onlyLeafCheck : true,
		lines : true
	});
}

// 动态改变表格大小
$(window).resize(function(){
//	console.log($(window).height() + ' , ' + $(window).width());
	$('#RelTaskGroup').datagrid("resize", {
			height : $(window).height() - 90,
			width : $(window).width() - sidebarWidth - 260 
		});

});
