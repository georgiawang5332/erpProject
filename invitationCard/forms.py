from django import forms
from django.contrib.auth.models import User

from . import models


# Create your forms here.
class InvitationUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            # 'password': forms.PasswordInput(attrs={'required': False}),
            'password': forms.PasswordInput(attrs={'placeholder': '密碼輸入'}),
        }


class InvitationForm(forms.ModelForm):
    class Meta:
        model = models.Invitation
        fields = ['name', 'phone', 'address', 'email', 'know', 'diet', 'baby_seat', ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入姓名'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入電話'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入地址'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '輸入信箱'}),
            # 在這裡為其他字段添加相應的小工具
        }



class GiveMoneyForm(forms.ModelForm):
    class Meta:
        model = models.GiveMoney
        fields = ['autonoGive', 'nameGive', 'phoneGive', 'addressGive', 'emailGive', 'status']

        widgets = {
            'nameGive': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入姓名'}),
            'phoneGive': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入電話'}),
            'addressGive': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入地址'}),
            'emailGive': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '輸入信箱'}),
            # 在這裡為其他字段添加相應的小工具
        }


class NotAttendForm(forms.ModelForm):
    class Meta:
        model = models.NotAttend
        fields = ['autonoNo', 'nameNo', 'emailNo', 'msgNo', 'status']

        widgets = {
            'nameNo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入姓名'}),
            'emailNo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '輸入信箱'}),
            'msgNo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '輸入地址'}),
            # 在這裡為其他字段添加相應的小工具
        }
