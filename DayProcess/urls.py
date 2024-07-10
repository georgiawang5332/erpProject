from django.urls import path

from . import views

app_name = "dayprocess"

# Create your urls here.
urlpatterns = [
    path("dayProcess/", views.dayProcessClick_view, name="dayprocessclick"),
   
]
