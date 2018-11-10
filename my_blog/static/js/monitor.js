$(function () { 
    $("[data-toggle='tooltip']").tooltip(); 
    Waves.init();
});

function switch_time(tt){
    var tt=$(tt)
    var s = tt.attr("data-original-title");
    tt.attr("data-original-title",tt.attr("temp-storage-1"));
    $('.tooltip-inner').text(tt.attr("temp-storage-1"));        
    tt.attr("temp-storage-1",s);
    s=tt.text();
    tt.text(tt.attr("temp-storage-2"));
    tt.attr("temp-storage-2",s);
    event.stopPropagation(); 
}
function pop_chart(tt){
    var $chart_body = $('#chart-body');
    $chart_body.html(null);
    var tt=$(tt).clone();
    tt.removeAttr("onclick");
    tt.removeAttr('class');
    tt[0].className='p-0 col-xl-3 col-lg-4 col-md-4 col-sm-5 col-6'
    // tt.attr('style','margin-right:auto;');
    tt.find('div.mcard')[0].className='m-0 mcard p-0';
    tt.find('p.text-overflow').addClass('h4');
    tt.find('div.shadow-sm').removeClass('ml-2');
    tt.find('div.shadow-sm').removeClass('shadow-sm');
    var $text_muted = tt.find('a.text-muted');
    tt.find('div.btn-group').append($('<p class="m-0 text-center text-truncate text-overflow h4" style="width:100%">'+$text_muted.attr("temp-storage-1")+' : '+$text_muted.attr("temp-storage-2")+'</p>'));
    tt.find('div.btn-group').append($('<p class="m-0 text-center text-truncate text-overflow h4" style="width:100%">'+$text_muted.attr("data-original-title")+' : '+$text_muted.text()+'</p>'));
    tt.find('div.btn-group').removeClass('btn-group')
    tt.find('a.text-muted').html(null);
    $("#chart").modal();
    $chart_body.append(tt);
    $chart_body.append()
    var $div = $('<div class="p-0 col-xl-3 col-lg-3 col-md-4 col-sm-6 col-12" style="margin-right:auto;"></div>');
    $div.append($('<h3 class="text-center my-3">选择集数</h3>'));
    for(i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        $div.append('<span><a onclick="record(this,'+String(i)+');" class="p-0 btn btn-secondary index_list" style="border:0;margin:6.3px;border-radius:40px;height:3em;line-height:3em;width:3em" href="###">'+String(i)+'</a></span>');
    $div.append($('<span style="padding:0em 5% 0em 5%;"><a class="m-1 p-0 btn btn-secondary index_list" onclick="record(this,-1);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:90%" href="###">全部</a></span>'));
    $div.append($('<h3 class="text-center my-3">选择显示信息</h3>'));
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-2);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">硬币数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-3);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">弹幕数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-4);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">分享数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-5);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">播放数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-6);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">回复数</a></span>');
    $div.append($('<h3 class="text-center my-3">图表调整</h3>'));
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili" onclick="record(this,-10);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_longarrowaltleft zi_2x"></i></a></span>');
    $div.append('<span class="h5">位置:12</span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili" onclick="record(this,-20);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_longarrowaltright zi_2x"></i></a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili" onclick="record(this,-30);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_pluscircle zi_2x"></i></a></span>');
    $div.append('<span class="h5">缩放:12</span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili" onclick="record(this,-40);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_minuscircle zi_2x"></i></a></span>');
    $chart_body.append($div);
    var $img = $('<div class="p-0 col-xl-6 col-lg-6 col-md-12 col-sm-12 col-12" style="margin-right:auto;"></div>');
    $img.append($('<div style="height:100%;width:100%;background-color:#000000"></div>'))
    $chart_body.append($img);
    

    // $.ajax({
    // type:"POST",	
    // url:"/change_password/",
    // data:{
    // 	password:password,
    // 	old_password:old_password,
    // 	csrfmiddlewaretoken:csrf
    // },
    // dataType:"json",
    // success:function(data){
    // 	if (data.state==0)
    // 		set_cookie(data,"修改");
    // 	else if(data.state==2)
    // 		location.reload();
    // 	else
    // 		input_error(data.info);
    // },
    // error:function(jqXHR){
    // 	input_error("发生错误 请尝试刷新");
    // }
    // });
    Waves.attach('.btn', ['waves-float']);

}
function record(tt,sum){
    var $tt = $(tt);
    if(sum>=0){
        $('.index_list').toggleClass('bg-bilibili',false);
        $tt.toggleClass('bg-bilibili',true);
    }else if(sum == -1){
        $('.index_list').toggleClass('bg-bilibili',true);
    }else if(sum<0 && sum>-10){
        $tt.toggleClass('bg-bilibili');
    }else if(sum<=10){
        $tt.toggleClass
    }
}