$(document).ready(function() {
	$('#projectList').bind('click', function() {
		$.ajax({
			type : "GET",
			url : "/ProjectManSys/projectRead/",
			datatype : "json",
			success : function(data) {
				var json = eval("(" + data + ")");//json转换json对象
				$("#plist li").remove();
				var ul = document.getElementById("plist");
				var fragment = document.createDocumentFragment();
				for ( i = 0; i < json.length; i++) {
					var li = document.createElement("li");
					html = "<a href='/ProjectManSys/" + json[i].id+"/'>" + json[i].name + "</a>";
					li.innerHTML = html;
					fragment.appendChild(li);
				}
				ul.appendChild(fragment);
			}
		});

	});
})