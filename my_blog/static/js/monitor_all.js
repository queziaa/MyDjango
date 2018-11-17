$(function () {
    window.time_key = 'view';
    $("[data-toggle='tooltip']").tooltip();
    Waves.init();
    again_login(null,'view');
});
function again_login(tt,type){
    if(tt != null){
        tt = $(tt);
        $('.login_btn').find('i').toggleClass('text-bilibili',false);
        tt.addClass('text-bilibili');
    }
    $(".login_sign_1").remove();
    $(".dropload-down").remove();
    window.time_key = type;
    var paging = 0;//页码数
    $('.domUp').dropload({
        scrollArea : window,
        domUp : {
            domClass   : 'dropload-up',
            domRefresh : '<div class="dropload-refresh zi_2x">下拉刷新</div>',
            domUpdate  : '<div class="dropload-update zi_2x">释放更新</div>',
            domLoad    : '<div class="dropload-load  zi_2x"><span class="loading"></span>加载中...</div>'
        },
        domDown : {
            domClass   : 'dropload-down',
            domRefresh : '<div class="dropload-refresh zi_2x">下拉加载</div>',
            domLoad    : '<div class="dropload-load zi_2x"><span class="loading"></span>加载中...</div>',
            domNoData  : '<div class="dropload-noData zi_2x">已经没有更多了</div>'
        },
        loadDownFn : function(me){
            var load_list = [];
            var url = '';
            var ajax_data = {}
            if (paging==0){
                url = "/id_list_post/";
                ajax_data = {
                    key:time_key,
                    csrfmiddlewaretoken:GETcsrfmiddlewaretoken(),
                };
            }else{
                url = "/mcard_list_post/";
                ajax_data = {
                    key:time_key,
                    id_list:[],
                    csrfmiddlewaretoken:GETcsrfmiddlewaretoken(),
                }
                var temp = window.id_list.slice(0,18)
                for(i in temp){
                    ajax_data['id_list'].push(temp[i]['id']);
                }
                ajax_data['id_list']  = JSON.stringify(ajax_data['id_list']);
                window.id_list = window.id_list.slice(18);
            }
            $.ajax({
                type:"POST",	
                url:url,
                data:ajax_data,
                dataType:"json",
                success:function(data){
                    if(paging == 0){
                        paging++;
                        window.id_list = data.slice(18);
                        data = data.slice(0,18);
                    }
                    for(var i = data.length-1;i>=0;i--){
                        var $temp = $('<div class="mt-0 ml-2 mr-2 mb-2 mcard p-0 shadow-sm" style="border-radius:0px 0px 7px 7px;"></div>');
                        $temp.append($(''
                            +'<span><a class="text-muted" style="color:#f8f9fa!important;background-color:rgba(000, 000, 000, .50);position: absolute; '
                            +'bottom:2em; right:0.5em" href="###" data-toggle="tooltip" title="" data-original-title="更新时间" temp-storage-1="加入时间" '
                            +'temp-storage-2="'+data[i]['start']+'" onclick="switch_time(this);">'+data[i]['hour']+'</a></span><img class="card-img-top" '
                            +'src="'+data[i]['cover']+'" style="width: 100%; display: block;" ><div class="p-0 card-body" style="'
                            +'background-color:rgba(255, 255, 255, .5);border-radius:0px 0px 7px 7px;"><div class="d-flex '
                            +'justify-content-between align-items-center"><div class="btn-group" style="width:100%"><p class="m-0 text-center '
                            +'text-truncate text-overflow" style="width:100%" title="'+data[i]['title']+'">'+data[i]['title']+'</p></div></div></div>'
                        ))
                        $temp = $('<div class="p-0 col-xl-2 col-lg-3 col-md-3 col-sm-4 col-5 login_sign_1" onclick="pop_chart(this)" temp-id= "'+data[i]['id']+'"></div>').append($temp);
                        $('.domUp').before($temp);
                    }
                    $("[data-toggle='tooltip']").tooltip();
                    if(window.id_list.length==0){
                        me.lock();
                        me.noData();
                    }
                    setTimeout(function(){
                        me.resetload();
                    },1000);
                },
                error:function(){
                    me.resetload();
                    me.lock();
                    me.noData();
                    $('.dropload-noData').text('获取数据失败尝试刷新或联系我:queziaa31@gmail.com');
                }
            });
        },
    });
}