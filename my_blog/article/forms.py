#coduploading=utf-8
from django import forms

class add_forms(forms.Form):
	pass

class add_comment(forms.Form):
	comment_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入评论','rows':u'4'}))

class outside_img(forms.Form):
	img_url = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此提交图片外链'}))

class release_forms(forms.Form):
	title = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入文章标题'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入文章内容'}))
