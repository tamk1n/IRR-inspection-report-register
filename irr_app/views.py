from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from .forms import NewIRForm
from .models import InspectionReport, Division, Observation
from manager.models import Company


class HomePageView(generic.TemplateView):
    template_name = "irr_app/home_page.html"


class UserLoginView(LoginView):
    template_name = "irr_app/login.html"
    redirect_authenticated_user = False
    form_class = AuthenticationForm


class NewIRView(generic.FormView):
    template_name = "irr_app/newir.html"
    form_class = NewIRForm
    success_url = reverse_lazy('irr_app:register')

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
        new_report = InspectionReport.objects.create(date=date,
                                        project=project,
                                        company=company,
                                        division=company.company_dvs.filter(name=division).first(),
                                        field=field,
                                        responsible_person=responsible_person,
                                        ir_type=ir_type
                                        )
        
        new_report.engineer.add(self.request.user)
        new_report.observations.add(observation1, observation2)
        return super().form_valid(form)

class IRRegisterView(generic.ListView):
    model = InspectionReport
    template_name='irr_app/done.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        company = user.employee_company.first()
        queryset = InspectionReport.objects.filter(company=company).all()
        print(queryset)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context)
        return context

