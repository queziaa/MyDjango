$(document).ready(function () {
	window["page"] = -1;
	window["imgPromptUploadimg"] = $("#imgPrompt");
	window["ajaxState"]=false;
	imgPromptUploadimg.attr("onclick","load_img_funct()");
	$(document).ready(function(){
		window["imgs_interval"] = setInterval(load_img_funct,500);
	}); 
});
function load_img_funct(){
	if (ajaxState)
	return false;
	ajaxState = true;
	if($(document).scrollTop()>$(document).height()-$(window).height()-20){
		imgPromptUploadimg.html("正在加载中...");
		$.ajax({
			type:"GET",
			url:"/get_img/"+(page+=1),
			dataType:"json",
			success:function(imgs_json){
				for(var i=0;i<imgs_json.len;i++)
					imgPromptUploadimg.before('<div class="imfMod"><img src='+imgs_json.data[i].url+' title='+imgs_json.data[i].id+' onclick="enlarge(this)"></div>');
				if(imgs_json.len<5){
					clearInterval(imgs_interval);
				imgPromptUploadimg.html("已经没有更多图片了");
					if(imgPromptUploadimg.outerHeight() + imgPromptUploadimg.offset().top+2 > $('#right').outerHeight())
						imgPromptUploadimg.css("position","static");
				}else{
					imgPromptUploadimg.html("下拉或点击加载更多");
				}
			}
		});
	}
	ajaxState = false;
}
