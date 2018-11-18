#coding=utf-8
"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path
from monitor import views
from django.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from django.views import static 

app_name = 'monitor'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('post_animation_info/',views.post_animation_info,name = 'post_animation_info'),
    path('post_index/',views.post_index,name = 'post_index'),
    path('all/',views.all,name="all"),
    path('top/',views.top,name="top"),
    path('log/',views.log,name="log"),
    path('admin/',admin.site.urls),

    path('id_list_post/',views.id_list_post,name="id_list_post"),
    path('mcard_list_post/',views.mcard_list_post,name="mcard_list_post"),
    path('top_list_post/',views.top_list_post,name="top_list_post"),
    path('info_post/',views.info_post,name="info_post"),

    url(r'^favicon\.ico$', static.serve,{'document_root': settings.STATIC_ROOT,'path': "/img/favicon.ico"}),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'), 
    
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)