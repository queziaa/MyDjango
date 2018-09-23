var page = 0;
var $right=$("#right");

$(document).ready(function(){
	setInterval(load_img_funct,500);
});
function load_img_funct(){
	if($(document).scrollTop()>$(document).height()-$(window).height()-20){
		$.ajax({
			type:"GET",
			url:"/get_img/"+page,
			dataType:"json",
			success:function(imgs_json){
				loadState = true;
				page+=1;
				for(var i=0;i<imgs_json.len;i++)
					$right.append($('<div class="imfMod"><img src='+imgs_json.data[i].url+' title='+imgs_json.data[i].id+' ></div>'));
				if(imgs_json.len<5)
					$(window).scroll=null;
				loadState = false;
			}
		});
	}
}