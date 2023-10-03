from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Division


class NewIRForm(forms.Form):
    date = forms.DateField(
        label=_("Date"), 
        widget=forms.SelectDateWidget())
  
    project = forms.CharField(label=_("Project"))

    division = forms.ModelChoiceField(
        label=_("Project"),
        queryset = Division.objects.all())

    field = forms.CharField(label=_("Field"))

    responsible_person = forms.CharField(
        label=_("Responsible Person"))

    observation1 = forms.CharField(
        label=_("Observation 1"),
        widget=forms.Textarea)
    
    observation2 = forms.CharField(
        label=_("Observation 2"),
        widget=forms.Textarea)

    type_of_observation = forms.ChoiceField(choices=[
            ('NGT', _('Negative')),
            ('POS', _('Positive'))
        ])






