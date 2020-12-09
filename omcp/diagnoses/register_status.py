from django.db import models


class RegisterStatus(models.TextChoices):
    UNREGISTERED = "UNREGISTERED"
    REGISTERED = "REGISTERED"
    COMPLETED = "COMPLETED"
