from .models import Email, GroupEmail  # 假設您有 GroupEmail 模型

def email_count(request):
    return {'total_emails': Email.objects.count()}


def notification_counts(request):
    total_emails = Email.objects.filter(is_read=False).count()
    total_group_emails = GroupEmail.objects.filter(is_read=False).count() 
    total_notifications = total_emails + total_group_emails
    
    return {
        'total_emails': total_emails,
        'total_group_emails': total_group_emails,
        'total_notifications': total_notifications,
    }

# 如果 GroupEmail 也有 is_read 字段，也可以加上過濾條件
    # total_emails = Email.objects.count()
    # total_group_emails = GroupEmail.objects.count()