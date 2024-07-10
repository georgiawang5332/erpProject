from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from BudgetSheet.models import Category, BudgetSheetModel, Currency# 確保你已經導入 Category 模型
from django.shortcuts import get_object_or_404
# from django.views.generic import (
#     DetailView,
# )
# Create your views here.
# add
from decimal import Decimal

def createBudget(request):
    template_name = 'budget/createBudget.html'

    if request.method == 'GET':
        create_budget_sheet = BudgetSheetModel.objects.all()
        categories = Category.objects.all()
        currencies = Currency.objects.all()

        context = {
            'create_budget_sheets': create_budget_sheet,
            'categories': categories,
            'currencies': currencies,
            'title': 'test ABC'
        }
        return render(request, template_name, context)

    if request.method == "POST":
        category_id = request.POST.get('category')
        currency_id = request.POST.get('currency')

        # 獲取 Category 和 Currency 實例
        category = get_object_or_404(Category, id=category_id)
        currency = get_object_or_404(Currency, id=currency_id)

        # 獲取其他表單數據
        expenditure_items = request.POST.get('expenditure_items', '')
        estimated_quantity = Decimal(request.POST.get('estimated_quantity', '0'))
        estimated_unit_price = Decimal(request.POST.get('estimated_unit_price', '0'))
        remark_one = request.POST.get('remark_one', '')
        actual_quantity = Decimal(request.POST.get('actual_quantity', '0'))
        actual_unit_price = Decimal(request.POST.get('actual_unit_price', '0'))
        payer = request.POST.get('payer', '')
        remark_two = request.POST.get('remark_two', '')

        # 創建新的 BudgetSheetModel 實例
        obj = BudgetSheetModel.objects.create(
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
        # estimated_expenses 和 paid 會自動計算

    return redirect('budget:budget_sheet_click')

# edit
def updateBudget(request, id):
    template_name = 'budget/updateBudget.html'
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
    template_name = 'budget/detailBudget.html'
    detail_budget_sheet = BudgetSheetModel.objects.get(id=id)
    context = {
        'detail_budget_sheets': detail_budget_sheet,
        'title': '詳閱 婚禮預算表'
    }
    return render(request, template_name, context)

# list
def budgetSheetClick_view(request):
    
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


from django.http import JsonResponse

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