from django.db import models
from .models import User
from .validity import Validity


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, default="")
    zipcode = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=20, default="")
    image = models.FileField(upload_to='users/', blank=True, default='users/no-img.svg')
    speciality = models.CharField(max_length=100, default="")
    validity = models.CharField(max_length=100, default=Validity.IN_REVIEW)
