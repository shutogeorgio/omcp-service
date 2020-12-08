from django.db import models

from .models import Diagnosis


class Summary(models.Model):
    diagnosis = models.OneToOneField(Diagnosis, on_delete=models.CASCADE, primary_key=True)
    comment = models.CharField(max_length=1000, default="")
