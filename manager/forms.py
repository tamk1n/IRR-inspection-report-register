from django import forms

class AddEngineerForm(forms.Form):
    email = forms.EmailField()