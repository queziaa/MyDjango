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
            if start_i['hour'] <= hour_max['hour']:
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

    # fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
    # fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+str(start_data)+'\n')
    # fp.close()
    ranking=[]
    aa = ['xxxxxxxxxxxxx','xxxxxxxxxxxxx','xxxxxxxxxxxxx','xxxxxxxxxxxxx','xxxxxxxxxxxxx','xxxxxxxxxxxxx']
    ranking.append({'title':'今日播放数','list':aa})
    ranking.append({'title':'今日播放数增长率','list':aa})
    ranking.append({'title':'今日推荐数','list':aa})
    ranking.append({'title':'今日推荐数增长率','list':aa})
    return render(request,'monitor_home.html',{'start':start_data,'ranking':ranking})
