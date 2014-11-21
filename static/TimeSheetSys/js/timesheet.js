
$('#tsTSLnk').addClass('active');

//  提交任务
function eventSubmit(uid, date) 
{
//	alert(uid + '    ' + date);

//	Ext.MessageBox.confirm('提交任务', '是否要提交当天任务(提交之后可以继续修改直到审核通过)?', callback);
	var r=confirm("是否要提交当天任务(提交之后不允许修改)?");
	if (r==true)
    {
    	//  提交任务检测
    	
    	
		$.ajax({
			type : "POST",
			url : "/confirm_actual_tasks",
			data : {
				uid : uid,
				date  : date
			},
			datatype : "json",
			success : function(data) {
				var json = eval('(' + data + ')');
				if(json.result == true)
				{
					//页面跳转
					window.location.href='/TimeSheetSys/timesheet/';
				}
				else
				{
					if(json.msg != '' || json.msg != null)
					{
						alert(json.msg);
					}
					else
					{
						alert("提交失败");
					}
						
				}
			}
		});
	}
	else
	{
		return null;
	}

}

// 审核通过
function eventAccept(uid, date) 
{
	var r=confirm("是否确定审核通过?");
	if (r==true)
    {
    	$.ajax({
			type : "GET",
			url : "/timesheet_judge",
			data : {
				uid : uid,
				date  : date,
				option  : 'accept'
			},
			datatype : "json",
			success : function(data) {
				//id="day-col-confirm-'+ Ext.Date.format(item[M.StartDate.name], 'Ymd') +'"
				//alert("审核通过");
				//$('#confirm-' + date).css('background-color', 'green').empty()
				
				//$('#confirm-msg-' + date).html('审核通过');
				//$('#dropdown-menu-div-' + date).remove();
				
				//页面跳转
				window.location.href='/TimeSheetSys/timesheet_viewmode/?date=today&uid=' + uid;
			}
		});
    }
    else
    {
    	return null;
    }
    
}

// 审核未通过
function eventReject(uid, date) 
{
	var r=confirm("是否设定为审核未通过?");
	if (r==true)
    {
    	$.ajax({
			type : "GET",
			url : "/timesheet_judge",
			data : {
				uid : uid,
				date  : date,
				option  : 'reject'
			},
			datatype : "json",
			success : function(data) {
				//id="day-col-confirm-'+ Ext.Date.format(item[M.StartDate.name], 'Ymd') +'"
				//alert("审核未通过");
				//$('#confirm-' + date).css('background-color', 'red').empty().html('<div id="day-col-confirm-'+ date +'">审核未通过</div>');
				
				//$('#confirm-msg-' + date).html('审核未通过');
				//$('#confirm-icon-' + date).removeClass().addClass("timeSheetUi_8");
				//$('#dropdown-menu-div-' + date).remove();
				
				//页面跳转
				window.location.href='/TimeSheetSys/timesheet_viewmode/?date=today&uid=' + uid;
			}
		});
    }
    else
    {
    	return null;
    }
    
}

//审核修改状态  确认修改
function applyChange(uid, date, sid) 
{
//	alert(uid + '    ' + date);

//	Ext.MessageBox.confirm('提交任务', '是否要提交当天任务(提交之后可以继续修改直到审核通过)?', callback);
	var r=confirm("是否确认修改?");
	if (r==true)
    {
		$.ajax({
			type : "POST",
			url : "/applychange_actual_tasks",
			data : {
				uid : uid,
				date  : date,
				sid   : sid
			},
			datatype : "json",
			success : function(data) {
				//页面跳转
				window.location.href='/TimeSheetSys/timesheet_viewmode/?date=today&uid=' + uid;
			}
		});
	}
	else
	{
		return null;
	}

}

function timesheetWindowClose(uid, date, sid)
{	
	var mode = Ext.get("mode").dom.innerHTML
	console.log("mode     " + mode);
	if(mode == 'edit')
	{
		location.href='/ProjectManSys';
	}
	else if(mode == 'judge')
	{
		console.log("judge mode return ");
		location.href='/TimeSheetSys';
	}
	else if(mode == 'viewedit')
	{
		if(sid == 'none' || sid == '' || sid == null)
		{
			location.href='/TimeSheetSys';
		}
		else
		{
			$.ajax({
				type : "POST",
				url : "/restore_daily_status",
				data : {
					uid : uid,
					date  : date,
					sid   : sid
				},
				datatype : "json",
				success : function(data) {
					//页面跳转
					location.href='/TimeSheetSys';
				}
			});
		}
	}

	
}

function timesheetDropdownMenu(id)
{	
	$(".dropdown:not(#"+id+")").toggle(false);
	$("#"+id).toggle();
	
}

