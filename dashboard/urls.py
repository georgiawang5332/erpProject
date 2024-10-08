
from django.urls import path
from . import views
from .views import DashboardView

app_name = "dash"

# urls your views here.

urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    # path('dashboard/', views.DashboardView, name='dashboard'),#home
    path('aboutus', views.Dashboard_About_us_view, name="d_aboutus"),
]
