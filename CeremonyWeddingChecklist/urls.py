from django.urls import path

from . import views

app_name = "ceremony"

# Create your urls here.
urlpatterns = [
    path("ceremonyItemsChecklist/", views.ceremonyItemsChecklistClick_view, name="ceremonyitemsclick"),
   
]
