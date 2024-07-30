from django.urls import path
from . import views

app_name = "send_email"

# Create your urls here.
urlpatterns = [
    path('', views.sendEmail, name='sendEmail')

]
