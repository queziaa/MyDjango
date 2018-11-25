from django_hosts import patterns, host #导入django-host
from django.conf import settings        #导入settings

from article import views as article
from monitor import views as monitor
from www import views as www        


host_patterns = patterns('',
    host(r'cv', 'www.urls', name='cv'),
    host(r'blog', 'www.urls', name='blog'),
    host(r'r', 'www.urls', name='r'),
    host(r'www', 'article.urls', name='www'),
    host(r'monitor', 'monitor.urls', name='monitor'),   
)