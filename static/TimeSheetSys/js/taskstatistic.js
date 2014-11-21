$(document).ready(function() {
//**************************************页面初始化************************************** 
	var _h = $(window).height();
	var _w = $(window).width();
	//Timesheet用户信息表格	
	$('#statistic').datagrid({
		//width:auto,  
	    height:'auto', 
	    url:'/TimeSheetSys/taskStatisticDetail/',
	    method:'get',
	    queryParams:{
	    	startdate : $('#startdate').html(),
	    	enddate : $('#enddate').html()
	    },
	    //toolbar: '#tsusersTb',
	    autoRowHeight: true,
	    striped:true,
	    //scrollbarSize: 400,
	    rownumbers:true,
	    singleSelect:true,
	    nowrap: false,
	    columns:[[
	    	{field:'taskId',title:'ID',sortable:true,editor:'text',hidden:true},
	    	{field:'task',title:'任务',sortable:true,editor:'text'},
	    	{field:'user',title:'用户',sortable:true,editor:'text'},
	        {field:'hours',title:'时长',sortable:true,editor:'text'}
	        
	        
	    ]]
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
});
//**************************************函数**************************************





