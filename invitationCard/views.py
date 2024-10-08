from django.http import HttpResponse
from django.shortcuts import render
from .models import Invite 

from invitationCard.models import *
# from django.contrib.auth.decorators import login_required

# Create your views here.
def inviteclick_view(request):
    templates_name = "invite/invite.html"
    context = {
        'title':'我是標題'
    }
    return render(request, templates_name, context)

def questionclick_view(request):
    templates_name = 'invite/questionclick.html'
    if request.method == 'POST':
        print(request.method)
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        know = request.POST.get('know')
        diet = request.POST.get('diet')
        
        # 獲取名稱數據
        fill_multi_names = request.POST.getlist('fill_multi_names')
        diet_choice_non_vegetarian = request.POST.get('diet_choice_non_vegetarian')
        diet_choice_vegetarian = request.POST.get('diet_choice_vegetarian')
        baby_seat = request.POST.get('baby_seat')
        kids_count = request.POST.get('kids_count')

        # 專車接送
        Pick_up_location = request.POST.get('Pick_up_location')
        Add_location = request.POST.get('Add_location')
        Passengers_name = request.POST.get('Passengers_name')
        Passengers_phone_num = request.POST.get('Passengers_phone_num')

        # 檢查必填欄位是否為空
        if not name or not phone or not address or not email or not know or not diet:
            return HttpResponse(
                '請填寫所有必填欄位！ 點擊<a style="text-decoration: none" href="{% url ''invite:invite %}"><b style="font-size:20px">_返回</b></a>連到 邀請函填寫<br>')

        # 檢查電話號碼是否已經存在
        if Invite.objects.filter(phone=phone).exists():
            return HttpResponse('邀請函創建成功，電話號碼已儲存。 點擊<a style="text-decoration: none" href="/"><b style="font-size:20px">返回</b></a>連到 首頁<br>')

        # 將每個名稱存入模型
        for fill_multi_name in fill_multi_names:
            invite = Invite(name=name, phone=phone, address=address, email=email, 
                            know=know, diet=diet, Pick_up_location=Pick_up_location, 
                            Add_location=Add_location, Passengers_name=Passengers_name, 
                            Passengers_phone_num=Passengers_phone_num,
                            fill_multi_names=fill_multi_name,diet_choice_non_vegetarian=diet_choice_non_vegetarian,
                            diet_choice_vegetarian=diet_choice_vegetarian,
                            baby_seat=baby_seat,kids_count=kids_count,
                        )
            invite.save()

        # 迭代完成後返回成功的 HttpResponse
        return HttpResponse('邀請函創建成功!!! 請點擊<a style="text-decoration: none" href="/"><b style="font-size:20px">返回</b></a>連到 首頁<br>')
    else:
        context = {
            'title': '邀請函 建立',
        }
        # 如果是 GET 請求，回傳 render 函式 ; # 如果是GET請求，返回表單
        return render(request, templates_name, context)


def survey_thankyou(request):
    return render(request, 'questionnaire/thankyou.html')


def givemoney_view(request):
    templates_name = 'invite/givemoneyclick.html'
    if request.method == 'POST':
        nameGive = request.POST.get('nameGive')
        phoneGive = request.POST.get('phoneGive')
        addressGive = request.POST.get('addressGive')
        emailGive = request.POST.get('emailGive')

        if GiveMoney.objects.filter(phoneGive=phoneGive).exists():
            return HttpResponse(
                '邀請函創建成功，電話號碼已儲存。 點擊<a style="text-decoration: none" href="/"><b style="font-size:20px">返回</b></a>連到 首頁<br>')

        givemoney = GiveMoney(nameGive=nameGive, phoneGive=phoneGive, addressGive=addressGive, emailGive=emailGive)
        givemoney.save()
        return HttpResponse(
            '邀請函創建成功!!! 請點擊<a style="text-decoration: none" href="/"><b style="font-size:20px">返回</b></a>連到 首頁<br>')
    else:
        context = {
            'title': '給錢 建立',
        }
        return render(request, templates_name, context)


def notattend_view(request):
    templates_name = 'invite/notattendclick.html'
    if request.method == 'POST':
        nameNo = request.POST.get('nameNo')
        emailNo = request.POST.get('emailNo')
        msgNo = request.POST.get('msgNo')

        notattend = NotAttend(nameNo=nameNo, emailNo=emailNo, msgNo=msgNo, )
        notattend.save()
        return HttpResponse(
            '邀請函創建成功!!! 請點擊<a style="text-decoration: none" href="/"><b style="font-size:20px">返回</b></a>連到 首頁<br>')
    else:
        context = {
            'title': '留言板 建立',
        }
        return render(request, templates_name, context)
