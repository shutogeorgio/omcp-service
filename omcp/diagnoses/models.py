from django.db import models

from .register_status import RegisterStatus
from .diagnosis_type import DiagnosisType
from users.doctor import Doctor
from users.patient import Patient


class Diagnosis(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=None, blank=True, null=True)
    title = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=1000, default="")
    video_link = models.CharField(max_length=100, default="")
    video_password = models.CharField(max_length=50, default="")
    type = models.CharField(max_length=50, default=DiagnosisType.MENTAL)
    status = models.CharField(max_length=50, default=RegisterStatus.REGISTERED)
    date = models.DateField(blank=True, null=True)
    image = models.FileField(upload_to='diagnoses/', blank=True, default='diagnoses/no-img.jpg')
