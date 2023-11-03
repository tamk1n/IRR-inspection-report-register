from typing import Any
from django import http
from django.shortcuts import render
from django.views import View, generic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from http import HTTPStatus
from .forms import AddEngineerForm, EngineerRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .tasks import create_token_and_send_email
from engineer.models import EngineerRegisterationToken
import os
from django.urls import reverse
import uuid
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .permissions import test_func
# Create your views here.

User = get_user_model()


class AddEngineerView(View, UserPassesTestMixin):
    template_name = 'manager/add_engineer.html'
    form_class = AddEngineerForm
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        context['form'] = self.form_class
        return render(request, self.template_name, context, status=HTTPStatus.OK)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(self.request.POST)
        context: dict = {}

        if not form.is_valid():
            context['form'] = form
            return render(request, self.template_name, context=context, status=HTTPStatus.BAD_REQUEST)
        
        engineer_email = form.cleaned_data['email']
        company = self.request.user.manager_company.first()
        print(company)
        register_token = EngineerRegisterationToken.objects.create(
            company=company
        )

        register_url = self.request.build_absolute_uri(
            reverse('manager:register-engineer', args=[register_token.token]))

        self.send_email(engineer_email, register_url)
        
        return render(request, self.template_name, context, status=HTTPStatus.OK)

    def send_email(self, engineer_email, register_url):
        create_token_and_send_email.delay(engineer_email, register_url)


class EngineerRegisterView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = EngineerRegisterForm

    # checks if user position is Manager
    def test_func(self):
        return self.request.user.position == 'Manager'
    
    def get(self, request, *args, **kwargs):
        raw_token = self.kwargs.get('token', None)
        context = {}
        context['token'] = raw_token

        if not self.is_token_valid(raw_token):
            return render(self.request, 'manager/invalid.html', context, status=HTTPStatus.BAD_REQUEST)
        
        return render(self.request, 'manager/engineer-register.html', context, status=HTTPStatus.OK)
    
    def is_valid_uuid(self, token):
        try:
            return uuid.UUID(token)
        except ValueError:
            return False

    def is_token_valid(self, token):
        uuid_token = self.is_valid_uuid(token)
        return False if not uuid_token or not EngineerRegisterationToken.objects.filter(
            token=uuid_token, is_expired=False).exists() else True
