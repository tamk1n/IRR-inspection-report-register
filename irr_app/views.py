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
        ir_type = form.cleaned_data['ir_type']
        company = self.request.user.employee_company.first()

        observation1 = Observation.objects.create(content=observation1)
        observation2 = Observation.objects.create(content=observation2)
        #print(self.request.user.username)
        new_report = InspectionReport.objects.create(date=date,
                                        #engineer=self.request.user,
                                        project=project,
                                        company=company,
                                        division=company.company_dvs.filter(name=division).first(),
                                        field=field,
                                        responsible_person=responsible_person,
                                        #observation1=observation1,
                                        #observation2=observation2,
                                        ir_type=ir_type
                                        )
        new_report.engineer.add(self.request.user)
        new_report.observations.add(observation1, observation2)
        return super().form_valid(form)

class DoneView(generic.TemplateView):
    template_name='irr_app/done.html'
    
    

