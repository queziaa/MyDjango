#coding=utf-8
from django.db import models

# Create your models here.
class Article(models.Model) :
    title = models.CharField(max_length = 110,null = True)  #博客题目
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    examine_time = models.DateTimeField(auto_now_add = True)  #
    content = models.TextField(blank = True, null = True)  #博客文章正文
    comments_quantity = models.IntegerField(default=0)  
    comment_ip = models.TextField(default='!')
    user = models.CharField(max_length = 11)
    label = models.CharField(max_length = 110,default = '!')


    #python2使用__unicode__, python3使用__str__
    def __str__(self) :
        return self.title

    class Meta:  #按时间下降排序
        ordering = ['-date_time']

class Comment_db(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    comments_text = models.TextField(max_length = 450,null = True)
    ip_hash = models.CharField(max_length = 13) 

    def __str__(self) :
        return self.comments_text


class IMG(models.Model):
    url = models.CharField(max_length=200,null = True)
    img_type = models.BooleanField(default= True)

    def __str__(self) :
        return self.url
        
    class Meta:  
        ordering = ['-id']

class Article_examine(models.Model):
    title = models.CharField(max_length = 110,null = True) 
    examine_time = models.DateTimeField(auto_now_add = True)
    content = models.TextField(blank = True, null = True) 
    visible = models.BooleanField(default= True)
    user = models.CharField(max_length = 11,null = True)
    label = models.CharField(max_length = 110,default = '!')

    def __str__(self) :
        return self.title

    class Meta:
        ordering = ['-examine_time']


class User_data(models.Model):
    name = models.CharField(max_length = 11,null = True)
    password = models.CharField(max_length = 64,null = True)
    cookie_name = models.CharField(max_length = 64,default = '!')
    cookie_password = models.CharField(max_length = 64,default = '!')
    cookie_time =  models.DateTimeField(auto_now_add = True)
    admin = models.BooleanField(default = False)

    def __str__(self) :
        return self.name
