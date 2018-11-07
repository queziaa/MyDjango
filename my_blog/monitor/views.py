from django.shortcuts import render
from django.http import HttpResponse
from monitor.models import start_time_2 as start_time
from my_blog.settings import CELERY_ERROR_LOG 
import os,time

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

    log = ''

    ranking=[]
    ranking_data = []
    ranking_time_temp = start_time.objects.all()
    for i in ranking_time_temp:
        for i_i in i['time']:
            temp = {}
            if len(i_i['view']) >= 25:
                temp = {'title':i['title'],'index':i_i['index'],'view':i_i['view'][-1]-i_i['view'][-25]}
                log+=str(i_i)
            elif len(i_i['view']) == 0:
                log+='0'
                continue
            elif len(i_i['view']) < 25:
                # log+='2'
                temp = {'title':i['title'],'index':i_i['index'],'view':i_i['view'][-1]-i_i['view'][1]}
            else:
                # log+='3'
                continue
            s=0
            if len(ranking_data) <= 6 :
                ranking_data.append(temp)
                continue
            for ranking_i in ranking_data:
                if ranking_i['view'] < temp['view']:
                    ranking_data.insert(s,temp)        
                    if len(ranking_data) > 6:
                        ranking_data = ranking_data[:6]
                    break
                s+=1
    temp = []

    ranking.append({'title':'今日播放数','list':ranking_data})
    ranking.append({'title':'今日播放数','list':ranking_data})
    ranking.append({'title':'今日播放数','list':ranking_data})
    ranking.append({'title':'今日播放数','list':ranking_data})

    # a = ['xxxxxxxxxxxxx','xxxxxxxxxxxxx','xxxxxxxxxxxxx']
    # aa.append(a) 
    # aa.append(a) 
    # aa.append(a) 
    # aa.append(a) 
    # ranking.append({'title':'今日播放数增长率','list':aa})
    # ranking.append({'title':'今日推荐数','list':aa})
    # ranking.append({'title':'今日推荐数增长率','list':aa})

    return render(request,'monitor_home.html',{'start':start_data,'ranking':ranking,'log':log})
