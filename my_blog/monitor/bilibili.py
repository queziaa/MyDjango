import requests
import json
import copy
import pymongo
import os
import time

error_log = r'/home/que/bilibili_monitor.log'
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
mongoHost = '127.0.0.1'
mongoPort = 27017
mongoName = 'monitor'
mongodb = 'start_time'
client = pymongo.MongoClient(host=mongoHost,port=mongoPort)
mongopost = client[mongoName][mongodb]

def count_time(start):
    hour_freq = 0
    hour = start
    day_freq = 0
    day = start
    while True:
        if hour < int(time.time()):
            break
        hour += 3600
        hour_freq += 1
        if hour_freq > 24:
            hour = None
            hour_freq = None
            break
    while True:
        if day < int(time.time()) and day_freq < 7:
            break
        day += 86400
        day_freq += 1
        if day_freq > 24:
            day = None
            day_freq = None
            break
    return {"hour_freq":hour_freq,"hour":hour,"day_freq":day_freq,"day":day}

def main():
    try:
        post_text = requests.get(url,headers=headers,timeout=10)
    except Exception as e:
        fp = open(error_log,'a+',encoding='utf-8')
        fp.write('\n'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+' : '+str(e))
        fp.close()
    else:
        result = json.loads(post_text.text)["result"]
        for i_result in result:
            for i_seasons in i_result["seasons"]:
                title = i_seasons['title']
                if title == None:
                    continue
                if mongopost.find_one({'title':title}) == None:
                    temp = {}
                    temp["title"] = i_seasons['title']
                    temp["cover"] = i_seasons['cover']
                    temp["time"] = []
                    if 'pub_index' not in i_seasons:
                        continue
                    temp["time"].append({'index':int(i_seasons['pub_index'][1:-1]),'ep_id':i_seasons['ep_id'],'start':i_seasons['pub_ts']})
                    temp.update(count_time(i_seasons['pub_ts']))
                    mongopost.insert(temp)
                else:
                    if mongopost.find_one({"$and":[{"title":title},{"time":{"$elemMatch":{"index":int(i_seasons['pub_index'][1:-1])}}}]}) == None:
                        temp = {'index':int(i_seasons['pub_index'][1:-1]),'ep_id':i_seasons['ep_id'],'start':i_seasons['pub_ts']}
                        temp.update(count_time(i_seasons['pub_ts']))
                        mongopost.update({"title":title},{"$push":{"time":temp}})


if __name__ == '__main__':
    main()