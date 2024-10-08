from django.urls import path

from . import views

app_name = "invite"

# Create your urls here.
urlpatterns = [
    # path('', views._view, name=''),
    path("invite/", views.inviteclick_view, name="invite"),
    path('questionclick', views.questionclick_view, name="questionclick_view"),
    path('givemoneyclick', views.givemoney_view, name="givemoney_view"),
    path('notattendclick', views.notattend_view, name="notattend_view"),
]
