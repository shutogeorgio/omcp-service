from django import forms
from django.core.files.storage import FileSystemStorage
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

    def save(self, files, doctor):
        diagnosis = Diagnosis.objects.create(doctor=doctor)
        diagnosis.status = RegisterStatus.UNREGISTERED
        diagnosis.title = self.data.get('title')
        diagnosis.description = self.data['description']
        diagnosis.date = self.data['date']
        image_data = files['image']
        fs = FileSystemStorage()
        filename = fs.save(image_data.name, image_data)
        diagnosis.image = filename
        diagnosis.video_link = self.data['video_link']
        diagnosis.video_password = self.data['video_password']
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
