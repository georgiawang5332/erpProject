from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import SendEmailForm
from .models import SendEmail


# Create your views here.
def sendEmail(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # from_email = form.cleaned_data['from_email']
            from_email = settings.EMAIL_HOST_USER  # 使用 settings 中的 EMAIL_HOST_USER
            to_email = form.cleaned_data['to_email']
            
            # 創建並保存 SendEmail 實例
            email = SendEmail.objects.create(
                subject=subject,
                message=message,
                from_email=from_email,
                to_email=to_email
            )
            
            # 實際發送郵件的邏輯
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [to_email],  # 要作為列表傳遞
                    fail_silently=False,
                )
                # 如果郵件發送成功，可以更新模型實例的狀態
                email.status = 'sent'  # 假設您在模型中有一個 status 字段
                email.save()
                return render(request, 'sendemail/success.html')
            except Exception as e:
                # 處理郵件發送失敗的情況
                email.status = 'failed'
                email.save()
                # 可以在這裡添加錯誤處理邏輯，比如顯示錯誤消息
                return render(request, 'sendemail/error.html', {'error': str(e)})
    else:
        form = SendEmailForm()
    
    return render(request, 'sendemail/sendemail.html', {'form': form})

