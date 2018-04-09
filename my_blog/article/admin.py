from django.contrib import admin
from article.models import Article
from article.models import Comment_db
from article.models import IMG
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment_db)
admin.site.register(IMG)