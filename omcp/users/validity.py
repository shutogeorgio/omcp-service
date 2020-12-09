from django.db import models


class Validity(models.TextChoices):
    IN_REVIEW = "IN_REVIEW"
    VALID = "VALID"
