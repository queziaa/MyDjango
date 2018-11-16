from django.shortcuts import render
from django.http import HttpResponse
from monitor.models import start_time_4 as start_time
from my_blog.settings import CELERY_ERROR_LOG 
import os,time,json

def home(request):
    start_data = []
    start_time_temp = start_time.objects.all()
    for i in start_time_temp:
        hour_max = get_hour_max(i)
        if len(hour_max) == 0:
            continue
        if len(start_data) == 0:
            start_data.append({'hour':hour_max['hour'],'start':hour_max['start'],'id':i['id'],'cover':i['cover'],'title':i['title']})
            continue
        s = 0
        for start_i in start_data:
            if start_i['hour'] < hour_max['hour']:
                start_data.insert(s,{'hour':hour_max['hour'],'start':hour_max['start'],'id':i['id'],'cover':i['cover'],'title':i['title']})
                if len(start_data) > 12:
                    start_data = start_data[:12]
                break
            s+=1
        start_data.append({'hour':hour_max['hour'],'start':hour_max['start'],'id':i['id'],'cover':i['cover'],'title':i['title']})
        if len(start_data) > 12:
            start_data = start_data[:12]
    for start_data_i in start_data:
        start_data_i['start'] = str_time(start_data_i['start'])
        start_data_i['hour'] = str_time(start_data_i['hour'])

    ranking=[]
    inc_num = lambda x,y:x-y
    inc_per = lambda x,y:(" %.2f%%" % ((x-y)/y*100))
    ranking.append({'title':'今日播放数','list':ranking_get('view',0,inc_num,True,False)})
    ranking.append({'title':'24小时播放数增长率','list':ranking_get('view',24,inc_per,False,False)})
    ranking.append({'title':'今日分享数','list':ranking_get('share',0,inc_num,True,False)})
    ranking.append({'title':'24小时分享数增长率','list':ranking_get('share',24,inc_per,False,False)})
    return render(request,'monitor_home.html',{'start':start_data,'ranking':ranking})

def all(request):
    return render(request,'monitor_all.html')

def top(request):
    return render(request,'monitor_top.html')

# 播放    今日         数量                   最高
# 回复    于1小时前    相对以现在的增长数量      最低
# 分享    于24小时前   相对以现在的增长率
# 弹幕    自定义时间
# 硬币

def top_list_post(request):
    if request.method == 'POST':
        data_type = int(request.POST.get('data_type',''))
        time = int(request.POST.get('time',''))
        calcu_type = int(request.POST.get('calcu_type',''))
        sort_type = int(request.POST.get('sort_type',''))
        if data_type == 0:
            data_type = 'view'
        elif data_type == 1:
            data_type = 'reply'
        elif data_type == 2:
            data_type = 'share'
        elif data_type == 3:
            data_type = 'coin'
        elif data_type == 4:
            data_type = 'danmaku'
        else:
            return HttpResponse('{"code":1,"data_type"'+str(data_type)+'}')
        if calcu_type == 0:
            calcu_type = lambda x,y:y
            blank_2 = False
        elif calcu_type == 1:
            calcu_type = lambda x,y:x-y
            blank_2 = True
        elif calcu_type == 2:
            calcu_type = lambda x,y:(" %.2f%%" % ((x-y)/y*100))
            blank_2 = False
        else:
            return HttpResponse('{"code":1,"blank_2"'+str(blank_2)+'}')
        if sort_type == 0:
            sort_type == False
        elif sort_type == 1:
            sort_type == False
        else:
            return HttpResponse('{"code":1,"sort_type"'+str(sort_type)+'}') 
        start_data = ranking_get(data_type,time,calcu_type,blank_2,sort_type)
        return HttpResponse(json.dumps(start_data))


def id_list_post(request):
    if request.method == 'POST':
        key=request.POST.get('key','')
        start_data = []
        start_time_temp = start_time.objects.all()
        for i in start_time_temp:
            total = 0
            for i_i in i['time']:
                if key == 'start' or key == 'hour':
                    total = i_i[key]
                elif len(i_i[key])!=0:
                    total += i_i[key][-1] if i_i[key][-1] != None else 0
            count = 0
            if start_data == []:
                start_data.append({'id':str(i['id']),key:total})
                continue
            for start in start_data:
                if start[key] <= total:
                    start_data.insert(count,{'id':str(i['id']),key:total})
                    count = -1
                    break
                count+=1
            if(count != -1):
                start_data.append({'id':str(i['id']),key:total})
        start_data_range = len(start_data)
        if start_data_range >= 18:
            start_data_range = 18
        for i in range(start_data_range):
            start_data[i] = get_mod_mcard(start_data[i]['id'])
        for i in start_data:
            i['id'] = str(i['id'])
    return HttpResponse(json.dumps(start_data))

def mcard_list_post(request):
    CELERY_ERROR_LOG = r'/home/que-linux/bilibili_monitor.log'
    data = None
    if request.method == 'POST':
        id_list=request.POST.get('id_list','')
        key=request.POST.get('key','')
        start_data = []
        id_list = json.loads(id_list)
        for i in id_list:
            if(i != 'None'):
                start_data.append(get_mod_mcard(i))
    return HttpResponse(json.dumps(start_data))

