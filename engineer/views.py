from django.shortcuts import render
from django.views import generic
# Create your views here.

class EngineerRegisterView(generic.TemplateView):
    template_name='engineer-register.html'