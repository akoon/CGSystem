
$('#tsUserLnk').addClass('active');

$(document).ready(function() {
//**************************************页面初始化************************************** 
	var _h = $(window).height();
	var _w = $(window).width();
	//Timesheet用户信息表格	
	$('#tsusers').datagrid({
		width:_w,  
	    height:_h - 60, 
	    url:'/TimeSheetSys/tsusersDetail',  
	    method:'get',
	    idField:'id', 
	    //toolbar: '#tsusersTb',
	    autoRowHeight: true,
	    striped:true,
	    //scrollbarSize: 400,
	    // rownumbers:true,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'first_name',title:'Username',sortable:true,editor:'text',width:300},
	        {field:'email',title:'Address',sortable:false,editor:'text',width:300},
	        {field:'status',title:'Status',sortable:false,editor:'text',width:300},
	        {field:'ops',title:'Operations',sortable:false,editor:'text',width:294}
	    ]]
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//报表生成窗口
	$('#reportWin').window({  
	    width:320,  
	    height:160,
	    title:'Generate report',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false
	});
	//报表生成开始时间DateBox
	$('#startdate').datebox({
	    editable:false  
	});
	//报表生成结束时间DateBox
	$('#enddate').datebox({
	    editable:false  
	});
	//报表生成确定按钮
	$('#reportOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//报表生成取消按钮
	$('#reportCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//报表生成取消
	$('#reportCancel').click( function() {
		$('#reportWin').window('close');
	});
	
	//报表生成确定
	$('#reportOk').click( function() {
		var startdate = $('#startdate').datebox('getValue');
		var enddate = $('#enddate').datebox('getValue');
		if(startdate == '' || enddate == '')
		{
			$.messager.show({
				height:40,
				msg:'Start date and end date cannot be empty',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
		else
		{
			if(startdate > enddate)
			{
				$.messager.show({
					height:40,
					msg:'Start time can not be greater than the end time',
					timeout:2000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
			}
			else
			{
				var row = $('#tsusers').datagrid('getSelected');
				//跳转到报表页面
				//window.location.href='/TimeSheetSys/report/?uid='+ row.id +'&startdate='+ startdate +'&enddate='+ enddate;
				//弹出报表窗口
				window.open ('/TimeSheetSys/report/?uid='+ row.id +'&startdate='+ startdate +'&enddate='+ enddate);
				$('#reportWin').window('close');
			}
		}
	} );
	
	//统计窗口
	$('#statisticWin').window({  
	    width:320,  
	    height:160,
	    title:'Statistics',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false
	});
	
	//报表生成开始时间DateBox
	$('#statisticStart').datebox({
	    editable:false  
	});
	//报表生成结束时间DateBox
	$('#statisticEnd').datebox({
	    editable:false  
	});
	//报表生成确定按钮
	$('#statisticOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//报表生成取消按钮
	$('#statisticCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//报表生成取消
	$('#statisticCancel').click( function() {
		$('#statisticWin').window('close');
	});
	
	//报表生成确定
	$('#statisticOk').click( function() {
		var startdate = $('#statisticStart').datebox('getValue');
		var enddate = $('#statisticEnd').datebox('getValue');
		if(startdate == '' || enddate == '')
		{
			$.messager.show({
				height:40,
				msg:'Start date and end date cannot be empty',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
		else
		{
			if(startdate > enddate)
			{
				$.messager.show({
					height:40,
					msg:'Start time can not be greater than the end time',
					timeout:2000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
			}
			else
			{
				var row = $('#tsusers').datagrid('getSelected');
				//跳转到报表页面
				//window.location.href='/TimeSheetSys/report/?uid='+ row.id +'&startdate='+ startdate +'&enddate='+ enddate;
				//弹出报表窗口
				window.open ('/TimeSheetSys/statistic/?uid='+ row.id +'&startdate='+ startdate +'&enddate='+ enddate);
				$('#statisticWin').window('close');
			}
		}
	} );
	
	//任务统计窗口
	$('#taskStatisticWin').window({  
	    width:320,  
	    height:160,
	    title:'Statistics',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false
	});
	
	//报表生成开始时间DateBox
	$('#taskStatisticStart').datebox({
	    editable:false  
	});
	//报表生成结束时间DateBox
	$('#taskStatisticEnd').datebox({
	    editable:false  
	});
	//报表生成确定按钮
	$('#taskStatisticOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//报表生成取消按钮
	$('#taskStatisticCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	//报表生成取消
	$('#taskStatisticCancel').click( function() {
		$('#taskStatisticWin').window('close');
	});
	//报表生成确定
	$('#taskStatisticOk').click( function() {
		var startdate = $('#taskStatisticStart').datebox('getValue');
		var enddate = $('#taskStatisticEnd').datebox('getValue');
		if(startdate == '' || enddate == '')
		{
			$.messager.show({
				height:40,
				msg:'Start date and end date cannot be empty',
				timeout:2000,
				showType:'slide',
				style:{
					right:'',
					top:0,
					bottom:''
				}
			});
		}
		else
		{
			if(startdate > enddate)
			{
				$.messager.show({
					height:40,
					msg:'Start time can not be greater than the end time',
					timeout:2000,
					showType:'slide',
					style:{
						right:'',
						top:0,
						bottom:''
					}
				});
			}
			else
			{
				//跳转到报表页面
				//window.location.href='/TimeSheetSys/report/?uid='+ row.id +'&startdate='+ startdate +'&enddate='+ enddate;
				//弹出报表窗口
				window.open ('/TimeSheetSys/taskStatistic/?&startdate='+ startdate +'&enddate='+ enddate);
				$('#taskStatisticWin').window('close');
			}
		}
	} );
});
//**************************************函数**************************************
//报表窗口打开
function reportWinOpen(){
//	$('#newName').val('');
//	$('#newDesc').val('');
	
	$('#reportWin').window('open');
	
};

//统计链接窗口打开
function statisticWinOpen(){
	$('#statisticWin').window('open');
	
};

//任务统计链接窗口打开
function taskStatisticWinOpen(){
	$('#taskStatisticWin').window('open');
	
};
