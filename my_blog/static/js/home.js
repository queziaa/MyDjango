$(document).ready(function () {
	window["page"] = -1;
	window["imgarticles"] = $("#imgPrompt");
	window["ajaxState"]=false;
	imgarticles.attr("onclick","load_articles_funct();");
	$(document).ready(function(){
		window["imgs_interval"] = setInterval(load_articles_funct,500);
	}); 
});
function load_articles_funct(){
	if (ajaxState)
		return false;
	ajaxState = true;
	if($(document).scrollTop()>$(document).height()-$(window).height()-20){
		imgarticles.html("正在加载中...");
		$.ajax({
			type:"GET",
			url:"/get_home_articles/"+(page+=1),
			dataType:"json",
			success:function(articles_json){
				for(var i=0;i<articles_json.length;i++)
					establishArticles(articles_json[i]);
				if(articles_json.length<5){
					clearInterval(imgs_interval);
					imgarticles.html("已经没有更多文章了");
					imgarticlesPosition();
				}else{
					imgarticles.html("下拉或点击加载更多");
				}
				$('pre code').each(function(i, block) {
					hljs.highlightBlock(block);
				});
			}
		});
	}
	ajaxState = false;
}
