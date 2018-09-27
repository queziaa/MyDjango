$(document).ready(function () {
	window["page"] = -1;
	window["imgPrompt"] = $("#imgPrompt");
	window["ajaxState"]=false;
	imgPrompt.attr("onclick","load_img_funct()");
	$(document).ready(function(){
		window["imgs_interval"] = setInterval(load_img_funct,500);
	}); 
});
function load_img_funct(){
	if (ajaxState)
	return false;
	ajaxState = true;
	if($(document).scrollTop()>$(document).height()-$(window).height()-20){
		imgPrompt.html("正在加载中...");
		$.ajax({
			type:"GET",
			url:"/get_img/"+(page+=1),
			dataType:"json",
			success:function(imgs_json){
				for(var i=0;i<imgs_json.len;i++)
					imgPrompt.before('<div class="imfMod"><img src='+imgs_json.data[i].url+' title='+imgs_json.data[i].id+' onclick="enlarge(this)"></div>');
				if(imgs_json.len<5){
					clearInterval(imgs_interval);
				imgPrompt.html("已经没有更多图片了");
					if(imgPrompt.outerHeight() + imgPrompt.offset().top+2 > $('#right').outerHeight())
						imgPrompt.css("position","static");
					else
						imgPrompt.css("position","");
				}else{
					imgPrompt.html("下拉或点击加载更多");
				}
			}
		});
	}
	ajaxState = false;
}
