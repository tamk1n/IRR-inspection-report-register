from django import forms
from django.utils.translation import gettext_lazy as _


class NewIRForm(forms.Form):
    date = forms.DateField(label=_())
