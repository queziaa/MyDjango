#coduploading=utf-8
from django import forms

class add_forms(forms.Form):
	pass

class add_comment(forms.Form):
	comment_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'Type a comment her','rows':u'4'}))

class outside_img(forms.Form):
	img_url = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'Submit the picture outer link here.'}))
