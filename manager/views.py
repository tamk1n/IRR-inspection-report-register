from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from http import HTTPStatus
from .forms import AddEngineerForm
from django.urls import reverse_lazy

# Create your views here.

class RegisterEmployeeView(View):
    template_name='manager/add_engineer.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {}
        context['form'] = AddEngineerForm
        return render(request=request, template_name=self.template_name, context=context, status=HTTPStatus.OK)
    
    def post(self, request: HttpRequest, *args, **kwargs):
        form = AddEngineerForm(self.request.POST)
        if form.is_valid():
            redirect_url = reverse_lazy("irr_app:home-page")
            return HttpResponseRedirect(redirect_url)
        else:
            context = {}
            context['form'] = AddEngineerForm

        return render(request=request, template_name=self.template_name, context=context, status=HTTPStatus.OK)

