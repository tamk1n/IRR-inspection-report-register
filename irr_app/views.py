from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
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
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(generic.TemplateView):
    """Just Home Page View"""
    template_name = "irr_app/home_page.html"


class UserLoginView(LoginView):
    """Logs in user"""
    template_name = "irr_app/login.html"



class UserLogoutView(LogoutView):
    """Logs user out and
    Redirect user to login page
    Customize LOGOUT_REDIRECT_URL in settings.py
    Only accepts POST request. 
    Any other request handled by Handle405Middleware"""
    http_method_names = ['post']


class NewIRView(LoginRequiredMixin, generic.CreateView):
    """Creates new IR
    Redirect user to IR Register after successfully create IR"""
    template_name = 'irr_app/newir.html'
    form_class = NewIRForm
    success_url = reverse_lazy('irr_app:irr')
    
    def get_form_kwargs(self) -> dict[str, Any]:
        """Add authenticated user to keyword arguments
        It will be used in forms"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()

        # create new observations since 
        # Observation and InspectionReport are many-to-many related
        obs1 = Observation.objects.create(content=form.cleaned_data['observation1'])
        obs2 = Observation.objects.create(content=form.cleaned_data['observation2'])

        # add the engineer who raised IR to InspectionReport
        # since MyUser and Inspection Report are many-to-one related
        self.object.engineer.add(self.request.user)
        self.object.observations.add(obs1, obs2)
        return super().form_valid(form)


class IRRegisterView(LoginRequiredMixin, generic.ListView):
    model = InspectionReport
    template_name = 'irr_app/done.html'
    paginator_class = Paginator
    paginate_by = 15
    
    def get_queryset(self) -> QuerySet[Any]:
        """queryset for specific division which is part of user's company"""
        user = self.request.user
        company = user.employee_company.first()
        divisions = company.company_dvs.all()
        queryset = InspectionReport.objects.select_related('division__company').filter(division__in=divisions).all()
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class SingleDeleteIR(LoginRequiredMixin, generic.DeleteView):
    """Single delete of IR.
    View only accepts POST Request
    Any other request handled by Handle405Middleware"""
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


class UpdateIRView(LoginRequiredMixin, generic.UpdateView):
    model = InspectionReport
    template_name = 'irr_app/newir.html'
    success_url = reverse_lazy('irr_app:irr')
    form_class = NewIRForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """If user is not the creator of IR it redirects user to success_url"""
        self.object = self.get_object()
        if self.object in self.request.user.my_irs.all():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        ir = self.object
        initial = {'observation1': ir.observations.all()[0].content,
                   'observation2': ir.observations.all()[1].content}
        return initial
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        ir = self.object

        self.object = form.save()

        # create new observations since 
        # Observation and InspectionReport are many-to-many related
        obs1, obs2 = ir.observations.all()[0], ir.observations.all()[1]
        obs1.content, obs2.content = form.cleaned_data['observation1'], form.cleaned_data['observation2']
        obs1.save()
        obs2.save()
        return super().form_valid(form)
