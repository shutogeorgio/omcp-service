from django.db import models
from .user import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    request = models.CharField(max_length=100)
    image_folder = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    validity = models.CharField(max_length=100)