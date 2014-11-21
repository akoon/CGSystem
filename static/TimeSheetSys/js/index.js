//tab标识当前页
$('#baseIndexLnk').addClass('active');

$(document).ready(function() {! function() {
		//获取当前系统管理员
		$.getJSON('/TimeSheetSys/adminlist/', function(data) {
			$.each(data.rows, function(i, row) {
				var $tbody = $('#superusers').children('tbody');
				var $tr = $('<tr></tr>');
				$tr.append($('<td></td>').text(row.user));
				$tr.append($('<td></td>').text(row.name));
				$tr.append($('<td></td>').text(row.sex == 0 ? 'Female' : 'Male'));
				$tr.append($('<td></td>').text(row.phone));
				$tr.append($('<td></td>').text(row.email));
				$tr.append($('<td></td>').text(row.department));
				$tr.append($('<td></td>').text(row.position));
				$tbody.append($tr);
			});
		});
	}();
});
