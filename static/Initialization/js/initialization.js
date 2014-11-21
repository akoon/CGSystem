$(document).ready(function(){
	
	//pillars id
	$('#validateform input[name="pillars_id"]').blur(function(){
		$(this).next('span').remove();		

		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">Pillars ID 不可为空！</span>');
		}

	});

	//pillars 密码
	$('#validateform input[name="pillars_pwd"]').blur(function(){
		$(this).next('span').remove();		

		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">密码不可为空！</span>');
		}

	});

	//pillars 序列号
	$('#validateform input[name="pillars_sn"]').blur(function(){
		$(this).next('span').remove();		

		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">序列号不可为空！</span>');
		}

	});

	//表单提交前验证
	$('#validateform').submit(function(){
		var validata = true;
		var $table = $(this).children('.form-table');
		$table.prevAll('span').remove();

  		$table.find(':input').each(function(i){
			if( $(this).val() == ""){
				validata = false;
				$table.before(function(){
					switch(i){
						case 0: 
							return '<span style="color: red;">Pillars ID 为空！<br/></span>';
						case 1: 
							return '<span style="color: red;">密码为空！<br/></span>';
						case 2: 
							return '<span style="color: red;">序列号为空！<br/></span>';
						default:
							return '';	
					}
				});
			}
		});

		return validata;
	});

	//邮件服务器
	$('#mailform input[name="EMAIL_HOST"]').blur(function(){
		$(this).next('span').remove();		
		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">服务器不可为空！</span>');
		}

	});
	
	//邮件服务器端口
	$('#mailform input[name="EMAIL_PORT"]').blur(function(){
		$(this).next('span').remove();		
		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">端口号不可为空！</span>');
		}

	});

	//发件邮箱
	$('#mailform input[name="EMAIL_HOST_USER"]').blur(function(){
		$(this).next('span').remove();		
		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">用户名不可为空！</span>');
		}

	});

	//发件邮箱密码
	$('#mailform input[name="EMAIL_HOST_PASSWORD"]').blur(function(){
		$(this).next('span').remove();		
		if( $(this).val() == ""){
			$(this).after('<span style="color: red;">密码不可为空！</span>');
		}

	});

	//邮件配置表单提交验证
	$('#mailform').submit(function(){
		var validata = true;
		var $table = $(this).children('.form-table');
		$table.prevAll('span').remove();
		
  		$table.find(':input').each(function(i){
			if( $(this).val() == ""){
				validata = false;
				$table.before(function(){
					switch(i){
						case 0: 
							return '<span style="color: red;">服务器为空！<br/></span>';
						case 1: 
							return '<span style="color: red;">端口号为空！<br/></span>';
						case 2: 
							return '<span style="color: red;">用户名为空！<br/></span>';
						case 3: 
							return '<span style="color: red;">密码为空！<br/></span>';
						case 4: 
							return '<span style="color: red;">TLS为空！<br/></span>';
						default:
							return '';	
					}
				});
			}
		});
		if(validata){
			$('#msg_mail').text('正在测试邮件发送功能...');
		}
		return validata;
	});





})
