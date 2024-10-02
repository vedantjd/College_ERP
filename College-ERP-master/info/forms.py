# forms.py
from django import forms

class ToggleForm(forms.Form):
    checkbox = forms.BooleanField(label='Toggle', required=False)
