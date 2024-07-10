from django.urls import path

from . import views

app_name = "preparation"

# Create your urls here.
urlpatterns = [
    path("preparationFlowChart/", views.preparationFlowChartClick_view, name="preparationclick"),
   
]
