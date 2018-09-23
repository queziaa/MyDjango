var register = true;
var login_reg_click = true;
$(document).ready(function(){ 
	$.ajax({
		type:"GET",
		url:"/obtain_name",
		dataType:"json",
		success:function(data){
			if(data.login){
				var user = $("#user");
				$("#registered").remove();
				$("#login").remove();
				$("#change").html(data.name);
				$("#change").attr("href","/user");
			}else{			
				$("#login").attr("onclick","loadLogin();return false;");
				$("#registered").attr("onclick","loadRegister();return false;");
			}
			$("#user").css("visibility","visible");
		}
	});

});
function loadRegister(){
	register = true;
	$('#user').html($('#dynamic_login').html());
	$("#display").remove();
	$("#login_reg").attr("onclick","loginRegisteredAjax();return false;")
}
function loginRegisteredAjax(){
	if(!login_reg_click)
		return false;
	input_error("加载中. . .",true);
	var name = $("#name").val();
	var password = $("#password").val();
	if(register){
		var url = "/registered/";
		var repeat_password = $("#repeat_password").val();
	}else{
		var url = "/login/";
		var repeat_password = password;
	}
	var error_text = namePassCheck(name,password,repeat_password);
	if(error_text)
		return input_error(error_text);
	var csrf = $('#comment [name="csrfmiddlewaretoken"]').val();
	$.ajax({
		type:"POST",	
		url:url,
		data:{
			name:name,
			password:password,
			csrfmiddlewaretoken:csrf
		},
		dataType:"json",
		success:function(data){
			if(data.state=="0")
				set_cookie(data,"登陆");
			else
				input_error(data["info"]);
		},
		error:function(jqXHR){
			input_error("发生错误 请尝试刷新");
		}
	});
	return false;
};
function loadLogin(){
	loadRegister();
	register = false;
	$("#repeat_password").remove();
	$("#login_reg").val("登陆");
}
function input_error(info,noClick){
	if(noClick==undefined)
		login_reg_click=true;
	else
		login_reg_click=false;
	var login_reg = $("#login_reg");
	login_reg.val(info);
	login_reg.css({"background":"#204042","color":"#bfc4cc"});
	return false;
}
function set_cookie(jsondata,info){
	$.cookie("name",jsondata.cookie_name,{expires:14,path:'/'});
	$.cookie("password",jsondata.cookie_password,{expires:14,path:'/'});
	input_error(info+"成功 三秒后刷新.",true);
	setTimeout('input_error("'+info+'成功 三秒后刷新..",true)',1000);
	setTimeout('location.reload()',1500);
}
function namePassCheck(name,password,repeat_password){
	if(name.length<5)
		return "用户名至少五位";
	if(name.length>14)
		return "用户名最多十四位";
	if(password.length<5)
		return "密码至少五位";
	if (password.length>14)
		return "密码最多十四位";
	if(password!=repeat_password)
		return "两次密码不一致";
}