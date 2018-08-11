#coduploading=utf-8
from django import forms


class add_comment(forms.Form):
	comment_content = forms.CharField(
		widget=forms.Textarea(
			attrs={'placeholder':u'在此输入评论\n以$开头的评论为登陆账户评论.以#开头的评论为匿名评论,匿名ID是由ip地址生成过程不可逆.\n查看图片超链接输入格式,点击格式帮助按钮',
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
