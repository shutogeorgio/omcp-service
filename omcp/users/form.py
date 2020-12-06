from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction

from .models import User
from .patient import Patient
from .doctor import Doctor
from .license import License
from .validity import Validity


class PatientSignUpForm(UserCreationForm):
    email = forms.CharField(required=True)
    name = forms.CharField(required=True)
    country = forms.CharField(required=True)
    address = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.email = self.cleaned_data.get('email')
        user.save()

        patient = Patient.objects.create(user=user)
        patient.name = self.cleaned_data.get('name')
        patient.country = self.cleaned_data.get('country')
        patient.address = self.cleaned_data.get('address')
        patient.zipcode = self.cleaned_data.get('zipcode')
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.image_folder = "no-image.png"
        patient.information = ""
        patient.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    email = forms.CharField(required=True)
    name = forms.CharField(required=True)
    country = forms.CharField(required=True)
    address = forms.CharField(required=True)
    zipcode = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    license_image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.email = self.cleaned_data.get('email')
        user.save()

        doctor = Doctor.objects.create(user=user)
        doctor.name = self.cleaned_data.get('name')
        doctor.country = self.cleaned_data.get('country')
        doctor.address = self.cleaned_data.get('address')
        doctor.zipcode = self.cleaned_data.get('zipcode')
        doctor.phone_number = self.cleaned_data.get('phone_number')
        doctor.image_folder = "no-image.png"
        doctor.speciality = ""
        doctor.validity = Validity.IN_REVIEW
        doctor.save()

        cert = License.objects.create(doctor=doctor)
        cert.image_folder = self.cleaned_data.get('license_image')
        cert.save()
        return user
