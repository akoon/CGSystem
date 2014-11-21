//tab标识当前页
$('#leaveSyslnk').addClass('active');
$('#leaveArchiveLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);

$(document).ready(function() {
//**************************************页面初始化**************************************
	$('#leaveTable').datagrid({
		width:	_w - sidebarWidth,  
	    height:	_h - 90, 
	    url:'/OASys/archivedLeave/',
	    method:'get',
	    idField:'id', 
	    toolbar: '#positionTb',
	    autoRowHeight: true,
	    striped:true,
	    fitColumns: true,
	    //scrollbarSize: 400,
	    rownumbers:true,
	    singleSelect:true,
	    columns:[[ 
	        {title:'id',field:'id',hidden:true},  
	        {field:'username',title:'申请人',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'userid',title:'userId',sortable:false,editor:'text',hidden:true},
	        {field:'reason',title:'请假原因',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.4},
	        {field:'starttime',title:'开始时间',sortable:false,editor:'text',width:($(window).width() - sidebarWidth) * 0.2},
	        {field:'endtime',title:'结束时间',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.2},
	        {field:'registertime',title:'提交时间',sortable:false,editor:'text',width:($(window).width() - sidebarWidth) * 0.15},
	        {field:'status',title:'状态',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'interval',title:'时长',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1}
	        ]],
		rownumbers : false,
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});	
	

});