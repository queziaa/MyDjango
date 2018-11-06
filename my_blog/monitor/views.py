from django.shortcuts import render
from django.http import HttpResponse
from monitor.models import start_time
from my_blog.settings import CELERY_ERROR_LOG 

import os

def home(request):
    fg = open(CELERY_ERROR_LOG,'r')
    return render(request,'monitor_home.html',{'log': str(fg.read())})
