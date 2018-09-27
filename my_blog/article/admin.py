from django.contrib import admin
from article.models import Article,Comment_db,IMG,Article_examine,User_data,Search_db

class Article_admin(admin.ModelAdmin):
	list_display = ('date_time','examine_time')
admin.site.register(Article,Article_admin)

class Comment_db_admin(admin.ModelAdmin):
	list_display = ('date_time',)
admin.site.register(Comment_db,Comment_db_admin)

admin.site.register(IMG)

class Article_examine_admin(admin.ModelAdmin):
	list_display = ('examine_time',)
admin.site.register(Article_examine,Article_examine_admin)

admin.site.register(User_data)

class Search_db_admin(admin.ModelAdmin):
	list_display = ('examine_time',)
admin.site.register(Search_db,Search_db_admin)