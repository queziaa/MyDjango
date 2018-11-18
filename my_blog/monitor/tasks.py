from __future__ import absolute_import
from celery import shared_task
from my_blog.settings import CELERY_ERROR_LOG
from monitor.spider_bilibili import main_spider_time,main_spider_data
from datetime import datetime, timedelta
import os,traceback,time

@shared_task
def spider_time():
    try:
        celery_list = main_spider_time(CELERY_ERROR_LOG)
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$spider_time:ERROR@'+traceback.format_exc()+'\n')
        fp.close()
    else:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$spider_time:OK@'+str(celery_list)+'\n')
        fp.close()
        # try:
        #     for i_celery in celery_list:
        #         time_countdown = i_celery['start']-int(time.time())
        #         spider_data.apply_async(countdown=time_countdown,args=(i_celery,))
        #         fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        #         fp.write(time.strftime('%Y-%m-s%d %H:%M:%S', time.localtime(time.time()))+'apply_async:OK@'+str(i_celery)+'\n')
        #         fp.close()
        # except Exception as e:
        #     fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        #     fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$apply_async:ERROR@'+str(e)+'\n')
        #     fp.close()

@shared_task
def spider_data():
    try:
        log = main_spider_data(CELERY_ERROR_LOG)
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$spider_data:ERROR@'+traceback.format_exc()+'\n')
        fp.close()
    else:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'$spider_data:OK@'+str(log)+'\n')
        fp.close()    
