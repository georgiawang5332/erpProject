from django.urls import path
from . import views

app_name = "resume"

# Create your urls here.
urlpatterns = [
    path('resume/', views.ResumeView, name='resume_app')

]
