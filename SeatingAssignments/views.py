from django.shortcuts import render

# Create your views here.
def tableSeatingAssignmentsClick_view(request):
    templates_name = "tableSeating/table_seating_assignments.html"
    context = {
        'title':'桌座位分配 Table seating assignments'
    }
    return render(request, templates_name, context)

