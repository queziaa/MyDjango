from django.shortcuts import render
from django.http import HttpResponse
from monitor.models import start_time_2 as start_time
from my_blog.settings import CELERY_ERROR_LOG 
import os,time,json

def home(request):
    start_data = []
    start_time_temp = start_time.objects.all()
    for i in start_time_temp:
        hour_max = {}
        for i_i in i['time']:
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
        start_data_i['start'] = time.strftime('%m月%d日%H:%M', time.localtime(start_data_i['start']))
        start_data_i['hour'] = time.strftime('%m月%d日%H:%M', time.localtime(start_data_i['hour']))

    ranking=[]
    inc_num = lambda x,y:x-y
    inc_per = lambda x,y:(" %.2f%%" % ((x-y)/y*100))
    ranking.append({'title':'今日播放数','list':ranking_get('view',inc_num,False)})
    ranking.append({'title':'今日播放数增长率','list':ranking_get('view',inc_per,True)})
    ranking.append({'title':'今日分享数','list':ranking_get('share',inc_num,False)})
    ranking.append({'title':'今日分享数增长率','list':ranking_get('share',inc_per,True)})
    return render(request,'monitor_home.html',{'start':start_data,'ranking':ranking})

def ranking_get(ranking_type,col_lam,blank_2):
    ranking_data = []
    ranking_time_temp = start_time.objects.all()
    for i in ranking_time_temp:
        for i_i in i['time']:
            temp = {}
            if len(i_i[ranking_type]) >= 25:
                if not blank_2 or i_i[ranking_type][-25] != 0:
                    temp = {'title':i['title'],'index':i_i['index'],ranking_type:col_lam(i_i[ranking_type][-1],i_i[ranking_type][-25])}
                else:
                    continue
            elif len(i_i[ranking_type]) <= 1:
                continue
            elif len(i_i[ranking_type]) < 25 and not blank_2:
                a = i_i[ranking_type]
                temp = {'title':i['title'],'index':i_i['index'],ranking_type:col_lam(i_i[ranking_type][-1],i_i[ranking_type][1])}
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
    return ranking_data

def post_animation_info(request):
    data = None
    if request.method == 'POST':
        id=request.POST.get('id','')
        index=int(request.POST.get('index',''))
        start_time_temp = start_time.objects.get(id=id)['time']
        if index == -1:
            data = {'coin':[],'danmaku':[],'share':[],'view':[],'reply':[],'min_start':999999999}
            for i in start_time_temp:
                if i['start']  < data['min_start']:
                    data['min_start'] = i['start']
                    data['hour_freq'] = i['hour_freq']
                data['start'] = data['min_start']
                while True:
                    if data['min_start'] > int(time.time()):
                        break
                    data['min_start'] += 3600
                    data['coin'].append(0)
                    data['danmaku'].append(0)
                    data['share'].append(0)
                    data['view'].append(0)
                    data['reply'].append(0)
            for i in start_time_temp:
                deviation = int((i['start'] - data['min_start']) / 3600)
                for data_i in range(len(i['coin'])):
                    data['coin'][deviation+data_i] = i['coin'][data_i] 
                    data['danmaku'][deviation+data_i] = i['danmaku'][data_i] 
                    data['share'][deviation+data_i] = i['share'][data_i] 
                    data['view'][deviation+data_i] = i['view'][data_i] 
                    data['reply'][deviation+data_i] = i['reply'][data_i] 
            data = json.dumps(data)
        else:
            for i in start_time_temp:
                if i['index'] == index:
                    data = i.to_json()
                    break
    return HttpResponse(data)

def post_index(request):
    data = {'info':1,'data':[]}
    if request.method == 'POST':
        id=request.POST.get('id','')
        start_time_temp = start_time.objects.get(id=id)['time']
        for i in start_time_temp:
            data['data'].append(i['index'])
            data['info'] = 0
    return HttpResponse(json.dumps(data))