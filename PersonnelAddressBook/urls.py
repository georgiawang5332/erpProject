from django.urls import path
from . import views

app_name = "personnelAddBook"

# Create your urls here.
urlpatterns = [
    path("personalAddBook/", views.PersonnelView, name="personnel_address_book"), 
    path('update-group-email/', views.update_group_email, name='update_group_email'),
    # path('sendEmail/', views.sendEmail, name='sendEmail')
    path('emails/', views.email_list, name='email_list'),
    path('check_new_emails/', views.check_new_emails, name='check_new_emails'), #刷新Gmail=georgiawang5332頁面
    # 已讀/未讀功能
    path('mark_as_read/', views.mark_as_read, name='mark_as_read'),

    # 未讀郵件數量視圖函數的url
    path('get-notification-info/', views.get_notification_info, name='get_notification_info'),
    # 刪除信件
    path('delete-email/<int:email_id>/', views.delete_email, name='delete_email'),
     
]
