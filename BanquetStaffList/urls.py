from django.urls import path

from . import views

app_name = "staffList"

# Create your urls here.
urlpatterns = [
    path("banquetStaffList/", views.banquetStaffListClick_view, name="stafflistclick"),
   
]
