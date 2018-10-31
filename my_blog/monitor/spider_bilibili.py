import requests,json,pymongo,os,time,re,traceback

url = 'https://bangumi.bilibili.com/web_api/timeline_global'
headers = {"Accept":"application/json, text/plain, */*",
"Host":"bangumi.bilibili.com",
"Referer":"https://www.bilibili.com/anime/timeline/",
"Origin":"https://www.bilibili.com",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Pragma":"no-cache",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
client = pymongo.MongoClient(host='localhost', port=27017, connect=False)
mongopost = client['monitor']['start_time']

def count_time(start):
    hour_freq = 0
    hour = start
    hour_data = []
    day_freq = 0
    day = start
    day_data = []
    while True:
        if hour > int(time.time()):
            break
        hour += 3600
        hour_freq += 1
        hour_data.append(None)
        if hour_freq >= 24:
            hour = None
            hour_freq = None
            hour_data = None
            break
    while True:
        if day > int(time.time()):
            break
        day += 86400
        day_freq += 1
        day_data.append(None)
        if day_freq >= 31:
            day = None
            day_freq = None
            day_data = None
            break
    return {"hour":hour,"hour_freq":hour_freq,"hour_data":hour_data,"day":day,"day_freq":day_freq,"day_data":day_data}

def main_spider_time(CELERY_ERROR_LOG):
    # celery_list = []
    post_text = requests.get(url,headers=headers,timeout=10)
    result = json.loads(post_text.text)["result"]
    for i_result in result:
        for i_seasons in i_result["seasons"]:
            title = i_seasons['title']
            if title == None or 'pub_index' not in i_seasons :
                continue
            i_seasons['pub_index'] = int(''.join(re.findall("\d+",i_seasons['pub_index'])))
            if mongopost.find_one({'title':title}) == None:
                temp = {}
                temp["title"] = title
                temp["cover"] = i_seasons['cover']
                temp["time"] = []
                temp["time"].append({'index':i_seasons['pub_index'],'season_id':i_seasons['season_id'],'start':i_seasons['pub_ts']})
                temp['time'][0].update(count_time(i_seasons['pub_ts']))
                mongopost.insert(temp)
                # if temp['time'][0]['hour'] != None:
                #     celery_list.append({'season_id':i_seasons['season_id'],'title':title,'index':i_seasons['pub_index'],'main_start':i_seasons['pub_ts'],'start':temp['time'][0]['hour'],'freq':temp['time'][0]['hour_freq'],'type':'hour'})
                # if temp['time'][0]['day'] != None:
                #     celery_list.append({'season_id':i_seasons['season_id'],'title':title,'index':i_seasons['pub_index'],'main_start':i_seasons['pub_ts'],'start':temp['time'][0]['day'],'freq':temp['time'][0]['day_freq'],'type':'day'})
            else:
                if mongopost.find_one({"$and":[{"title":title},{"time":{"$elemMatch":{"index":i_seasons['pub_index']}}}]}) == None:
                    temp = {'index':i_seasons['pub_index'],'season_id':i_seasons['season_id'],'start':i_seasons['pub_ts']}
                    temp.update(count_time(i_seasons['pub_ts']))
                    mongopost.update({"title":title},{"$push":{"time":temp}})
                    # if temp['hour'] != None:
                    #     celery_list.append({'season_id':i_seasons['season_id'],'title':title,'index':i_seasons['pub_index'],'main_start':i_seasons['pub_ts'],'start':temp['hour'],'freq':temp['hour_freq'],'type':'hour'})
                    # if temp['day'] != None:
                    #     celery_list.append({'season_id':i_seasons['season_id'],'title':title,'index':i_seasons['pub_index'],'main_start':i_seasons['pub_ts'],'start':temp['day'],'freq':temp['day_freq'],'type':'day'})
    # return celery_list

def main_spider_data(CELERY_ERROR_LOG):
    for find_data in mongopost.find():
        for i_time in find_data['time']:
            if i_time['hour'] != None:
                temp = time_range(i_time['hour'],420)
                if  temp == 0:
                    i_time = spider_requests(i_time,'hour',CELERY_ERROR_LOG)
                elif temp == -1:
                    while time_range(i_time['hour'],420) != -1:
                        i_time['hour'] += 3600
                        i_time['hour_freq'] += 1
                        i_time['hour_data'].append(None)
                        if i_time['hour_freq'] >= 24:
                            i_time['hour_freq'] = None
                            i_time['hour'] = None
                            break
                    if time_range(i_time['hour'],420) == 0:
                        i_time = spider_requests(i_time,'hour',CELERY_ERROR_LOG)
                else:
                    pass
            if i_time['day'] != None:
                temp = time_range(i_time['day'],3600)
                if  temp == 0:
                    i_time = spider_requests(i_time,'day',CELERY_ERROR_LOG)
                elif temp == -1:
                    while time_range(i_time['day'],3600) != -1:
                        i_time['day'] += 86400
                        i_time['day_freq'] += 1
                        i_time['day_data'].append(None)
                        if i_time['day_freq'] >= 24:
                            i_time['day_freq'] = None
                            i_time['day'] = None
                            break
                    if time_range(i_time['day'],3600) == 0:
                        i_time = spider_requests(i_time,'day',CELERY_ERROR_LOG)
                else:
                    pass
            if i_time['hour'] != None or i_time['day'] != None:
                mongopost.update({'title':find_data['title']},{'$pull':{'time':{'index':i_time['index']}}})
                mongopost.update({'title':find_data['title']},{'$push':{'time':i_time}})

def spider_requests(i_time,hour_or_day,CELERY_ERROR_LOG):
    url='https://bangumi.bilibili.com/ext/web_api/season_count?season_type=1&season_id=' + str(i_time['season_id'])
    try:
        post_text = requests.get(url,headers=headers,timeout=10)
        result = json.loads(post_text.text)
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'spider_requests:ERROR@'+traceback.format_exc()+'\n')
        fp.close()
    else:
        if hour_or_day == 'day':
            i_time["day"] += 86400
            i_time["day_freq"] += 1
            i_time["day_data"].append(result['result'])
            if i_time['day_freq'] >= 24:
                i_time['day_freq'] = None
                i_time['day'] = None
        elif hour_or_day == 'hour':
            i_time['hour'] += 3600
            i_time['hour_freq'] += 1
            i_time['hour_data'].append(result['result'])
            if i_time['hour_freq'] >= 24:
                i_time['hour_freq'] = None
                i_time['hour'] = None
        else:
            pass
    return i_time

def time_range(time_data,r):
    if time_data == None:
        return 1
    t = int(time.time())
    if t + r < time_data:
        return 1
    if t - r > time_data:
        return -1
    return 0

if __name__ == '__main__':
    CELERY_ERROR_LOG = r'/home/que-linux/bilibili_monitor.log'
    main_spider_time(CELERY_ERROR_LOG)