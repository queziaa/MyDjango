#coding=utf-8
"""
Django settings for my_blog project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import djcelery
from celery.schedules import crontab
from datetime import datetime,timedelta  
djcelery.setup_loader()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r-&180r7ih4(cm+49ky&@8l(uyx4*6-o7t0!t8$eagsgc9)f^h'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
ALLOWED_HOSTS = ['www.queziaa.fun','cv.queziaa.fun','monitor.queziaa.fun']
# ALLOWED_HOSTS = ['www.localhost.com','cv.localhost.com','monitor.localhost.com']
# DEBUG = True


CELERY_ERROR_LOG = r'/var/www/MyDjango/my_blog/static/img/monitor.log'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_hosts',
    'djcelery',
    'article',
    'monitor',
    'www',
    'django_mongoengine',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'my_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'DIRS': [TEMPLATE_PATH],
    },
]

WSGI_APPLICATION = 'my_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': 'a20owksertcy37weujd',
        'OPTIONS': {    
            'sql_mode': 'traditional',
            },
    }
}
MONGODB_DATABASES = {
    "default": {
        "name": 'monitor',
        "host": "127.0.0.1",
        "password": '',
        "username": '',
        "tz_aware": False, # if you using timezones in django (USE_TZ = True)
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

ROOT_HOSTCONF = 'my_blog.hosts'
DEFAULT_HOST = 'www'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')    
 #设置静态文件路径为主目录下的media文件夹
MEDIA_URL = '/media/' 

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai' 
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  
# 这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULE={
        # "sqlclear-1-day": {
        #     'task': 'article.tasks.SearchArrangementThread',
        #     'schedule': timedelta(days=1)
        #     # 'args':
        # },
        "bilibili_spider_time-1-hour": {
            'task': 'monitor.tasks.spider_time',
            'schedule': timedelta(minutes=1)
        },
        "bilibili_spider_data-3-minute":{
            'task': 'monitor.tasks.spider_data',
            'schedule': timedelta(minutes=1)
        }
}