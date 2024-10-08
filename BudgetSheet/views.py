from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from BudgetSheet.models import *
from decimal import Decimal, InvalidOperation
from django.core.paginator import Paginator


# Create your views here.

# add
def CreateCategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'<div class="alert alert-primary" style="font-size:20px;" role="alert"><strong>成功新增用戶:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> {name}</div>')
            return redirect('budget:list_category')  # 假設您有一個列出所有類別的視圖
    
    context = {
        'title': '建立 類別',
    }
    return render(request, 'budget/create_category.html', context)
# forms.py
# def CreateCategory(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('budget:list_category')  # 假設您有一個列出所有類別的視圖
#     else:
#         form = CategoryForm()
    
#     context = {
#         'title': '新增類別',
#         'form': form,
#     }
#     return render(request, 'budget/createCategory.html', context)

# edit/update
def updateCategory(request, id):
    # 取得要更新的 Category 物件
    category = get_object_or_404(Category, id=id)

    # 檢查是否是 POST 請求 (提交了表單)
    if request.method == 'POST':
        # 從 POST 資料中獲取類別名稱
        new_name = request.POST.get('name')

        # 檢查名稱是否為空或重複
        if not new_name:
            return HttpResponse("類別名稱不能為空", status=400)

        if Category.objects.filter(name=new_name).exists() and new_name != category.name:
            return HttpResponse("類別名稱已存在", status=400)

        # 更新類別名稱
        category.name = new_name
        category.save()  # 保存更新

        # 更新後重定向到某個頁面 (例如類別列表)
        return redirect('budget:list_category')

    # 如果是 GET 請求，則顯示當前類別的編輯頁面
    context = {
        'update_category': category,
    }
    return render(request, 'budget/update_category.html', context)

# del
def delCategory(request, id):
    category = get_object_or_404(Category, id=id)  # 找到特定ID的類別
    if request.method == 'POST':  # 確認是POST請求才進行刪除
        category.delete()  # 刪除類別
        return redirect('budget:list_category')  # 刪除後重定向到貨幣列表;刪除後重定向到某個頁面

    return render(request, 'budget/del_category.html', {'del_category': category})  # 確認刪除的頁面

# detail
def detailCategory(request, id):
    category = get_object_or_404(Category, id=id)  # 找到特定ID的類別
    return render(request, 'budget/detail_category.html', {'detail_category': category})  # 顯示詳細資訊的頁面

# list
def ListCategoryClick(request):
    templates_name = "budget/wedding_budget_sheet_category.html"
    list_category = Category.objects.all()
    context = {
        'title': '類別',
        'list_category': list_category,
    }
    return render(request, templates_name, context)

# ///////////////////////////////////////////////////////////////////////
# add
def CreateCurrency(request):
    template_name = 'budget/create_currency.html'

    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        symbol = request.POST.get('symbol')

        if name and code:  # 確保至少有名稱和代碼
            Currency.objects.create(name=name, code=code, symbol=symbol)
            messages.success(request, f'<div class="alert alert-primary" style="font-size:20px;" role="alert"><strong>成功新增用戶:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> {name}</div>')
            return redirect(reverse('budget:list_currency'))  # 使用 reverse 函數獲取 URL
        else:
            context = {
                'error': '請提供貨幣名稱和代碼。',
                'title': '建立 貨幣',
            }
            return render(request, template_name, context)

    # 如果是 GET 請求，返回空的表單
    context = {
        'title': '建立 貨幣',
    }
    return render(request, template_name, context)

# edit/update
def updateCurrency(request, id):
    currency = get_object_or_404(Currency, id=id)  # 根據ID找到指定的貨幣
    if request.method == 'POST':  # 如果是表單提交（POST請求）
        name = request.POST.get('name')  # 獲取表單中提交的數據
        code = request.POST.get('code')
        symbol = request.POST.get('symbol')
        
        # 更新貨幣資料
        currency.name = name
        currency.code = code
        currency.symbol = symbol
        currency.save()  # 保存更新到資料庫
        
        return redirect('budget:detail_currency', id=currency.id)  # 更新成功後重定向到詳閱頁面
    return render(request, 'budget/update_currency.html', {'update_currency': currency})  # 渲染更新表單

# del
def delCurrency(request, id):
    currency = get_object_or_404(Currency, id=id)  # 根據ID找到貨幣
    if request.method == 'POST':  # 只有當是POST請求才進行刪除
        currency.delete()  # 刪除貨幣
        return redirect('budget:list_currency')  # 刪除後重定向到貨幣列表

    return render(request, 'budget/del_currency.html', {'del_currency': currency})  # 確認刪除頁面

# detail
def detailCurrency(request, id):
    currency = get_object_or_404(Currency, id=id)  # 根據ID找到指定貨幣
    return render(request, 'budget/detail_currency.html', {'detail_currency': currency})  # 渲染顯示詳情的頁面

# list
def ListCurrencyClick(request):
    templates_name = "budget/wedding_budget_sheet_currency.html"
    list_currency = Currency.objects.all()
    context = {
        'title': '貨幣',
        'list_currency': list_currency,
    }
    return render(request, templates_name, context)

# //////////////////////////////////////////////////////////////

