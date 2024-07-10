from django.urls import path

from . import views

app_name = "table"

# Create your urls here.
urlpatterns = [
    path("tableSeatingAssignments/", views.tableSeatingAssignmentsClick_view, name="tableseatingclick"),
   
]
