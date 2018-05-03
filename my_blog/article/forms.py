#coduploading=utf-8
from django import forms


class add_comment(forms.Form):
	comment_content = forms.CharField(
		widget=forms.Textarea(
			attrs={'placeholder':u'在此输入评论\n以$开头的评论，登陆了账户发布的评论.以#开头的评论，匿名的评论,此时ID是由ip地址生成的，且过程不可逆.\n如需插入图片,请事先提交图片获取图片id,在插入图片位置书写“{@图片id@}“',
			'rows':u'4'}
		),
		min_length=1,
		max_length=450,
		required=True,
        strip=True,
        error_messages={'required': '评论不能为空',
                        'min_length': '评论最少为1个字符',
                        'max_length': '评论最不超过为450个字符'},
    )

class outside_img(forms.Form):
	img_url = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'在此提交图片外链','rows':u'2'}),
		max_length=150,
		required=True,
        strip=True,
        error_messages={'required': '不能为空',
                        'max_length': '不超过为150个字符'},
	)

class release_forms(forms.Form):
	title = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'在此输入文章标题','rows':u'2'}),
		min_length=1,
		max_length=110,
		required=True,
        strip=True,
        error_messages={'required': '标题不能为空',
                        'min_length': '标题最少为1个字符',
                        'max_length': '标题最不超过为110个字符'},

	)
	content = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'在此输入文章内容','rows':u'6'}),
		min_length=1,
		required=True,
        strip=True,
        error_messages={'required': '内容不能为空',
                        'min_length': '内容最少为1个字符'},
	)
	label = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'在此输入文章标签,不同标签以#分割','rows':u'1'}),
		required=False,
        strip=True,
		max_length=110,
        error_messages={
                        'max_length': '标签最不超过为110个字符'},
	)

class login_forms(forms.Form):
	name = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'用户名'}),
		min_length=5,
		max_length=11,
		required=True,
        strip=True,
        error_messages={'required': '用户名不能为空',
                        'min_length': '用户名最少为5个字符',
                        'max_length': '用户名最不超过为11个字符'},
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)
class registered_foms(forms.Form):
	name = forms.CharField(
		widget=forms.Textarea(attrs={'placeholder':u'用户名'}),
		min_length=5,
		max_length=11,
		required=True,
        strip=True,
        error_messages={'required': '用户名不能为空',
                        'min_length': '用户名最少为5个字符',
                        'max_length': '用户名最不超过为11个字符'},
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)
	repeat_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'再次输入密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)

class cehange_password_foms(forms.Form):
	oid = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'老密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'新密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)
	repeat_password = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder':u'再次输入密码'}),
		min_length=5,
		max_length=60,
		required=True,
        strip=True,
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为5个字符',
                        'max_length': '密码最不超过为60个字符'},
	)


