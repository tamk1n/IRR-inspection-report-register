from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from http import HTTPStatus
from .forms import AddEngineerForm
from django.urls import reverse_lazy

# Create your views here.


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

