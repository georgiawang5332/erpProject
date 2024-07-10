from django.urls import path

from . import views

app_name = "invitesend"

# Create your urls here.
urlpatterns = [
    path("InvitationSending/", views.invitationSendingFormClick_view, name="invitationsendclick"),
   
]
