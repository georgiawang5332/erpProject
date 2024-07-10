from django.shortcuts import render

# Create your views here.
def dayItemListClick_view(request):
    templates_name = "dayItem/wedding_day_item_list.html"
    context = {
        'title':'婚宴當天物品清單 Wedding day item list'
    }
    return render(request, templates_name, context)

