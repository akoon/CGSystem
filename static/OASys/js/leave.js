//tab标识当前页
$('#leaveSyslnk').addClass('active');
$('#leaveLnk').addClass('active');

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
	    url:'/OASys/leaveDetail/',
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
	        {field:'tid',title:'请假类型ID',hidden:true},
	        {field:'type',title:'请假类型',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'reason',title:'请假原因',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.4},
	        {field:'starttime',title:'开始时间',sortable:false,editor:'text',width:($(window).width() - sidebarWidth) * 0.2},
	        {field:'endtime',title:'结束时间',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.2},
	        {field:'registertime',title:'提交时间',sortable:false,editor:'text',width:($(window).width() - sidebarWidth) * 0.15},
	        {field:'status',title:'状态',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'sid',title:'状态ID',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'interval',title:'时长',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.1},
	        {field:'ops',title:'操作',sortable:true,editor:'text',width:($(window).width() - sidebarWidth) * 0.2}
	        
	        ]],
		rownumbers : false
	    //onLoadSuccess:onLoadSuccess,
	    //onDblClickCell:onDblClickCell,
	    //onDblClickRow:onDblClickRow,
	    //onClickRow:onClickRow
	});
	
	//新建假条窗口
	$('#leaveAddWin').window({  
	    width:310,  
	    height:280,  
	    title:'新建请假单',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onLeaveTableOpen
	});
	
	//新建假条类型combbox
	$('#newType').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false,  
		panelHeight: 'auto'
	});
	
	//新建假条开始时间DateBox
	$('#newStartTime').datetimebox({
	    editable:true  
	});
	//新建假条结束时间DateBox
	$('#newEndTime').datetimebox({
	    editable:true  
	});
	
	//新建假条时长numberfield
	$('#newInterval').numberbox({
		min:0,
		value:0
	});
	
	//新建假条确定按钮
	$('#leaveAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//新建假条取消按钮
	$('#leaveAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//修改假条窗口
	$('#leaveEditWin').window({  
	    width:310,  
	    height:280,  
	    title:'修改请假单',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
	    onOpen:onLeaveTableOpen
	});
	
	//修改假条类型combbox
	$('#oldType').combobox({  
	    method:'get',
	    valueField:'id',  
	    textField:'name',   
	    required:true,
	    editable:false,  
		panelHeight: 'auto'
	});
	
	//修改假条开始时间DateBox
	$('#oldStartTime').datetimebox({
	    editable:true  
	});
	//修改假条结束时间DateBox
	$('#oldEndTime').datetimebox({
	    editable:true  
	});
	
	//修改假条时长numberfield
	$('#oldInterval').numberbox({
		min:0,
		value:0
	});
	
	//修改假条确定按钮
	$('#leaveEditOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//修改假条取消按钮
	$('#leaveEditCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
//**************************************表单验证****************************************

//**************************************Toolbar操作*************************************
//—--------------添加行
	$('#leaveAdd').click( function() {			
		$('#leaveAddWin').window('open');
	});
	$('#leaveAddCancel').click( function() {
		$('#leaveAddWin').window('close');
	});
	$('#leaveAddOk').click( function() {
		var type = $('#newType').combobox('getValue');
		
		$.ajax({
			type : "POST",
			url : "/OASys/leaveCreate/",
			data : {
				type: type,
				starttime: $('#newStartTime').datebox('getValue'),
				endtime:   $('#newEndTime').datebox('getValue'),
				reason:		$('#newReason').val(),
				intervalDay:		$('#newIntervalDay').val(),
				intervalHour:		$('#newIntervalHour').val()
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				
				if (json.success){
					$('#leaveAddWin').window('close');
					$('#leaveTable').datagrid('reload');
				}
				
				$.messager.show({
					height:40,
					msg:json.message,
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
		
    } );
    
    //—--------------修改行
	$('#leaveEdit').click( function() {
		var row = $('#leaveTable').datagrid('getSelected');
		
		if(row != null)
		{
			if(row.sid == 1 || row.sid == 2)
			{
				$.messager.show({
					height:40,
					msg:"当前请假单不允许修改.",
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
				$('#leaveEditWin').window('open');
				
				$('#oldType').combobox('select',row.tid);
				$('#oldReason').val(row.reason);
				$('#oldStartTime').datebox("setValue", row.starttime);
				$('#oldEndTime').datebox("setValue", row.endtime);
				var interval = row.interval;
				$('#oldIntervalDay').val(Math.floor(interval / 8));
				$('#oldIntervalHour').val(interval % 8);
				
				
			}
			
		}
		else
		{
			$.messager.show({
				height:40,
				msg:"请选择要修改的行",
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
	$('#leaveEditCancel').click( function() {
		$('#leaveEditWin').window('close');
	});
	$('#leaveEditOk').click( function() {
		var type = $('#oldType').combobox('getValue');
		var row = $('#leaveTable').datagrid('getSelected');
		
		$.ajax({
			type : "POST",
			url : "/OASys/leaveUpdate/",
			data : {
				id: row.id,
				type: type,
				starttime: $('#oldStartTime').datebox('getValue'),
				endtime:   $('#oldEndTime').datebox('getValue'),
				reason:		$('#oldReason').val(),
				intervalDay:		$('#oldIntervalDay').val(),
				intervalHour:		$('#oldIntervalHour').val()
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");
				
				if (json.success){
					$('#leaveEditWin').window('close');
					$('#leaveTable').datagrid('reload');
				}
				
				$.messager.show({
					height:40,
					msg:json.message,
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
    } );
    
    //删除行
    $('#leaveDestroy').click( function() {
    	var row = $('#leaveTable').datagrid('getSelected');
		if(row == null)
		{
			$.messager.show({
				height:40,
				msg:"请选择要删除的请假单.",
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
			$.messager.confirm("删除", "是否删除请假单.", function (r) {  
		        if (r) {  
		            $.ajax({
						type : "POST",
						url : "/OASys/leaveDestroy/",
						data : {
							id: row.id
						},
						datatype : "json",
						success : function(data) {
							var json = eval("(" + data + ")");
							
							$.messager.show({
								height:40,
								msg:json.message,
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
					$('#leaveTable').datagrid('reload');
		        }  
		    });
		}
    });
});
//**************************************函数**************************************

function onLeaveTableOpen(){
	$('#newType').combobox('reload','/OASys/leavetypeRead');
	
};
		
//提交假条
function submitLeave(id){
	$.messager.confirm("提交", "是否确认提交.", function (r) {  
        if (r) {
        	$.ajax({
				type : "POST",
				url : "/OASys/leaveCommit/",
				data : {
					id: id
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");
					
					$.messager.show({
						height:40,
						msg:json.message,
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
			$('#leaveTable').datagrid('reload');
        }
    });
	
};

//审核通过
function leaveJudgementAck(id){
	$.messager.confirm("审核通过", "是否设定为审核通过.", function (r) {  
        if (r) {  
            $.ajax({
				type : "POST",
				url : "/OASys/leaveJudge/",
				data : {
					id: id,
					option: 'ack'
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");
					
					$.messager.show({
						height:40,
						msg:json.message,
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
			$('#leaveTable').datagrid('reload');
        }  
    });  

};

//审核不通过
function leaveJudgementNeg(id){
	$.messager.confirm("审核不通过", "是否设定为审核不通过.", function (r) {  
        if (r) {  
            $.ajax({
				type : "POST",
				url : "/OASys/leaveJudge/",
				data : {
					id: id,
					option: 'neg'
				},
				datatype : "json",
				success : function(data) {
					var json = eval("(" + data + ")");
					
					$.messager.show({
						height:40,
						msg:json.message,
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
			$('#leaveTable').datagrid('reload');
        }  
    });  

};


