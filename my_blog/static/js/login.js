$(document).ready(function(){ 
	window["register"] = true;
	window["login_reg_click"] = true;
	window["track"] = "";
	$("#search").attr("onclick","loadSearch();return false;")
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
function loadSearch(){
	login_reg_click = true;
	$('#user').html($('#dynamic_login').html());
	$("#login_reg").attr("onclick","loadSearchAjax();return false;");
	$("#name").attr("placeholder","关键字");
	$("#repeat_password").remove();
	$("#password").remove();
	input_error("搜索");
	$("#display").remove();
	delSearch();
}
function loadSearchAjax(){
	if(!login_reg_click)
		return false;
	input_error("加载中. . .",true);
	var keyword = $("#name").val();
	var csrf = $('#comment [name="csrfmiddlewaretoken"]').val();
	$.ajax({
		type:"POST",	
		url:"/port_search/",
		data:{
			keyword:keyword,
			csrfmiddlewaretoken:csrf
		},
		dataType:"json",
		success:function(data){
			if(data.state==0){
				window["track"] = data.track;
				window["surplus"] = data.end;
				window["$right"] = $("#right");
				if(typeof(imgs_interval) != "undefined" )
					clearInterval(imgs_interval);
				$("#right").html(null);
				$right.append($('<dir class="loadPrompt" id="imgPrompt">下拉或点击加载更多</dir>'));				
				window["imgarticles"] = $("#imgPrompt");
				loadSearchDom(data.data);
				imgarticlesPosition();
				if(!surplus){
					window["imgs_interval"] = setInterval(load_Search_funct,500);
					window.onbeforeunload = delSearch;
				}
				else{
					imgarticles.html("已经没有更多结果了");
				}
				input_error("搜索");
			}
			else if(data.state==1)
				input_error(data.info);
			else if(data.state==2)
				input_error("发生错误 请尝试刷新");
			else
				input_error("发生错误 请尝试刷新");
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			input_error("发生错误 请尝试刷新");
		}
	});
	window["searchState"] = false;
	return false;
};
function load_Search_funct(){
	if (searchState||surplus)
		return false;
	searchState = true;
	if($(document).scrollTop()>$(document).height()-$(window).height()-20){
		imgarticles.html("正在加载中...");
		$.ajax({
			type:"GET",
			url:"/surplus_search/?track="+track+"&end=false",
			dataType:"json",
			success:function(Search_json){
				if(Search_json.state==0){
					if(Search_json.end){
						surplus = true;
						clearInterval(imgs_interval);
						imgarticles.html("已经没有更多结果了");
					}else{
						imgarticles.html("下拉或点击加载更多");
					}
					loadSearchDom(Search_json.data);
					imgarticlesPosition();
				}
				else{
					imgarticles.html("发生错误 请尝试刷新");
				}
			}
		});
	}
	searchState = false;
}
function loadSearchDom(domJson){
	for(i in domJson)
		establishArticles(domJson[i]);
}
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
			if(data.state==0)
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
	var login_reg = $("#login_reg");
	if(noClick==undefined){
		login_reg_click=true;
		login_reg.css({"background":"#bfc4cc","color":"#31332e"});
	}
	else{
		login_reg_click=false;
		login_reg.css({"background":"#204042","color":"#bfc4cc"});
	}
	login_reg.val(info);
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
function establishArticles(articlesJson){
	var $section_main = $('<dir class="section_main"></dir>').append($('<div class="title"><a href="/detailed/'+articlesJson.id+'/">'+articlesJson.title+'</a></div>'));
	if(articlesJson.content.img)
		var $img = $('<img src="'+articlesJson.content.img+'" onclick="enlarge(this)">');
	else if(articlesJson.content.code)
		var $img = $('<pre><code>'+articlesJson.content.code+'</code></pre>');
	else
		var $img = null;
	$section_main.append($('<div class="subject"><p>'+articlesJson.content.text+'......</p></div>').append($img));
	articlesJson.label = articlesJson.label.split('#')
	Label_test = "";
	for(Label_single in articlesJson.label)
		Label_test = Label_test+'<a class="label" onclick="searchTags(this);return false;">'+articlesJson.label[Label_single]+'</a>'
	$section_main.append($('<div class="ther"><span>发布者:'+articlesJson.user+'</span><span>发布于:'+articlesJson.date_time+'</span><span>提交于:'+
		articlesJson.examine_time+'</span><span>评论数:'+articlesJson.comments_quantity+'</span><span>'+Label_test+'</span>'+'</div>'));
	imgarticles.before($section_main);
}
function delSearch(){
	$.ajax({
		url:"/surplus_search/?track="+track+"&end=true",
		type : 'GET',
		dataType : 'json',
	});
}
function searchTags(aLabel){
	loadSearch();
	$("#name").val(aLabel.text);
	loadSearchAjax();

}
function imgarticlesPosition(){
	imgarticles.css("position","static");
	if(imgarticles.outerHeight() + imgarticles.offset().top+2 > $('#right').outerHeight())
		imgarticles.css("position","static");
	else
		imgarticles.css("position","");
}