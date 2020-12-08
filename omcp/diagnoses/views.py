from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import DiagnosisCreationForm
from .models import Diagnosis
from .register_status import RegisterStatus
from users.doctor import Doctor
from users.patient import Patient


def list_diagnosis(request):
    diagnoses = Diagnosis.objects.all()
    current_user = request.user
    template_path = '../frontend/diagnoses/list.html'
    return render(request, template_path, context={'user': current_user, 'diagnoses': diagnoses})


def desc_diagnosis(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    current_user = request.user
    template_path = '../frontend/diagnoses/desc.html'
    return render(request, template_path, context={'user': current_user, 'diagnosis': diagnosis})


def create_diagnosis(request):
    current_user = request.user
    template_path = '../frontend/diagnoses/create.html'
    form = DiagnosisCreationForm(request.POST or None,
                                 request.FILES or None)
    if request.method == 'POST':
        if current_user.is_doctor:
            if form.is_valid():
                doctor = get_object_or_404(Doctor, user_id=current_user.id)
                form = DiagnosisCreationForm(request.POST or None,
                                             request.FILES or None, instance=doctor)
                form.save()
                return redirect('/diagnoses')
    return render(request, template_path, context={'user': current_user, 'form': form})


def register_diagnosis(request, diagnosis_id):
    current_user = request.user
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    if current_user.is_patient:
        patient = get_object_or_404(Patient, user_id=current_user.id)
        if request.method == 'POST':
            if diagnosis.status == 'UNREGISTERED':
                diagnosis.status = 'REGISTERED'
                diagnosis.patient = patient
                diagnosis.save()
                return redirect('/diagnoses/{}'.format(diagnosis_id))
            return redirect('/diagnoses')
        return redirect('/diagnoses')
