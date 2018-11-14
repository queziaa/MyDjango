#coding=utf-8
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
mongopost = client['monitor']['start_time_4']


def main_spider_time(CELERY_ERROR_LOG):
    post_text = requests.get(url,headers=headers,timeout=10)
    try:
        result = json.loads(post_text.text)["result"]
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'spider_requests:ERROR@'+post_text.text+traceback.format_exc()+'\n')
        fp.write(post_text.text)
        fp.close()
    for i_result in result:
        for i_seasons in i_result["seasons"]:
            # if title == None or 'pub_index' not in i_seasons :
            #     continue
            i_seasons['pub_index'] = int(''.join(re.findall("\d+",i_seasons['pub_index'])))
            if not mongopost.find_one({'season_id':i_seasons['season_id']}):
                temp = {}
                temp["title"] = i_seasons['title']
                temp["cover"] = i_seasons['cover']
                temp["season_id"] = i_seasons['season_id']
                temp["time"] = []
                aid = sid_aid(i_seasons['season_id'],i_seasons['pub_index'])
                if aid == -1:
                    continue                    # 彻查season_id
                temp["time"].append({'index':i_seasons['pub_index'],'start':i_seasons['pub_ts'],'aid':aid}) 
                temp['time'][0].update(count_time(i_seasons['pub_ts']))
                mongopost.insert(temp)
            else:
                if not mongopost.find_one({"$and":[{"season_id":i_seasons['season_id']},{"time":{"$elemMatch":{"index":i_seasons['pub_index']}}}]}):
                    aid = sid_aid(i_seasons['season_id'],i_seasons['pub_index'])
                    if aid == -1:
                        continue
                    temp = {'index':i_seasons['pub_index'],'start':i_seasons['pub_ts'],'aid':aid}
                    temp.update(count_time(i_seasons['pub_ts']))
                    mongopost.update({"season_id":i_seasons['season_id']},{"$push":{"time":temp}})
                    
def main_spider_data(CELERY_ERROR_LOG):
    for find_data in mongopost.find():
        for i_time in find_data['time']:
            while time_range(i_time['hour'],180) == -1:
                i_time['hour'] += 3600
                i_time['hour_freq'] += 1
                i_time['coin'].append(None)
                i_time['danmaku'].append(None)
                i_time['share'].append(None)
                i_time['view'].append(None)
                i_time['reply'].append(None)
            if time_range(i_time['hour'],180) == 0:
                i_time = spider_requests(i_time,CELERY_ERROR_LOG)
            mongopost.update({'title':find_data['title']},{'$pull':{'time':{'index':i_time['index']}}})
            mongopost.update({'title':find_data['title']},{'$push':{'time':i_time}})

def spider_requests(i_time,CELERY_ERROR_LOG):
    try:
        url='https://api.bilibili.com/x/web-interface/view?aid=' + str(i_time['aid'])
        headers['Host'] = 'api.bilibili.com'
        post_text = requests.get(url,headers=headers,timeout=10)
        if post_text.status_code != 200:
            fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
            fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$spider_requests:ERRORget404@'+url+post_text.text+'\n')
            fp.close()
            return 1
        result = json.loads(post_text.text)['data']['stat']
        i_time['hour'] += 3600
        i_time['hour_freq'] += 1
        i_time['coin'].append(result['coin'])
        i_time['danmaku'].append(result['danmaku'])
        i_time['share'].append(result['share'])
        i_time['view'].append(result['view'])
        i_time['reply'].append(result['reply'])
        return i_time
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'spider_requests:ERROR???@'+traceback.format_exc()+url+post_text.text+'\n')
        fp.close()
        return 1

def time_range(time_data,r):
    if time_data == None:
        return 1
    t = int(time.time())
    if t + r < time_data:
        return 1
    if t - r > time_data:
        return -1
    return 0

def count_time(start):
    coin = []
    danmaku = []
    share = []
    view = []
    reply = []
    hour_freq = 0
    hour = start
    while True:
        if hour > int(time.time()):
            break
        hour += 3600
        hour_freq += 1
    return {"hour":hour,"hour_freq":hour_freq,'coin':coin,'danmaku':danmaku,'share':share,'view':view,'reply':reply}

def sid_aid(s_id,index):        
        url='https://www.bilibili.com/bangumi/play/ss' + str(s_id)
        headers['Host'] = 'www.bilibili.com'
        post_text = requests.get(url,headers=headers,timeout=10)
        text = json.loads(re.findall('__INITIAL_STATE__.*function',post_text.text)[0][18:-10])['epList']
        for i in text:
            if i['index'] == str(index):
                return int(i['aid'])
        return -1

if __name__ == '__main__':
    CELERY_ERROR_LOG = r'/home/que-linux/bilibili_monitor.log'
    main_spider_time(CELERY_ERROR_LOG)
    main_spider_data(CELERY_ERROR_LOG)