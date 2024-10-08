from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from PersonnelAddressBook.models import Employee, GroupEmail

# send mail
from django.core.mail import send_mail
from django.conf import settings
from PersonnelAddressBook.forms import SendEmailForm
from PersonnelAddressBook.models import SendEmail

# 接收信件
from PersonnelAddressBook.models import Email
# 步驟 1：創建自動抓取郵件的函數
# 在 views.py 中，創建一個函數來抓取郵件。
import logging

from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

# Create your views here.
def PersonnelView(request):
    template_name = "personneladdbook/mailsummary.html"
    personal_address_book = Employee.objects.exclude(group_emails__isnull=False).order_by('-id')
    group_emails = GroupEmail.objects.all().select_related('employee')
    # all_emails = Email.objects.all().order_by('-received_at')
    total_group_emails = group_emails.count()
    send_email_form = SendEmailForm()

    if request.method == 'POST':
        action = request.POST.get('action')
        employee_id = request.POST.get('employee_id')

        if employee_id:
            employee = get_object_or_404(Employee, id=employee_id)

            if action == 'add':
                GroupEmail.objects.get_or_create(employee=employee, defaults={'action': '加入'})
            elif action == 'remove':
                GroupEmail.objects.filter(employee=employee).delete()
        elif action == 'send_email':
            send_email_form = SendEmailForm(request.POST)
            if send_email_form.is_valid():
                subject = send_email_form.cleaned_data['subject']
                message = send_email_form.cleaned_data['message']
                from_email = settings.EMAIL_HOST_USER
                to_email = send_email_form.cleaned_data['to_email']

                try:
                    send_mail(subject, message, from_email, [to_email], fail_silently=False)
                    SendEmail.objects.create(
                        subject=subject,
                        message=message,
                        from_email=from_email,
                        to_email=to_email
                    )
                    return render(request, 'personneladdbook/success.html')
                except Exception as e:
                    return render(request, 'personneladdbook/error.html', {'error': str(e)})

    context = {
        'personal_address_book': personal_address_book,
        'group_emails': group_emails,
        'total_group_emails':total_group_emails,
        'send_email_form': send_email_form,
        'title': '通訊錄'
    }
    return render(request, template_name, context)

