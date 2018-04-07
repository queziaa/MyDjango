from django import forms

class add_forms(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()

class add_comment(forms.Form):
	comment_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':u'Type a comment her','rows':u'4'}))