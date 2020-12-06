from django.db import models
from .doctor import Doctor


class License(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, primary_key=True)
    image_folder = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.image_folder