def update_group_email(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        employee_id = request.POST.get('employee_id')

        if employee_id:
            employee = get_object_or_404(Employee, id=employee_id)

            if action == 'add':
                group_email, created = GroupEmail.objects.get_or_create(employee=employee, defaults={'action': '加入'})
                if created:
                    return JsonResponse({'status': 'added'})
            elif action == 'remove':
                GroupEmail.objects.filter(employee=employee).delete()
                return JsonResponse({'status': 'removed'})

    return JsonResponse({'status': 'error'})

# 抓取mail data 進入數據，但是需要使用python manage.py fetch_emails

# def email_list(request):
#     received_emails = Email.objects.all().order_by('-received_at')
#     return render(request, 'personneladdbook/email_list.html', {'emails': received_emails})

from django.core.paginator import Paginator
def email_list(request):
    page_size = 25  # 每頁顯示25封郵件
    all_emails = Email.objects.all().order_by('-received_at')
    total_emails = all_emails.count()
    paginator = Paginator(all_emails, page_size)  # 每頁顯示25封郵件
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    # 只查詢未讀郵件
    # unread_emails = Email.objects.filter(is_read=False).count()

    logger.info(f"Total emails in database: {paginator.count}")#{total_emails}

    for email in all_emails[:10]:
        logger.debug(f"Email: {email.id}, {email.subject}, {email.from_email}, {email.to_email}, {email.received_at}")
    context ={
        'emails': all_emails, 
        'total_emails': total_emails,
        'page_obj': page_obj,
        # 'total_emails': Email.objects.count(),
    }
    return render(request, 'personneladdbook/email_list.html', context)

def update_emails(request):
    try:
        fetch_emails_task.delay()
        return JsonResponse({'status': 'success', 'message': 'Emails update started'})
    except Exception as e:
        logger.error(f"Error updating emails: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
# 自動更新信件
from .tasks import fetch_emails_task
fetch_emails_task()

def check_new_emails(request):
    last_email_id = request.GET.get('last_id', 0)
    max_new_emails = getattr(settings, 'MAX_NEW_EMAILS', 10)
    new_emails = Email.objects.filter(id__gt=last_email_id).order_by('-received_at')[:max_new_emails]
    # new_emails = Email.objects.filter(id__gt=last_email_id).order_by('-received_at')

    new_emails_data = [{
        'id': email.id,
        'received_at': email.received_at.strftime('%Y-%m-%d %H:%M:%S'),
        'subject': email.subject,
        'from_email': email.from_email,
        'to_email': email.to_email,
        'is_sent': email.is_sent
    } for email in new_emails]
    return JsonResponse({'new_emails': new_emails_data})

# 表格中實現已讀/未讀功能在 views.py 中添加一個新的視圖函數來處理標記為已讀的 AJAX 請求：
@require_POST
def mark_as_read(request):
    email_id = request.POST.get('email_id')
    try:
        email = Email.objects.get(id=email_id)
        email.is_read = True
        email.save()
        return JsonResponse({'success': True})
    except Email.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

# 表格中實現已讀/未讀功能在 views.py 中添加一個新的視圖函數來處理標記為已讀的 AJAX 請求：
@require_POST
def mark_as_read(request):
    email_id = request.POST.get('email_id')
    try:
        email = Email.objects.get(id=email_id)
        email.is_read = True
        email.save()
        return JsonResponse({'success': True})
    except Email.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

def get_notification_info(request):
    unread_email_count = Email.objects.filter(is_read=False).count()
    total_group_emails = GroupEmail.objects.count()

    # 計算總通知數量
    total_notifications = unread_email_count + total_group_emails
    # 獲取最新的未讀郵件
    latest_email = Email.objects.filter(is_read=False).order_by('-received_at').first()
    # 獲取最新的 GroupEmail
    # latest_group_email = GroupEmail.objects.filter(is_read=False).order_by('-added_at').first()
    latest_group_email = GroupEmail.objects.order_by('-added_at').first()

    # 準備返回的數據
    data = {
        'unread_email_count': unread_email_count,
        'total_notifications': total_notifications,
        'total_group_emails': total_group_emails,
        'latest_email': {
            'subject': latest_email.subject if latest_email else None,
            'received_at': latest_email.received_at.isoformat() if latest_email else None,
        },
        'latest_group_email': {
            'added_at': latest_group_email.added_at.isoformat() if latest_group_email else None,
        },
    }
    return JsonResponse(data)

# def get_notification_info(request):
#     unread_email_count = Email.objects.filter(is_read=False).count()
#     total_group_emails = GroupEmail.objects.count()

#     # 計算總通知數量
#     total_notifications = unread_email_count + total_group_emails

#     latest_email = Email.objects.filter(is_read=False).order_by('-received_at').first()

#     # 準備返回的數據
#     data = {
#         'unread_email_count': unread_email_count,
#         'total_notifications': total_notifications,
#         'total_group_emails': total_group_emails,
#         'latest_email': latest_email,
#         'latest_email': {
#             'subject': latest_email.subject if latest_email else None,
#             'received_at': latest_email.received_at.isoformat() if latest_email else None,
#         },
#     }
#     return JsonResponse(data)

# 未讀郵件數量視圖函數: 要實現即時同步接收Gmail未讀新郵件數量，並顯示最新郵件的接收時間。以下是一些建議的實現方法:即時同步接收到Gmail的未讀新郵件數量:

# 刪除信件
def delete_email(request, email_id):
    email = get_object_or_404(Email, id=email_id)
    email.delete()
    return redirect('personnelAddBook:email_list')  # 替換為顯示郵件列表的視圖名稱