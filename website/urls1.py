
from django.urls import path
from . import views

app_name = "web"

# urls your views here.

urlpatterns = [
    # path('', views.WebsiteView, name='website'),


    path('', views.home_view, name='home'),
    # path('logout', LogoutView.as_view(template_name='quiz/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view, name="aboutus"),
    path('contactus', views.contactus_view, name="contactus"),
    # path('afterlogin', views.afterlogin_view, name='afterlogin'),
    # path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),#儀表板-後台ERP

    # path('adminclick', views.adminclick_view, name="adminclick"),

]
