from django.shortcuts import render

# Create your views here.
def preparationFlowChartClick_view(request):
    templates_name = "preparation/preparation_flow_chart_click.html"
    context = {
        'title':' 婚禮籌備流程表 Wedding preparation flow chart'
    }
    return render(request, templates_name, context)

