#coduploading=utf-8
from django import forms

class add_forms(forms.Form):
	pass

class add_comment(forms.Form):
	comment_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入评论\n'
		'如果是以$开头的评论，说明用户登陆了此账户发布的评论\n如果是以#开头的评论，说明用户未登陆账户,此ID是由ip地址生成的，且此过程不可逆.'
		,'rows':u'4'}))

class outside_img(forms.Form):
	img_url = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此提交图片外链'}))

class release_forms(forms.Form):
	title = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入文章标题'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'在此输入文章内容'}))

class login_forms(forms.Form):
	name = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'用户名'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'密码'}))

class registered_foms(forms.Form):
	name = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'用户名'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'密码'}))
	repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'再次输入密码'}))

class cehange_password_foms(forms.Form):
	oid = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'老密码'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'新密码'}))
	repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':u'再次输入密码'}))