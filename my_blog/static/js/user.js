function open_change_password() {
	var dynamic_login = document.getElementById("dynamic_login");
	var name = document.getElementById("name");
	dynamic_login.style.display="block";
	name.id="old_password";
	name.type="password";
	name.placeholder="老密码";
	document.getElementById("password").placeholder="新密码";
	document.getElementById("repeat_password").placeholder="再次输入新密码";
	document.getElementById("login_reg").value="修改密码";
	document.getElementById("user_title").appendChild(dynamic_login);
	document.getElementById("login_reg").onclick = function(){
		input_error("加载中. . .");
		var old_password = document.getElementById("old_password").value;
		var password = document.getElementById("password").value;
		var repeat_password = document.getElementById("repeat_password").value;

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
		var comment = document.getElementById("comment");
		for(var i=0; i<comment.length;i++){
			if(comment[i].name=="csrfmiddlewaretoken"){
				var csrf = comment[i].value;
				break;
			}
		}
		var request = new XMLHttpRequest();
		request.open("POST", "/cehange_password/");
		var data = "csrfmiddlewaretoken="+csrf+"&old_password="+old_password+"&password="+password+"&repeat_password="+repeat_password;
		request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		request.send(data);
		request.onreadystatechange = function() {
			if (request.readyState===4) {
				if (request.status===200) { 
					var jsondata = JSON.parse(request.responseText);
					if (jsondata["state"]=="0"){
						set_cookie(jsondata,"修改");
					}else if(jsondata["state"]=="2"){
						alert(request.status+":发生错误 请重新登录");
						location.reload();
					}else{
						input_error(jsondata["info"]);
					}
				} else {
					alert(request.status+":发生错误 请尝试刷新");
				}
			} 
		}
		return false;
	}
}