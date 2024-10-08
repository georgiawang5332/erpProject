from django.shortcuts import render

# Create your views here.
def invitationSendingFormClick_view(request):
    templates_name = "invitationSending/invitation_sending_form.html"
    context = {
        'title':'喜帖發送表 wedding invitation sending form'
    }
    return render(request, templates_name, context)

