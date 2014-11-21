$(document).ready(function() {
//**************************************页面初始化************************************** 
	var _h = $(window).height();
	var _w = $(window).width();
	//Timesheet用户信息表格	
	$('#tsusers').datagrid({
		//width:auto,  
	    height:'auto', 
	    url:'/TimeSheetSys/reportDetail/',
	    method:'get',
	    queryParams:{
	    	uid : $('#uid').html(),
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
	        {field:'date',title:'日期',sortable:true,editor:'text',width:80},
	        {field:'user',title:'用户',sortable:true,editor:'text',width:55},
	        {field:'status',title:'状态',sortable:true,editor:'text',hidden:true},
	        {field:'title',title:'标题',sortable:true,editor:'text',width:550},
	        {field:'startTime',title:'开始时间',sortable:true,editor:'datebox'},
	        {field:'endTime',title:'结束时间',sortable:true,editor:'datebox'},
	        {field:'desc',title:'备注',sortable:true,editor:'text',width:430}
	        
	    ]]
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
});
//**************************************函数**************************************





