from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import NewIRForm
from .models import InspectionReport, Observation



class HomePageView(generic.TemplateView):
    """Just Home Page View"""
    template_name = "irr_app/home_page.html"


class UserLoginView(LoginView):
    """Logs in user"""
    template_name = "irr_app/login.html"
    redirect_authenticated_user = False
    form_class = AuthenticationForm


class UserLogoutView(LogoutView):
    http_method_names = ['post']

"""@method_decorator(login_required, name="dispatch")
class NewIRView(generic.FormView):
    Creates new Inspection Report Form
    template_name = "irr_app/newir.html"
    
    form_class = NewIRForm
    success_url = reverse_lazy('irr_app:register')

    def get_form_kwargs(self) -> dict[str, Any]:
        Adds authenticated user to keyword arguments
           Return keyword arguments
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form: NewIRForm) -> HttpResponse:
        Form validation
        date = form.cleaned_data['date']
        project = form.cleaned_data['project']
        division = form.cleaned_data['division']
        field = form.cleaned_data['field']
        responsible_person = form.cleaned_data['responsible_person']
        observation1 = form.cleaned_data['observation1']
        observation2 = form.cleaned_data['observation2']
        ir_type = form.cleaned_data['ir_type']

        observation1 = Observation.objects.create(content=observation1)
        observation2 = Observation.objects.create(content=observation2)
        new_report = InspectionReport.objects.create(date=date,
                                        project=project,
                                        division=self.request.user.employee_company.first().company_dvs.filter(name=division).first(),
                                        field=field,
                                        responsible_person=responsible_person,
                                        ir_type=ir_type
                                        )
        
        new_report.engineer.add(self.request.user)
        new_report.observations.add(observation1, observation2)
        return super().form_valid(form)"""


class NewIRView(generic.CreateView):
    #model = InspectionReport
    #fields = ['date', 'project', 'field', 'responsible_person', 'observations', 'ir_type']
    template_name = 'irr_app/newir.html'
    form_class = NewIRForm
    success_url = reverse_lazy('irr_app:irr')
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs.pop('instance')
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.engineer.add(self.request.user)
        return super().form_valid(form)
    
@method_decorator(login_required, name="dispatch")
class IRRegisterView(generic.ListView):
    model = InspectionReport
    template_name = 'irr_app/done.html'
    paginator_class = Paginator
    paginate_by = 15
    
    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        company = user.employee_company.first()
        divisions = company.company_dvs.all()
        queryset = InspectionReport.objects.filter(division__in=divisions).all()
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name="dispatch")
class SingleDeleteIR(generic.DeleteView):
    model = InspectionReport
    http_method_names = ['post']
    success_url = reverse_lazy('irr_app:irr')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        # checks if the authenticated user is the creator of the IR
        if self.object in self.request.user.my_irs.all():
            self.object.delete()

        return HttpResponseRedirect(success_url)


@method_decorator(login_required, name="dispatch")
class UpdateIRView(generic.UpdateView):
    model = InspectionReport
    template_name = 'irr_app/newir.html'
    form_class = NewIRForm
    #fields = ['date', 'project', 'field', 'responsible_person', 'observations', 'ir_type']

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs