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
from article import views
from django.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from django.views import static 

app_name = 'article'
urlpatterns = [
    path('admin/',admin.site.urls),
    path('', views.home, name = 'home'),
    path('me/',views.me,name='me'),
    path('detailed/<int:id>/',views.detailed,name='detailed'),
    path('archive/',views.archive,name='archive'),
    path('upload/', views.upload,name='upload'),
    path('examine/', views.examine,name='examine'),
    path('get_examine/', views.get_examine,name='get_examine'),
    path('Error/',views.Error,name='Error'),
    path('404/',views.e404,name='e404'),
    path('release/', views.release,name='release'),
    path('user/',views.user,name='user'),
    path('exit/',views.exit,name='exit'),
    path('cehange_password/',views.cehange_password,name='cehange_password'),

    path('get_name/',views.get_name,name='get_name'),
    path('Dynamic_window_registered/',views.registered,name='Dynamic_window_registered'),
    path('Dynamic_window_login/', views.login,name='Dynamic_window_login'),


    url(r'^favicon\.ico$', static.serve,{'document_root': settings.STATIC_ROOT,'path': "/img/favicon.ico"}),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'), 


]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




