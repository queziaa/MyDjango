$(document).ready(function(){
	$("#change_password").attr("onclick","open_change_password();return false;");
});
function open_change_password(){
	$("#user_title").append($("#dynamic_login").html());
	var name = $("#name");
	name.attr("id","old_password");
	name.attr("type","password");
	name.attr("placeholder","老密码");
	$("#password").attr("placeholder","新密码");
	$("#repeat_password").attr("placeholder","再次输入新密码");
	$("#login_reg").val("修改密码");
	$("#login_reg").attr("onclick","changeAjax();return false;")
}
function changeAjax(){
	input_error("加载中. . .");
	var old_password = $("#old_password").val();
	var password = $("#password").val();
	var repeat_password = $("#repeat_password").val();
	if(old_password.length<5)
		return input_error("老密码至少五位");
	if(old_password.length>14)
		return input_error("老密码最多十四位");
	if(password.length<5)
		return input_error("新密码至少五位");
	if (password.length>14)
		return input_error("新密码最多十四位");
	if(repeat_password !== password)
		return input_error("两次密码不一致");
	var csrf = $('#comment [name="csrfmiddlewaretoken"]').val();
	$.ajax({
		type:"POST",	
		url:"/change_password/",
		data:{
			password:password,
			old_password:old_password,
			csrfmiddlewaretoken:csrf
		},
		dataType:"json",
		success:function(data){
			if (data.state==0)
				set_cookie(data,"修改");
			else if(data.state==2)
				location.reload();
			else
				input_error(data.info);
		},
		error:function(jqXHR){
			input_error("发生错误 请尝试刷新");
		}
	});
	return false;
}