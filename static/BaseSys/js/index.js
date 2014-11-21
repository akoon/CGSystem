//tab标识当前页
$('#baseIndexLnk').addClass('active');
	

$(document).ready(function(){
	!function(){
		//获取当前系统管理员
		$.getJSON('/BaseSys/peopleDetail/', function(data){
			$.each(data.rows, function(i, row){
				var $tbody = $('#superusers').children('tbody');
				if(row.is_superuser == true){
					var $tr = $('<tr></tr>');
					$tr.append($('<td></td>').text(row.user));
					$tr.append($('<td></td>').text(row.name));
					$tr.append($('<td></td>').text(row.sex == 0 ? 'Female' : 'Male'));
					$tr.append($('<td></td>').text(row.phone));
					$tr.append($('<td></td>').text(row.email));
					$tr.append($('<td></td>').text(row.department));
					$tr.append($('<td></td>').text(row.position));
					$tbody.append($tr);
				}				
			});
		});
		//获取当前部门数
		$.getJSON('/BaseSys/departmentDetail/', function(data){
			var count = data.length;		
			$.each(data, function(i, item){
				count += item.children.length;
			});
			$('#departmentcount').text(count);
		});

		//获取当前职位数
		$.getJSON('/BaseSys/positionDetail', function(data){
			var count = data.total;
			$('#positioncount').text(count);
		});

		//数据库信息及其他信息
		$.getJSON('/BaseSys/systemenvironmentdetail/', function(data){
			var database = data.databases;
			$('#databasename').text(database.databasesname);
			$('#databaseuser').text(database.databasesuser);
			$('#databasehost').text(database.databaseshost);
			$('#databaseport').text(database.databasesport);
			var mountdir = data.mountdir;
			$('#mountdir').text(mountdir);
		});

	}()















})
