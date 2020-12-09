from django import forms
from django.forms import ModelForm

from .models import Diagnosis
from .summary import Summary


class DateInput(forms.DateInput):
    input_type = 'date'


class DiagnosisCreationForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['title', 'description', 'date', 'video_link', 'video_password', 'image']
        widgets = {
            'date': DateInput(),
        }


class SummaryCreationForm(ModelForm):
    class Meta:
        model = Summary
        fields = ['comment']
