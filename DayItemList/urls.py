from django.urls import path

from . import views

app_name = "dayitem"

# Create your urls here.
urlpatterns = [
    path("dayItemListClick/", views.dayItemListClick_view, name="dayitemlistclick"),
   
]
