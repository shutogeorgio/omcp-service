from django.db import models
from .models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, default="")
    zipcode = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=20, default="")
    request = models.CharField(max_length=100, null=True)
    image_folder = models.CharField(max_length=100, default="")
