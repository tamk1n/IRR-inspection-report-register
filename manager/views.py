from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from http import HTTPStatus
from .forms import AddEngineerForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class RegisterEmployeeView(View):
    template_name = 'manager/add_engineer.html'
    form_class = AddEngineerForm
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context: dict = {}
        context['form'] = self.form_class
        return render(request, self.template_name, context, status=HTTPStatus.OK)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(self.request.POST)
        context = {}

        if not form.is_valid():
            context['form'] = form
            return render(request, self.template_name, context=context, status=HTTPStatus.BAD_REQUEST)

        return render(request, self.template_name, context, status=HTTPStatus.OK)


    def user_fullname(self):
        show_user_fullname.delay(user=self.request.user)
