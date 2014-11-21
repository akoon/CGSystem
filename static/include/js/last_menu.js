$(document).ready(function(){
	$.extend($.fn.validatebox.defaults.rules, {
		equals: {
			validator: function(value,param){
					return value == $(param[0]).val();
				},
			message: '两次密码不相同！'
		}
	});

	$('#changepasswd').dialog({
		modal: true,
		closed: true,
		buttons: [{
				text:'Ok',
				iconCls:'icon-ok',
				handler:function(){
					$('#ff').form('submit', {
						url: '/changepasswd/',
						onSubmit: function(){
						var isValid = $(this).form('validate');
						if (!isValid){
							showmsg('校验失败！');
						}
						return isValid;
						},
						success: function(data){
							var json = eval("(" + data + ")");
							if(json.success){
								alert('修改密码后，请重新登录！');
								location.href = '/logout';
							}else{
								showmsg('旧密码不正确，请重新输入！');
								$('#ff').form('clear');
							}
						}
					});
				}
			},{
				text:'Cancel',
				handler:function(){
					$('#ff').form('clear');
				}
			}]
	});
	
	function showmsg(m){
		$.messager.show({
			height:40,
			msg:m,
			timeout:2000,
			showType:'slide',
			style:{
				right:'',
				top:0,
				bottom:''
			}
		});
	}
	
	//反馈添加窗口
	$('#reportAddWin').window({  
	    width:640,  
	    height:480,  
	    title:'提交反馈',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
//	    onOpen:onprojectTaskAddOpen   
	});
	//反馈添加确定按钮
	$('#reportAddOk').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	//反馈添加取消按钮
	$('#reportAddCancel').linkbutton({  
	    iconCls: 'icon-cancel'  
	});
	
	//反馈意见textarea
	$('#reportContent').width($('#reportAddWin').width()-35);
	$('#reportContent').height($('#reportAddWin').height()-110);
	
	//—--------------添加反馈
	$('#reportAdd').click( function() {			
		$('#reportAddWin').window('open');
	});
	$('#reportAddCancel').click( function() {
		$('#reportAddWin').window('close');
	});
	$('#reportAddOk').click( function() {
		$.ajax({
			type : "POST",
			url : "/report/",
			data : {
				content:$('#reportContent').val()				
			},
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");				 
				if (json.success){
					$('#reportAddWin').window('close');
					$.messager.show({
						height:40,
						msg:"反馈提交成功",
						timeout:2000,
						showType:'slide',
						style:{
							right:'',
							top:0,
							bottom:''
						}
					});
				}else{
					$.messager.show({
						height:40,
						msg:"反馈提交失败",
						timeout:2000,
						showType:'slide',
						style:{
							right:'',
							top:0,
							bottom:''
						}
					});
				}
			}
		});
	});
	
	//我的反馈窗口
	$('#myReportWin').window({  
	    width:640,  
	    height:480,  
	    title:'我的反馈',
	    modal:true,
	    closed:true,
	    resizable:false,
	    collapsible:false,
	    minimizable:false,
	    maximizable:false,
//	    onOpen:onprojectTaskAddOpen   
	});
	//我的反馈关闭按钮
	$('#myReportClose').linkbutton({  
	    iconCls: 'icon-ok'  
	});
	
	//—--------------我的反馈
	$('#myReport').click( function() {
		//我的反馈表格
		$('#myReportTable').datagrid({
			width: $('#myReportWin').width()-25,
		    height:$('#myReportWin').height()-70,
		    url:'/myReport/',
		    idField:'id',
		    autoRowHeight: true,
		    striped:true,
		    fitColumns: true,
		    rownumbers:false,
		    singleSelect:true,
		    columns:[[
		    	{title:'id',field:'id',hidden:true},
		    	{field:'content',title:'反馈内容',width: $('#myReportWin').width()*0.7},
		    	{field:'creat_time',title:'提交时间',width: $('#myReportWin').width()*0.3}
		    ]]
		});
	
		$('#myReportWin').window('open');
	});
	$('#myReportClose').click( function() {
		$('#myReportWin').window('close');
	});
	
});


