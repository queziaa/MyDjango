function Delete_node(node){
	node.parentNode.removeChild(node);
}
function enlarge(fixed_img){
	var backgroundDiv=document.createElement("div");
	backgroundDiv.style.cssText="left:0;top:0;position:fixed;background:#000;opacity:0.5;width:100%;height:100%";
	backgroundDiv.id="backgroundDiv";
	backgroundDiv.onclick=function(){Delete_node(this);Delete_node(document.getElementById("new_img"));};
	document.body.appendChild(backgroundDiv);
	var new_img=document.createElement("img");
	new_img.src=fixed_img.src;
	document.body.appendChild(new_img);
	new_img.id="new_img";
	new_img.style.cssText="position:fixed;margin:0;top:0;left:0;border-radius:0;border:0;max-width:none;";
	new_img.onclick=function(){Delete_node(this);Delete_node(document.getElementById("backgroundDiv"));};
	if(document.body.clientHeight/fixed_img.height*fixed_img.width<document.body.clientWidth){
		new_img.width*=document.body.clientHeight/fixed_img.height;
		new_img.height=document.body.clientHeight;
		new_img.style.left=(document.body.clientWidth-new_img.width)/2+"px";
	}else{
		new_img.height*=document.body.clientWidth/fixed_img.width;
		new_img.width=document.body.clientWidth;
		new_img.style.top=(document.body.clientHeight-new_img.height)/2+"px";
	}
}