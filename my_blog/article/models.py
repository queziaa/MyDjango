#coding=utf-8
from django.db import models

# Create your models here.
class Article(models.Model) :
    title = models.CharField(max_length = 100)  #博客题目
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    examine_time = models.DateTimeField(auto_now_add = True)  #
    content = models.TextField(blank = True, null = True)  #博客文章正文
    comments_quantity = models.IntegerField(default=0)  
    comment_ip = models.TextField(default='!')

    #python2使用__unicode__, python3使用__str__
    def __str__(self) :
        return self.title

    class Meta:  #按时间下降排序
        ordering = ['-date_time']

class Comment_db(models.Model):
    date_time = models.DateTimeField(auto_now_add = True)
    comments_text = models.TextField(max_length = 100)
    ip_hash = models.CharField(max_length = 13) 

    def __str__(self) :
        return self.comments_text


class IMG(models.Model):
    url = models.CharField(max_length=200)
    img_type = models.BooleanField(default= True)

    class Meta:  
        ordering = ['-id']

class Article_examine(models.Model):
    title = models.CharField(max_length = 100) 
    examine_time = models.DateTimeField(auto_now_add = True)
    content = models.TextField(blank = True, null = True) 
    visible = models.BooleanField(default= True)


    def __str__(self) :
        return self.title

    class Meta:
        ordering = ['-examine_time']