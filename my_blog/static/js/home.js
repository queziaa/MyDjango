$(document).ready(function () {
	window["page"] = 0;
	window["imgarticles"] = $("#imgPrompt");
	window["ajaxState"]=false;
	imgarticles.attr("onclick","load_articles_funct();");
	$(document).ready(function(){
		window["articles_interval"] = setInterval(load_articles_funct,500);
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
			url:"/get_home_articles/"+page,
			dataType:"json",
			success:function(articles_json){
				page+=1;
				for(var i=0;i<articles_json.length;i++)
					establishArticles(articles_json[i]);
				if(articles_json.length<5){
					clearInterval(articles_interval);
					imgarticles.html("已经没有更多文章了");
				}else{
					imgarticles.html("下拉或点击加载更多");
					imgarticles.css("position","static");
				}
				$('pre code').each(function(i, block) {
			        hljs.highlightBlock(block);
    			});
			}
		});
	}
	ajaxState = false;
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
	$section_main.append($('<div class="ther"><span>发布者:'+articlesJson.user+'</span><span>发布于'+articlesJson.date_time+'</span><span>提交于'+articlesJson.examine_time+'</span><span>'+articlesJson.comments_quantity+'条评论</span></div>'));
	imgarticles.before($section_main);
}