# add
def createBudget(request):
    template_name = 'budget/create_budget.html'

    if request.method == 'GET':
        categories = Category.objects.all()
        currencies = Currency.objects.all()

        context = {
            'categories': categories,
            'currencies': currencies,
            'title': 'test ABC'
        }
        return render(request, template_name, context)

    if request.method == "POST":
        category_id = request.POST.get('category')
        currency_id = request.POST.get('currency')
        expenditure_items = request.POST.get('expenditure_items', '')
        remark_one = request.POST.get('remark_one', '')
        payer = request.POST.get('payer', '')
        remark_two = request.POST.get('remark_two', '')

        # 驗證必填字段 (加入所有必填欄位)
        if not all([category_id, currency_id, expenditure_items, remark_one, payer, remark_two]):
            return JsonResponse({'status': 'error', 'message': '請填寫所有必填字段。'})

        # 獲取 Category 和 Currency 實例
        category = get_object_or_404(Category, id=category_id)
        currency = get_object_or_404(Currency, id=currency_id)

        # 驗證數值字段
        try:
            estimated_quantity = Decimal(request.POST.get('estimated_quantity') or '0')
            estimated_unit_price = Decimal(request.POST.get('estimated_unit_price') or '0')
            actual_quantity = Decimal(request.POST.get('actual_quantity') or '0')
            actual_unit_price = Decimal(request.POST.get('actual_unit_price') or '0')
        except InvalidOperation:
            return JsonResponse({'status': 'error', 'message': '請確保所有數值字段都填寫正確。'})

        # 創建新的 BudgetSheetModel 實例
        BudgetSheetModel.objects.create(
            category=category,
            currency=currency,
            expenditure_items=expenditure_items,
            estimated_quantity=estimated_quantity,
            estimated_unit_price=estimated_unit_price,
            remark_one=remark_one,
            actual_quantity=actual_quantity,
            actual_unit_price=actual_unit_price,
            payer=payer,
            remark_two=remark_two,
        )
        
        messages.success(request, f'<div class="alert alert-primary" style="font-size:20px;" role="alert"><strong>成功新增用戶:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</strong> {expenditure_items}</div>')
        return JsonResponse({'status': 'success', 'message': '預算表單已成功創建。'})

    return render(request, template_name)

# edit/update
def updateBudget(request, id):
    template_name = 'budget/update_budget.html'
    edit_budget_sheet = get_object_or_404(BudgetSheetModel, id=id)

    if request.method == 'POST':
        # 處理表單提交
        # edit_budget_sheet.category = category
        category_name = request.POST.get('category')
        category = get_object_or_404(Category, name=category_name)
        edit_budget_sheet.expenditure_items = request.POST.get('expenditure_items')
        edit_budget_sheet.estimated_quantity = request.POST.get('estimated_quantity')
        edit_budget_sheet.estimated_unit_price = request.POST.get('estimated_unit_price')
        # edit_budget_sheet.currency = request.POST.get('currency')
        currency_name = request.POST.get('currency')
        currency = get_object_or_404(Currency, name=currency_name)  # 假設 Currency 模型有一個 name 欄位
        
        edit_budget_sheet.estimated_expenses = request.POST.get('estimated_expenses')
        edit_budget_sheet.remark_one = request.POST.get('remark_one')
        edit_budget_sheet.actual_quantity = request.POST.get('actual_quantity')
        edit_budget_sheet.actual_unit_price = request.POST.get('actual_unit_price')
        edit_budget_sheet.paid = request.POST.get('paid')
        edit_budget_sheet.payer = request.POST.get('payer')
        edit_budget_sheet.remark_two = request.POST.get('remark_two')
        
        edit_budget_sheet.save()
        return redirect('budget:budget_sheet_click')

    context = {
        'categories': Category.objects.all(),  # 添加這行
        'currencies': Currency.objects.all(),  # 添加這行
        'edit_budget_sheets': edit_budget_sheet,
        'title': 'EDIT ABC'
    }
    return render(request, template_name, context)

# delete
def delBudget(request, id):
    del_budget_sheet = BudgetSheetModel.objects.get(pk=id)
    del_budget_sheet.delete()
    messages.success(request, 'record removed')
    return redirect('budget:budget_sheet_click')

# detail
def detailBudget(request, id):
    template_name = 'budget/detail_budget.html'
    detail_budget_sheet = BudgetSheetModel.objects.get(id=id)
    context = {
        'detail_budget_sheets': detail_budget_sheet,
        'title': '詳閱 婚禮預算表'
    }
    return render(request, template_name, context)

# list
def ListBudgetSheetClick(request):
    templates_name = "budget/wedding_budget_sheet.html"
    latest_events = BudgetSheetModel.objects.order_by('-id')
    budget_sheets  = BudgetSheetModel.objects.order_by('-id')

    total_estimated_expenses = sum(sheet.estimated_quantity * sheet.estimated_unit_price for sheet in budget_sheets)
    total_actual_expenses    = sum(sheet.actual_quantity * sheet.actual_unit_price for sheet in budget_sheets)

    context = {
        'title': '婚禮預算表 wedding budget sheet',
        'latest_events': latest_events,
        'budget_sheets': budget_sheets,
        'categories': Category.objects.all(),
        "formatted_total_estimated_expenses": "${:,.2f}".format(total_estimated_expenses),
        "formatted_total_actual_expenses": "${:,.2f}".format(total_actual_expenses),
    }
    return render(request, templates_name, context)

# class PostDetailView(DetailView):
#     model = BudgetSheetModel

def get_budget_data(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(BudgetSheetModel.objects.all(), 50)
    page_obj = paginator.get_page(page)
    
    data = [
        {
            'id': item.id,
            'paid': float(item.paid),
            # ... 其他需要的字段 ...
        }
        for item in page_obj
    ]
    
    return JsonResponse({
        'data': data,
        'has_next': page_obj.has_next(),
        'total_pages': paginator.num_pages,
    })