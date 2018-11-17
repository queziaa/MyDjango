from django_hosts import patterns, host #导入django-host
from django.conf import settings        #导入settings

from article import views as article  #导入app1,我的app1叫ss_update
from monitor import views as monitor  #导入app2,我的app2叫translate
from www import views as www          #导入app2,我的app2叫translate


host_patterns = patterns('',
    host(r'cv', 'www.urls', name='www'),
    host(r'www', 'article.urls', name='article'),
    host(r'monitor', 'monitor.urls', name='monitor'),   
)