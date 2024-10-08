from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, label="姓名")
    Email = forms.EmailField(label="信箱")
    Message = forms.CharField(max_length=500, label="留言", widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

