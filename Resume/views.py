from django.shortcuts import render

# Create your views here.
def ResumeView(request):
    template_name = 'resume/resume.html'
    context = {
        'title': '履歷表'
    }
    return render(request, template_name, context)