from django.contrib import admin

from article.models import Article,Comment_db,IMG,Article_examine

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment_db)
admin.site.register(IMG)
admin.site.register(Article_examine)