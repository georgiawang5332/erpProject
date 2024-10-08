from django import forms
from .models import SendEmail

# Create your forms here.
# class SendEmailForm(forms.ModelForm):
    # class Meta:
        # model = SendEmail
        # fields = "__all__"
        # fields = ['subject', 'message', 'to_email']

class SendEmailForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'custom-input input1'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'custom-input input2'}))
    to_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-input input3'}))

