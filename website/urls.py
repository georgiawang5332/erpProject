
from django.urls import path
from . import views

app_name = "web"

# urls your views here.

urlpatterns = [
    # path('', views.WebsiteView, name='website'),


    path('', views.home_view, name='home'),
    path('aboutus', views.aboutus_view, name="aboutus"),
    path('contactus', views.contactus_view, name="contactus"),
  
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('adminclick', views.adminclick_view, name="adminclick"),

]
