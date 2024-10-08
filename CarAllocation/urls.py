from django.urls import path

from . import views

app_name = "carAllocation"

# Create your urls here.
urlpatterns = [
    path("carAllocation/", views.carAllocationClick_view, name="carallocationclick"),
   
]
