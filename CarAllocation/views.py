from django.shortcuts import render

# Create your views here.
def carAllocationClick_view(request):
    templates_name = "car/wedding_car_allocation.html"
    context = {
        'title':'迎娶禮車分配 Wedding car allocation'
    }
    return render(request, templates_name, context)
