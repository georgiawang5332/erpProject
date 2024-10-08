from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # 或者你的自定義 User 模型
from accounts.models.user import *
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model


# Create your views here.

# list
def ListEmpInfo(request):
    templates_name = "accounts/employee_info.html"
    users = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users, 10)  # 每頁顯示10個用戶
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': '員工個人資料 Employee Profile',
        'page_obj': page_obj,
    }
    return render(request, templates_name, context)

# create/add 新增
User = get_user_model()

def CreateEmpInfo(request):
    template_name = 'accounts/create_emp_info.html'

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        avatar = request.FILES.get('avatar')

        if not all([email, username, password]):
            messages.error(request, "請填寫所有必要的欄位")
            return render(request, template_name)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "此信箱已被使用")
            return render(request, template_name)

        try:
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            if avatar:
                user.avatar = avatar
                user.save()

            messages.success(request, f'<div class="alert alert-primary" style="font-size:20px;" role="alert"><strong>成功新增用戶:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> {username}</div>')

            return redirect('account:list_emp_info_click')
        except Exception as e:
            messages.error(request, f"創建用戶時出錯：{str(e)}")
            return render(request, template_name)

    return render(request, template_name)

# detail
def DetailEmpInfo(request, id):
    template_name = 'accounts/detail_emp_info.html'
    detail_emp_info = get_object_or_404(User, id=id)
    context = {
        'detail_emp_info': detail_emp_info,
        'title': '員工個人資料 Detail Employee Profile'
    }
    return render(request, template_name, context)

# update/edit
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

def UpdateEmpInfo(request, id):
    template_name = 'accounts/update_emp_info.html'
    update_emp_info = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        # 處理表單提交
        update_emp_info.email = request.POST.get('email')
        update_emp_info.username = request.POST.get('username')
        update_emp_info.first_name = request.POST.get('first_name')
        update_emp_info.last_name = request.POST.get('last_name')
        update_emp_info.avatar = request.POST.get('avatar')
        
        # 確保有新頭像上傳，並保存上傳的文件
        if 'avatar' in request.FILES:
            update_emp_info.avatar = request.FILES['avatar']
            
        # 處理日期
        date_joined_str = request.POST.get('date_joined')
        try:
            # 嘗試將輸入的日期字符串轉換為 datetime 對象
            date_joined = datetime.strptime(date_joined_str, '%Y年%m月%d日 %H:%M')
            update_emp_info.date_joined = date_joined
        except ValueError:
            # 如果轉換失敗，可以選擇跳過更新這個字段或者返回錯誤信息
            pass  # 或者在這裡添加錯誤處理邏輯

        update_emp_info.save()
        return redirect('account:list_emp_info_click')

    context = {
        'update_emp_info': update_emp_info,
        'title': '員工個人資料 Update Employee Profile'
    }
    return render(request, template_name, context)

# del
def DelEmpInfo(request, id):
    del_emp_info = User.objects.get(pk=id)
    del_emp_info.delete()
    messages.success(request, 'record removed/記錄已刪除')
    return redirect('account:list_emp_info_click')