from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from .models import Division


class NewIRForm(forms.Form):
    date = forms.DateField(
        label=_("Date"), 
        widget=forms.SelectDateWidget())
  
    project = forms.CharField(label=_("Project"))
    division = forms.ModelChoiceField(label=_("Division"), queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if user:
            self.fields['division'].queryset = user.employee_company.first().company_dvs

    field = forms.CharField(label=_("Field"))

    responsible_person = forms.CharField(
        label=_("Responsible Person"))

    observation1 = forms.CharField(
        label=_("Observation 1"),
        widget=forms.Textarea)
    
    observation2 = forms.CharField(
        label=_("Observation 2"),
        widget=forms.Textarea)

    ir_type = forms.ChoiceField(choices=[
            ('NGT', _('Negative')),
            ('POS', _('Positive'))
        ])






