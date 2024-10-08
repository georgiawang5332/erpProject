from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from accounts.forms import SignInForm


class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {
            "form": forms,
            "user_avatar": request.user.avatar.url if request.user.is_authenticated and request.user.avatar else None
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("dash:dashboard")
        context = {
            "form": forms,
            # 因在此createsuperuser新增會無法顯示照片所以利用createsuperuser新增的都會進不去產生錯誤! nav.html 就添加了if else
            "user_avatar": request.user.avatar.url if request.user.is_authenticated and request.user.avatar else None
            }
        return render(request, self.template_name, context)

