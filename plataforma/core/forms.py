# forms.py
from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, label='Data inicial')
    end_date = forms.DateField(required=False, label='Data final')
