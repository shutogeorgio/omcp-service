from django.contrib import admin
from .models import User
from .patient import Patient
from .doctor import Doctor
from .license import License

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(License)
