$(function () { 
    $("[data-toggle='tooltip']").tooltip(); 
    Waves.init();
    window["ajax_chart"]={};
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
    var col_1 = 'p-0 col-xl-2 col-lg-12 col-md-12 col-sm-12 col-12';
    var col_2 = 'p-0 col-xl-2 col-lg-3 col-md-12 col-sm-12 col-12';
    var col_3 = 'p-0 col-xl-8 col-lg-9 col-md-12 col-sm-12 col-12';
    var $chart_body = $('#chart-body');
    $chart_body.html(null);
    var tt=$(tt).clone();
    var $div = $('<div class="'+col_2+'"></div>');
    $div.append($('<h3 class="text-center my-3">选择集数</h3>'));
    var index_list = post_index(tt.attr('temp-id'));
    if(typeof(index_list)!='object'){
        $div.append($('<span style="padding:0em 5% 0em 5%;"><a class="m-1 p-0 btn btn-secondary index_list index_list-all" style="border:0;border-radius:7px;height:3em;line-height:3em;width:90%" href="###">抱歉没有获取到信息 请尝试刷新</a></span>'));
        $div.append($('<span style="padding:0em 5% 0em 5%;"><a class="m-1 p-0 btn btn-secondary index_list index_list-all" style="border:0;border-radius:7px;height:3em;line-height:3em;width:90%" href="mailto:queziaa31@gmail.com">或联系我queziaa31@gmail.com</a></span>'));
    }else{
        for(i in index_list)
            $div.append('<span><a onclick="record(this,'+index_list[i]+');" class="p-0 btn btn-secondary index_list" style="border:0;margin:6.3px;border-radius:40px;height:3em;line-height:3em;width:3em" href="###">'+index_list[i]+'</a></span>');
        $div.append($('<span style="padding:0em 5% 0em 5%;"><a class="m-1 p-0 btn btn-secondary index_list index_list-all" onclick="record(this,-1);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:90%" href="###">全部</a></span>'));
    }
    $div.append($('<h3 class="text-center my-3">选择显示信息</h3>'));
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-2);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">硬币数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-3);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">弹幕数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-4);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">分享数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-5);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">播放数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list" onclick="record(this,-6);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">回复数</a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary stat_list stat_list_all" onclick="record(this,-7);" style="border:0;margin:2.5%;border-radius:7px;height:3em;line-height:3em;width:45%" href="###">显示全部</a></span>');
    $div.append($('<h3 class="text-center my-3">图表调整</h3>'));
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili img-btn" onclick="record(this,-10);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_longarrowaltleft zi_2x"></i></a></span>');
    $div.append('<span class="h5 img_y">位置:1</span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili img-btn" onclick="record(this,-20);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_longarrowaltright zi_2x"></i></a></span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili img-btn" onclick="record(this,-30);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_minuscircle zi_2x"></i></a></span>');
    $div.append('<span class="h5 img_m">缩放:1</span>');
    $div.append('<span><a class="p-0 btn btn-secondary bg-bilibili img-btn" onclick="record(this,-40);" style="border:0;border-radius:7px;height:3em;line-height:3em;width:3em"href="###"><i class="zi zi_pluscircle zi_2x"></i></a></span>');
    $chart_body.append($div);
    var $img = $('<div id="canvas-holder1"></div>');
    $img.append('<canvas id="chart1" class="chartjs-render-monitor"></canvas>');
    $img.append('<div class="chartjs-tooltip" id="tooltip-0" style="opacity: 1; top: 409.698px; left: 953.018px;">June: -41</div>');
    $img.append('<div class="chartjs-tooltip" id="tooltip-1" style="opacity: 1; top: 274.152px; left: 953.018px;">June: 16</div>');
    $img = $('<div class="'+col_3+'"></div>').append($img);
    $chart_body.append($img);    
    $('.index_list').toggleClass('bg-bilibili',true);
    $('.stat_list').toggleClass('bg-bilibili',true);
    tt.removeAttr("onclick");
    tt.removeAttr('class');
    tt[0].className=col_1;
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
    window["ajax_chart"]={'index':-1,'info':[-2,-3,-4,-5,-6],'img_y':1,'img_m':1};
    Waves.attach('.btn', ['waves-float']);
    onclick_chart();
}
function record(tt,sum){
    var $tt = $(tt);
    if(sum>=0){
        ajax_chart['index']=Number($tt.text());
        $('.index_list').toggleClass('bg-bilibili',false);
        $tt.toggleClass('bg-bilibili',true);
        onclick_chart();
    }else if(sum == -1){
        if($tt.hasClass('bg-bilibili')==false){
            $('.index_list').toggleClass('bg-bilibili',true);            
            ajax_chart['index']=-1;
            onclick_chart();
        }else{
            ajax_chart['index']=null;
            $('.index_list').toggleClass('bg-bilibili',false);
        }
    }else if(sum == -7){
        if($tt.hasClass('bg-bilibili')==false){
            ajax_chart['info']=[-2,-3,-4,-5,-6];
            $('.stat_list').toggleClass('bg-bilibili',true);
            Load_img();      
        }else{
            ajax_chart['info']=[];
            $('.stat_list').toggleClass('bg-bilibili',false);
        }
    }else if(sum<0 && sum>-10){
        if($.inArray(sum, ajax_chart['info']) == -1){
            ajax_chart['info'].push(sum);
            Load_img();
        }else{
            ajax_chart['info'].splice($.inArray(sum, ajax_chart['info']),1);
            Load_img();
        }
        if(ajax_chart['info'].length==5)
            $('.stat_list_all').toggleClass('bg-bilibili',true);
        else
            $('.stat_list_all').toggleClass('bg-bilibili',false);
            $tt.toggleClass('bg-bilibili');
    }else if(sum ==-10 && ajax_chart['img_y']>1){
        ajax_chart['img_y']-=1;
        $('.img_y').text('位置:'+ajax_chart['img_y']);
        Load_img();
    }else if(sum ==-30 && ajax_chart['img_m']>1){
        ajax_chart['img_m']-=1;
        $('.img_m').text('缩放:'+ajax_chart['img_m']);
        Load_img();
    }else if(sum ==-20){
        if (ajax_chart['hour_freq']/ajax_chart['img_m']-ajax_chart['img_y']-1>=21){
            ajax_chart['img_y']+=1;
            $('.img_y').text('位置:'+ajax_chart['img_y']);
            Load_img();
        }
    }else if(sum ==-40){
        if (ajax_chart['hour_freq']/(ajax_chart['img_m']+1)-ajax_chart['img_y']>21){
            ajax_chart['img_m']+=1;
            $('.img_m').text('缩放:'+ajax_chart['img_m']);
            Load_img();
        }
    }else{
        ;
    }
}
function post_index(id){
    var result;
    csrfmiddlewaretoken = $('#chart').attr('csrf_token');
    csrfmiddlewaretoken = csrfmiddlewaretoken.substring(csrfmiddlewaretoken.indexOf("value='")+7,csrfmiddlewaretoken.indexOf("' />"));
    $.ajax({
        type:"POST",	
        url:"/post_index/",
        data:{
            id:id,
            csrfmiddlewaretoken:csrfmiddlewaretoken,
        },
        async : false,
        dataType:"json",
        success:function(data){
            result =  data['data'];
        },
        error:function(jqXHR,textStatus,errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
            result = "发生错误 请尝试刷新";
        }
    });
    return result;
}
function onclick_chart(){
    var id = $('#chart').find('[temp-id]').attr('temp-id');
    var csrfmiddlewaretoken = $('#chart').attr('csrf_token');
    var csrfmiddlewaretoken = csrfmiddlewaretoken.substring(csrfmiddlewaretoken.indexOf("value='")+7,csrfmiddlewaretoken.indexOf("' />"));
    $.ajax({
        type:"POST",	
        url:"/post_animation_info/",
        data:{
            index:ajax_chart['index'],
            id:id,
            csrfmiddlewaretoken:csrfmiddlewaretoken,
        },
        dataType:"json",
        success:function(data){
            window['Load_img_data'] = data; 
            ajax_chart['hour_freq'] = data['hour_freq'];
            $('.img_y').text('位置:1');
            $('.img_y').text('位置:1');
            ajax_chart['img_m'] = 1;
            ajax_chart['img_y'] = 1;
            Load_img(data);
        },
        error:function(jqXHR,textStatus,errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
}
function Load_img(data){
    if (data == undefined){
        data = Load_img_data;
    }
    var lineChartData = [];
    if($.inArray(-2,ajax_chart['info'])!=-1){lineChartData.push(screen_line_chart('硬币数','coin',data,window.chartColors.blue));}
    if($.inArray(-3,ajax_chart['info'])!=-1){lineChartData.push(screen_line_chart('弹幕数','danmaku',data,window.chartColors.grey));}
    if($.inArray(-4,ajax_chart['info'])!=-1){lineChartData.push(screen_line_chart('分享数','share',data,window.chartColors.purple));}
    if($.inArray(-5,ajax_chart['info'])!=-1){lineChartData.push(screen_line_chart('播放数','view',data,window.chartColors.red));}
    if($.inArray(-6,ajax_chart['info'])!=-1){lineChartData.push(screen_line_chart('回复数','reply',data,window.chartColors.yellow));}
    // alert(lineChartData[0]['data']);
    console.log(lineChartData);
    color_init({'labels':  screen_line_chart_date(data['start']),'datasets':lineChartData});
}
function screen_line_chart(label_str,dict_key,data,chartColors){
    var color = Chart.helpers.color;
    var img_y = ajax_chart['img_y'];
    var img_m = ajax_chart['img_m'];
    var datasets_data = data[dict_key].slice(img_y*img_m);
    var datasets_data_min = [];
    // var datasets_data_length = datasets_data.length
    for(var i=0;i<21;i++)
        datasets_data_min.push(datasets_data[i*img_m]);
    // if(img_m!=1){
    //     for(i in datasets_data)
    //         if(datasets_data_length-i/img_m!=0)
    //             datasets_data.splice(datasets_data_length-i-1,1);
    // }
    return {
        'label': label_str,
        'backgroundColor': color(chartColors).alpha(0.2).rgbString(),
        'borderColor': chartColors,
        'pointBackgroundColor': chartColors,
        'data': datasets_data_min
    }
}
function screen_line_chart_date(start){
    var img_y = ajax_chart['img_y'];
    var img_m = ajax_chart['img_m'];
    var labels_data = [];
    start = start + img_y*img_m*3600;
    for(var i=1;i<=11;i++){
        labels_data.push(getMyDate(start));
        start = start + img_m*3600;
        labels_data.push('');
    }
    labels_data.pop();
    return labels_data
}
function getMyDate(str){  
    var oDate = new Date(str*1000),  
    oYear = oDate.getFullYear(),  
    oMonth = oDate.getMonth()+1,  
    oDay = oDate.getDate(),  
    oHour = oDate.getHours(),  
    oTime = oYear +'年'+ oMonth +'月'+ oDay +'日'+ oHour+'时';
    return oTime.substring(2);  
};
function color_init(lineChartData) {
	var chartEl = document.getElementById('chart1');
	new Chart(chartEl, {
		type: 'line',
		data: lineChartData,
		options: {
			title: {
				display: true,
			},
			tooltips: {
				enabled: false,
				mode: 'index',
				intersect: false,
				custom: customTooltips
			}
		}
	});
};
var customTooltips = function (tooltip) {
    $(this._chart.canvas).css('cursor', 'pointer');	
    var positionY = this._chart.canvas.offsetTop;
    var positionX = this._chart.canvas.offsetLeft;	
    $('.chartjs-tooltip').css({
		opacity: 0,
    });	
    if (!tooltip || !tooltip.opacity) {
		return;
	}	if (tooltip.dataPoints.length > 0) {
		tooltip.dataPoints.forEach(function (dataPoint) {
			var content = [dataPoint.xLabel, dataPoint.yLabel].join(': ');
            var $tooltip = $('#tooltip-' + dataPoint.datasetIndex);
            $tooltip.html(content);
			$tooltip.css({
				opacity: 1,
				top: positionY + dataPoint.y + 'px',
				left: positionX + dataPoint.x + 'px',
			});
		});
	}
};