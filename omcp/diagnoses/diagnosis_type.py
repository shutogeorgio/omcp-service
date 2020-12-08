from django.db import models


class DiagnosisType(models.TextChoices):
    MENTAL = 'Mental Illness'
    PREVENTIVE = 'Preventive Medicine'
