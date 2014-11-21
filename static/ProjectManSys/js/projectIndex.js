//tab标识当前页
$('#projectIndexLnk').addClass('active');

var _h = $(window).height();
var _w = $(window).width();

sidebarWidth = 182;
$(".project-bar").width(sidebarWidth);
$(".project-content").width(_w - sidebarWidth);



// $(document).ready(function() {
	// //项目统计信息
	// $.ajax({
		// type : "POST",
		// url : "/ProjectManSys/project_summary/",
		// data : {
			// proj_id : $('#projectId').html()
// 
		// },
		// datatype : "json",
		// success : function(data) {
			// var json = eval("(" + data + ")");
// 
			// $("#proj-taskcount").html(json.taskCount);
			// $("#proj-wipcount").html(json.wipCount);
			// $("#proj-publish-count").html(json.publishCount);
			// $("#proj-submit-count").html(json.submitReCount);
			// $("#proj-passed-count").html(json.passedCount);
			// $("#proj-qc-count").html(json.qcCount);
// 
		// }
	// });
// 
	// //组信息表格
	// $('#projectUserTable').datagrid({
		// width : 200,
		// height : $('#project-userinfo').height(),
		// url : '/ProjectManSys/projectPeopleDetail/',
		// //method:'get',
		// idField : 'id',
		// toolbar : '#projectPeopleTb',
		// autoRowHeight : true,
		// striped : true,
		// scrollbarSize : 0,
		// showHeader : false,
		// showFooter : false,
		// rownumbers : false,
		// singleSelect : true,
		// columns : [[{
			// title : 'id',
			// field : 'id',
			// hidden : true
		// }, {
			// field : 'name',
			// title : '项目成员',
			// sortable : true,
			// width : 178
		// }]],
		// queryParams : {
			// projectId : $('#projectId').html()
		// },
		// onClickRow : onClickRow,
	// });
// 
	// // 图片上传窗口
	// $('#projectImgWin').window({
		// width : 280,
		// height : 170,
		// title : '图片上传',
		// modal : true,
		// closed : true,
		// resizable : false,
		// collapsible : false,
		// minimizable : false,
		// maximizable : false,
		// //onClose : onprojectImgClose
	// });
	// // 图片上传确定按钮
	// $('#projectImgOk').linkbutton({
		// iconCls : 'icon-ok'
	// });
	// // 图片上传取消按钮
	// $('#projectImgCancel').linkbutton({
		// iconCls : 'icon-cancel'
	// });
	// $('#projecImg').click(function() {
		// $('#projectImgWin').window('open');
	// });
	// $('#projectImgCancel').click(function() {
		// $('#projectImgWin').window('close');
	// });
// 
	// $("#projectImgOk").click(function() {
		// var id = $('#projectId').html();
		// var file = $("#projectImage").val();
		// if (file == "") {
			// alert("请选择上传的图片");
			// return;
		// } else {
			// $.ajaxFileUpload({
				// url : '/ProjectManSys/projectImg',
				// secureuri : false,
				// fileElementId : "projectImage", // file的id
				// dataType : "json",
				// data : {
					// id : id
				// }, // 返回数据类型为文本
				// success : function(data, status) {
					// if (data.sucess) {
						// $('#projectImgWin').window('close');
						// $.messager.show({
							// height : 40,
							// msg : '图片上传成功',
							// timeout : 2000,
							// showType : 'slide',
							// style : {
								// right : '',
								// top : 0,
								// bottom : ''
							// }
						// });
// 
					// }
				// }
			// });
		// }
	// });
// });
// 
// //单击表格行事件
// function onClickRow(rowIndex, field, value) {
	// console.log(rowIndex);
	// console.log(field.id);
	// console.log(field.name);
// 
	// $.ajax({
		// type : "POST",
		// url : "/ProjectManSys/project_user_summary/",
		// data : {
			// proj_id : $('#projectId').html(),
			// user_id : field.id
		// },
		// datatype : "json",
		// success : function(data) {
			// var json = eval("(" + data + ")");
// 
			// $("#user-taskcount").html(json.taskCount);
			// $("#user-wipcount").html(json.wipCount);
			// $("#user-publish-count").html(json.publishCount);
			// $("#user-submit-count").html(json.submitReCount);
			// $("#user-passed-count").html(json.passedCount);
			// $("#user-qc-count").html(json.qcCount);
// 
		// }
	// });
// 
// }

$(document).ready(function(){

	$('#projectImgWin').window({
				 width : 280,
				 height : 170,
				 title : 'Image Upload',
				 modal : true,
				 closed : true,
				 resizable : false,
				 collapsible : false,
				 minimizable : false,
				 maximizable : false
	});
	// 图片上传确定按钮
	$('#projectImgOk').linkbutton({
		iconCls : 'icon-ok'
	});
	// 图片上传取消按钮
	$('#projectImgCancel').linkbutton({
		 iconCls : 'icon-cancel'
	});
	$('#projectImg').click(function() {
		 $('#projectImgWin').window('open');
	});
	$('#projectImgCancel').click(function() {
		 $('#projectImgWin').window('close');
	}); 
	$("#projectImgOk").click(function() {
		 var id = $('#projectId').html();
		 var file = $("#newprojectImg").val();
		 if (file == "") {
			 alert("Please images you want to upload");
			 return;
		 } else {
			 $.ajaxFileUpload({
				url : '/ProjectManSys/projectImg',
				 secureuri : false,
				 fileElementId : "newprojectImg", // file的id
				 dataType : "json",
				 data : {
					 id : id
				 }, // 返回数据类型为文本
				 success : function(data, status) {
					 if (data.sucess) {
						 $('#projectImgWin').window('close');
						 $('#projectImg').attr("src",data.path);
						 $.messager.show({
							 height : 40,
							 msg : 'upload success',
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
	 
	 
		 
})


