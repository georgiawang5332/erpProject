from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from calendarapp.models import Event

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    # template_name = "calendarapp/dashboard.html"
    template_name = "dashboard/dataIndex.html" 

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)

# def DashboardView(request): 
#     template_name = "dashboard/dataIndex.html" 
#     context={'title':'我是後台資料 Data'}
#     return render(request,template_name,context)  

def Dashboard_About_us_view(request): 
    template_name = "dashboard/aboutus.html" 
    context={'title':'我是關於我'}
    return render(request,template_name,context)  