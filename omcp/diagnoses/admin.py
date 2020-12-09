from django.contrib import admin

# Register your models here.
from .models import Diagnosis
from .summary import Summary

admin.site.register(Diagnosis)
admin.site.register(Summary)
