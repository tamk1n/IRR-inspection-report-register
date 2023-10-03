from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .forms import NewIRForm
from .models import InspectionReport, Division, Observation


class HomePageView(generic.TemplateView):
    template_name = "irr_app/home_page.html"


class UserLoginView(LoginView):
    template_name = "irr_app/login.html"
    redirect_authenticated_user = False
    form_class = AuthenticationForm


class NewIRView(generic.FormView):
    template_name = "irr_app/newir.html"
    form_class = NewIRForm
    success_url = reverse_lazy('irr_app:done')

    def form_valid(self, form: NewIRForm) -> HttpResponse:
        date = form.cleaned_data['date']
        project = form.cleaned_data['project']
        division = form.cleaned_data['division']
        field = form.cleaned_data['field']
        responsible_person = form.cleaned_data['responsible_person']
        observation1 = form.cleaned_data['observation1']
        observation2 = form.cleaned_data['observation2']
        type_of_observation = form.cleaned_data['type_of_observation']

        Observation.objects.create(content=observation1)
        Observation.objects.create(content=observation2)
        #print(self.request.user.username)
        InspectionReport.objects.create(date=date,
                                        engineer=self.request.user,
                                        project=project,
                                        company=self.request.user.employee_company,
                                        )
        return super().form_valid(form)

class DoneView(generic.TemplateView):
    template_name='irr_app/done.html'
    
    

