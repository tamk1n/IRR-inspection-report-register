from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from .models import Division, InspectionReport


class NewIRForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        if user:
            self.fields['division'].queryset = user.employee_company.\
                first().company_dvs.all()

    observation1 = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 30, "rows": 5}))
    observation2 = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 30, "rows": 5}))
    
    class Meta:
        model = InspectionReport
        fields = ('date', 'project',
                  'division', 'field', 'responsible_person',
                  'ir_type')
    
        widgets = {
            'date': forms.SelectDateWidget(),
        }

        
    





