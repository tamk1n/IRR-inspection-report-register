from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
# Create your views here.

class HomePageView(generic.TemplateView):
    template_name = "irr_app/home_page.html"

class UserLoginView(LoginView):
    template_name = "irr_app/login.html"
    redirect_authenticated_user = False
    form_class = AuthenticationForm

    
    