def get_mod_mcard(id):
    start_data = {}
    mod_id = start_time.objects.get(id=id)
    start_data['cover'] = mod_id['cover']
    start_data['title'] = mod_id['title']
    hour_max = get_hour_max(mod_id)
    start_data['start'] = str_time(hour_max['start'])
    start_data['hour'] = str_time(hour_max['hour'])
    start_data['id'] = str(mod_id['id'])
    return start_data

def get_hour_max(mod):
    hour_max = {}
    for i_i in mod['time']:
        if i_i['hour'] == i_i['start']:
            pass
        elif hour_max == {}:
            hour_max['hour'] = i_i['hour']
            hour_max['start'] = i_i['start']
        elif i_i['hour'] > hour_max['hour']:
            hour_max['hour'] = i_i['hour']
            hour_max['start'] = i_i['start']
        else:
            pass
    return hour_max

def str_time(i):
    return time.strftime('%m月%d日%H:%M', time.localtime(i))

def ranking_get(ranking_type,time_apart,col_lam,blank_2,reverse_list):
    time_apart+=1
    ranking_data = []
    ranking_time_temp = start_time.objects.all()
    for i in ranking_time_temp:
        for i_i in i['time']:
            temp = {}
            if len(i_i[ranking_type])>= 1 and time_apart == 1 and i_i[ranking_type][-1]!=None:
                temp = {'id':str(i['id']),'title':i['title'],'index':i_i['index'],ranking_type:i_i[ranking_type][-time_apart]}
            elif len(i_i[ranking_type]) >= time_apart and i_i[ranking_type][-1]!=None and i_i[ranking_type][-time_apart]!=None:
                if blank_2 or i_i[ranking_type][-time_apart] != 0:
                    temp = {'id':str(i['id']),'title':i['title'],'index':i_i['index'],ranking_type:col_lam(i_i[ranking_type][-1],i_i[ranking_type][-time_apart])}
                else:
                    continue
            elif len(i_i[ranking_type]) <= 1:
                continue
            elif len(i_i[ranking_type]) < time_apart and blank_2 and i_i[ranking_type][-1]!=None and i_i[ranking_type][1]!=None:
                temp = {'id':str(i['id']),'title':i['title'],'index':i_i['index'],ranking_type:col_lam(i_i[ranking_type][-1],i_i[ranking_type][1])}
            else:
                continue
            s=0
            if len(ranking_data) <= 6:
                temp['num'] = temp[ranking_type]
                temp.pop(ranking_type)
                ranking_data.append(temp)
                continue
            for ranking_i in ranking_data:
                if ranking_i['num'] < temp[ranking_type]:
                    temp['num'] = temp[ranking_type]
                    temp.pop(ranking_type)
                    ranking_data.insert(s,temp)
                    if len(ranking_data) > 6:
                        ranking_data = ranking_data[:6]
                    break
                s+=1
    if(reverse_list):
        ranking_data.reverse()
    return ranking_data

def post_animation_info(request):
    data = None
    if request.method == 'POST':
        id=request.POST.get('id','')
        index=int(request.POST.get('index',''))
        start_time_temp = start_time.objects.get(id=id)['time']
        # if index == -1:
        #     data = {'coin':[],'danmaku':[],'share':[],'view':[],'reply':[],'min_start':None}
        #     for i in start_time_temp:
        #         if data['min_start'] == None:
        #             data['min_start'] = i['start']
        #             data['hour_freq'] = i['hour_freq'] 
        #         elif i['start']  < data['min_start']:
        #             data['min_start'] = i['start']
        #             data['hour_freq'] = i['hour_freq']
        #         data['start'] = data['min_start']
        #         for hour_freq in range(data['hour_freq']):
        #             data['coin'].append(0)
        #             data['danmaku'].append(0)
        #             data['share'].append(0)
        #             data['view'].append(0)
        #             data['reply'].append(0)
        #     for i in start_time_temp:
        #         differ = i['hour_freq']
        #         differ = data['hour_freq']
        #         differ = i['hour_freq']-data['hour_freq']
        #         for key in ['coin','danmaku','share','view','reply']:
        #             for hour_freq in range(i['hour_freq']):
        #                 data[key][differ+hour_freq]+=i[key][hour_freq]
                # deviation = int((i['start'] - data['min_start']) / 3600)
                # for data_i in range(len(i['coin'])):
                #     data['coin'][deviation+data_i] = i['coin'][data_i] 
                #     data['danmaku'][deviation+data_i] = i['danmaku'][data_i] 
                #     data['share'][deviation+data_i] = i['share'][data_i] 
                #     data['view'][deviation+data_i] = i['view'][data_i] 
                #     data['reply'][deviation+data_i] = i['reply'][data_i] 
            # data = json.dumps(data)
        # else:
        for i in start_time_temp:
            if i['index'] == index:
                data = i.to_json()
                break
    return HttpResponse(data)

def post_index(request):
    data = {'info':1,'data':[],'disabled':[]}
    if request.method == 'POST':
        id=request.POST.get('id','')
        start_time_temp = start_time.objects.get(id=id)['time']
        for i in start_time_temp:
            data['data'].append(i['index'])
            if len(i['coin']) == 0:
                data['disabled'].append(True)
            else:
                data['disabled'].append(False)
            data['info'] = 0
    return HttpResponse(json.dumps(data))