from django.db import models
from .models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, default="")
    zipcode = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=20, default="")
    image_folder = models.CharField(max_length=100, null="")
    speciality = models.CharField(max_length=100, default="")
    validity = models.CharField(max_length=100, default=" ")