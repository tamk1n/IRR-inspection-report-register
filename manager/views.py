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
# Create your views here.

User = get_user_model()


class AddEngineerView(View):
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
        register_token = EngineerRegisterationToken.objects.create(
            company=company
        )

        register_url = self.request.build_absolute_uri(
            reverse('manager:register-engineer', args=[register_token.token]))

        self.send_email(register_token, engineer_email, register_url)
        
        return render(request, self.template_name, context, status=HTTPStatus.OK)

    def send_email(self, engineer_email, register_url):
        create_token_and_send_email.delay(engineer_email, register_url)


class EngineerRegisterView(generic.CreateView):
    form_class = EngineerRegisterForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        raw_token = self.kwargs.get('token', None)
        self.template_name = 'manager/engineer-register.html' if EngineerRegisterationToken.objects.\
            filter(token=is_valid_uuid(raw_token), is_expired=True).exists() else 'manager/invalid.html'

        if not is_token_valid(raw_token):
            render(self.request, 'manager/invalid.html', status=HTTPStatus.BAD_REQUEST)

        def is_valid_uuid(token):
            try:
                return uuid.UUID(token)
            except ValueError:
                return False

        def is_token_valid(token):
            uuid_token = is_valid_uuid(token)
            if not uuid_token or not EngineerRegisterationToken.objects.filter(token=uuid_token, is_expired=True).exists():
                return False
            #render(self.request, 'manager/invalid.html', status=HTTPStatus.BAD_REQUEST)
            #return render(self.request, 'manager/engineer-register.html', status=HTTPStatus.OK) 
        
        return render(self.request, 'manager/engineer-register.html', status=HTTPStatus.OK) 