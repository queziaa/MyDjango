from __future__ import absolute_import
from celery import shared_task
from my_blog.settings import CELERY_ERROR_LOG
from article.models import Search_db
import datetime
import time


@shared_task
def test():
    fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
    fp.write('$'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+'\n')
    fp.close()

@shared_task
def SearchArrangementThread():
    try:
        search = Search_db.objects.filter(examine_time__lte=datetime.date.today()-datetime.timedelta(days=2))
    except Exception as e:
        fp = open(CELERY_ERROR_LOG,'a+',encoding='utf-8')
        fp.write('$'+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+srt(e)+'\n')
        fp.close()
    else:
        search.delete()