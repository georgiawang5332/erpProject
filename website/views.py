from django.shortcuts import render,redirect,reverse
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def afterlogin_view(request):
    return redirect('dash:dashboard')

def home_view(request):
    template_name = "website/webIndex.html"
    # 訪問此視圖的次數，在會話變量中計算。 Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # if request.user.is_authenticated:
        # return HttpResponseRedirect('web:home')
        # return redirect(reverse('web:home'))
    if request.user.is_authenticated and request.path != reverse('web:home'):
        return redirect(reverse('web:home'))

    context={'num_visits': num_visits}  
    return render(request, template_name, context)

def aboutus_view(request):
    return render(request,'website/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'website/contactussuccess.html')
    return render(request, 'website/contactus.html', {'form':sub})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return redirect(reverse('account:signin'))
    # return HttpResponseRedirect('account:signin')
