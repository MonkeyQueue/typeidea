#这个文件是用来作后台管理的Form

from django import forms


class PostAdminForm(forms.ModelForm):
    desc=forms.CharField(widget=forms.Textarea,label='摘要',required=False)
    