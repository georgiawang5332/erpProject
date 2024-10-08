from django.shortcuts import render

# Create your views here.
def banquetStaffListClick_view(request):
    templates_name = "banquetStaff/banquet_staff_list.html"
    context = {
        'title':'婚禮預算表 wedding budget sheet'
    }
    return render(request, templates_name, context)

