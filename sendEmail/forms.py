from django import forms
from .models import SendEmail

# Create your forms here.
class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = ['subject', 'message', 'to_email']