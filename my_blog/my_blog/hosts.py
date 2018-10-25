from django_hosts import patterns, host #导入django-host
from django.conf import settings        #导入settings

from article import views as article  #导入app1,我的app1叫ss_update
from monitor import views as monitor  #导入app2,我的app2叫translate
from www import views as www          #导入app2,我的app2叫translate


host_patterns = patterns('',
    host(r'www', 'www.urls', name='www'),          #子域名，类似weather.test.com中的weather
    host(r'blog', 'article.urls', name='article'), #子域名，类似translate.test.com 中的translate
    host(r'monitor', 'monitor.urls', name='monitor'),
    
)