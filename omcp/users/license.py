from django.db import models
from .doctor import Doctor


class License(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, primary_key=True)
    image = models.FileField(upload_to='licenses/', blank=True, default='licenses/sample.jpg')

