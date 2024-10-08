from django.shortcuts import render

# Create your views here.
def ceremonyItemsChecklistClick_view(request):
    templates_name = "ceremony/ceremony_items_preparation_checklist.html"
    context = {
        'title':'儀式婚禮物品準備清單 Ceremony Wedding Items Preparation Checklist'
    }
    return render(request, templates_name, context)

