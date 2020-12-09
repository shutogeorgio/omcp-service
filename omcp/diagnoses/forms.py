from django import forms
from django.forms import ModelForm

from .models import Diagnosis
from .register_status import RegisterStatus
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

    def save(self, doctor):
        diagnosis = Diagnosis.objects.create(doctor=doctor)
        diagnosis.status = RegisterStatus.UNREGISTERED
        diagnosis.title = self.cleaned_data.get('title')
        diagnosis.description = self.cleaned_data.get('description')
        diagnosis.date = self.cleaned_data.get('date')
        diagnosis.image = self.cleaned_data.get('image')
        diagnosis.video_link = self.cleaned_data.get('video_link')
        diagnosis.video_password = self.cleaned_data.get('video_link')
        diagnosis.save()
        return diagnosis


class SummaryCreationForm(ModelForm):
    class Meta:
        model = Summary
        fields = ['comment']

    def save(self, diagnosis):
        summary = Summary.objects.create(diagnosis=diagnosis)
        summary.comment = self.cleaned_data.get('comment')
        summary.save()
        return summary
