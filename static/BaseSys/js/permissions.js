$(document).ready(function() {
	// **************************************页面初始化**************************************
	
	var _h = $(window).height();
    var _w = $(window).width();
    var  w = $("#content").width();
    
    $('#permissions').css({
        height: _h - 150,
    });
        
    $('.permissionsShow, .moveButton_Warp').css({
        height: _h - 260,
    });
        
    $('.permissionsContent， .entrance-Warp， .entrance-Inner').css({
        width: w,
    });
	
	$('.permissionsList_body_A ul, .permissionsList_body_B ul').css({
        height: _h - 310,
    });
	
});