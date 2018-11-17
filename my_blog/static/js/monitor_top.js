$(function () {
    window.top_data={'data_type':0,'time':0,'calcu_type':0,'sort_type':0,'shelves':0};
    window.calcu_type = $('.calcu_type'); 
    window.calcu_type.prop('disabled', true);
    window.calcu_type.selectpicker('refresh');
    window.calcu_type_parent = $('.calcu_type');
    window.calcu_type_parent.attr("title","");
    window.calcu_type_parent.attr("data-original-title","时间为现在时只能查询数量");
    window.calcu_type_parent.attr("data-toggle","tooltip");
    $("[data-toggle='tooltip']").tooltip();
    $("[role='button']").attr('title','');
});
function sele_onch(type,th){
    if(type == 0){
        window.top_data['data_type'] = th.selectedIndex;
    }else if(type == 1){                    
        window.calcu_type.prop('disabled', false);
        window.calcu_type.selectpicker('refresh');
        window.calcu_type_parent.parent().attr("data-original-title","");
        $("[data-toggle='tooltip']").tooltip();
        if(th.selectedIndex == 0){
            window.top_data['time'] = 0;
            window.top_data['calcu_type'] = 0;
            window.calcu_type.prop('disabled', true);
            window.calcu_type.selectpicker('refresh');
            window.calcu_type.selectpicker('val', '数量');
            $('.time_sele').addClass('display_none');
            window.calcu_type_parent.attr("title","");
            window.calcu_type_parent.attr("data-original-title","时间为现在时只能查询数量");
            window.calcu_type_parent.attr("data-toggle","tooltip");
            $("[data-toggle='tooltip']").tooltip();
            return false;
        }else if(th.selectedIndex == 1){
            window.top_data['time'] = 1;
        }else if(th.selectedIndex == 2){
            window.top_data['time'] = 24;
        }
        if(th.selectedIndex == 3){
            window.top_data['time'] = 3;
            $('.time_sele').removeClass('display_none');
            return false;
        }else{
            $('.time_sele').addClass('display_none');
        }
    }else if(type == 2){
        window.top_data['calcu_type'] = th.selectedIndex;
    }else if(type == 3){
        window.top_data['sort_type'] = th.selectedIndex;
    }else if(type == 4){
        if(th.selectedIndex == 0){
            window.top_data['shelves'] = 24;
        }else if(th.selectedIndex == 1){
            window.top_data['shelves'] = 168;
        }else if(th.selectedIndex == 2){
            window.top_data['shelves'] = -1;
        }else if(th.selectedIndex == 3){
            window.top_data['shelves'] = 3;
            $('.shelves_sele').removeClass('display_none');
            return false;
        }else{
            $('.shelves_sele').addClass('display_none');
        }
        window.top_data['shelves'] = th.selectedIndex;
    }else{}
    top_post();
}
function inp_onb(th){
    th = $(th);
    if(isNaN(parseInt(th[0].value))){
        th.addClass('alert-danger');
    }else{
        th.removeClass('alert-danger');
        top_post();
    }
}
function top_post(){
    if(window.top_data['time'] == 3){
        if(isNaN(parseInt($('.time_sele')[0].value)))
            return false
        else
            window.top_data['time'] = parseInt($('.time_sele')[0].value);
    }
    if(window.top_data['shelves'] == 3){
        if(isNaN(parseInt($('.shelves_sele')[0].value)))
            return false
        else
            window.top_data['shelves'] = parseInt($('.shelves_sele')[0].value)*24;
    }
    $.ajax({
        type:"POST",
        url:"/top_list_post/",
        data:{
            data_type:window.top_data['data_type'],
            time:window.top_data['time'],
            calcu_type:window.top_data['calcu_type'],
            sort_type:window.top_data['sort_type'],
            shelves:window.top_data['shelves'],
            csrfmiddlewaretoken:GETcsrfmiddlewaretoken(),
        },
        dataType:"json",
        success:function(data){
            
        },
        error:function(jqXHR,textStatus,errorThrown){
        }
    });
}