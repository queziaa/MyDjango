var register = true;
var login_reg_click = true;
window.onload=function(){
	var request = new XMLHttpRequest();
	request.open("GET", "/obtain_name");
	request.send();
	request.onreadystatechange = function() {
		if (request.readyState===4) {
			if (request.status===200) { 
				var data = JSON.parse(request.responseText);
				if(data["login"]=="True"){
					var user = document.getElementById("user");
					user.removeChild(document.getElementById("registered"));
					user.removeChild(document.getElementById("login"));
					change=document.getElementById("change").href="/user";
					change=document.getElementById("change").text=data["name"];
				}
				document.getElementById("user").style.visibility="visible";
			} else {
				request.send();
			}
		} 
	}
}
function loadRegister(){
	register = true;
	var dynamic_login=document.getElementById("dynamic_login");
	document.getElementById("user").innerHTML=dynamic_login.innerHTML;
	dynamic_login.parentNode.removeChild(dynamic_login);

	document.getElementById("login_reg").onclick = function() {
		if(!login_reg_click)
			return false;
		input_error("加载中. . .",true);
		var name = document.getElementById("name").value;
		var password = document.getElementById("password").value;
		if(name.length<5)
			return input_error("用户名至少五位");
		if(name.length>14)
			return input_error("用户名最多十四位");
		if(password.length<5)
			return input_error("密码至少五位");
		if (password.length>14)
			return input_error("密码最多十四位");
		var comment = document.getElementById("comment");
		for(var i=0; i<comment.length;i++){
			if(comment[i].name=="csrfmiddlewaretoken"){
				var csrf = comment[i].value;
				break;
			}
		}
		if(register){
			var url = "/registered/";
			var repeat_password = document.getElementById("repeat_password").value;
			if(repeat_password !== password)
				return input_error("两次密码不一致");
		}else{
			var url = "/login/";
		}
		var request = new XMLHttpRequest();
		request.open("POST", url);
		var data = "name=" + name + "&password=" + password	+ "&csrfmiddlewaretoken=" + csrf;
		if(register)
			data += "&repeat_password=" + repeat_password;
		request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		request.send(data);
		request.onreadystatechange = function() {
			if (request.readyState===4) {
				if (request.status===200) { 
					var jsondata = JSON.parse(request.responseText);
					if (jsondata["state"]=="0"){
						set_cookie(jsondata,"登陆");
					}else{
						input_error(jsondata["info"]);
					}
				} else {
					request.send();
				}
			} 
		}
		return false;
	}
}
function loadLogin(){
	loadRegister();
	register = false;
	var repeatPass=document.getElementsByName("repeat_password")[0];
	repeatPass.parentNode.removeChild(repeatPass);
	document.getElementById("login_reg").value="登陆";
}
function input_error(info,noClick){
	if(noClick==undefined)
		login_reg_click=true;
	else
		login_reg_click=false;
	var login_reg = document.getElementById("login_reg");
	login_reg.value=info;
	login_reg.style.background="#204042";
	login_reg.style.color="#bfc4cc";
	return false;
}
function set_cookie(jsondata,info){
	var exp = new Date();
	exp.setTime(exp.getTime() + 1209600000);
	document.cookie = "name="+ jsondata["cookie_name"] + ";expires=" + exp.toGMTString() + ";path=/";
	document.cookie = "password="+ jsondata["cookie_password"] + ";expires=" + exp.toGMTString() + ";path=/";
	input_error(info+"成功 三秒后刷新.",true);
	setTimeout('input_error("'+info+'成功 三秒后刷新..",true)',1000);
	setTimeout('location.reload()',1500);
}