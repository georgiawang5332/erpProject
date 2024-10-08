from django.shortcuts import render

# Create your views here.
def dayProcessClick_view(request):
    templates_name = "dayProcess/wedding_day_process.html"
    context = {
        'title':'婚宴當日流程 Wedding day process'
    }
    return render(request, templates_name, context)
