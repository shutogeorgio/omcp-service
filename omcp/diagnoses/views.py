from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import DiagnosisCreationForm, SummaryCreationForm
from .models import Diagnosis
from .register_status import RegisterStatus
from users.doctor import Doctor
from users.patient import Patient

from .summary import Summary


def list_diagnosis(request):
    diagnoses = Diagnosis.objects.all()
    current_user = request.user
    template_path = '../frontend/diagnoses/list.html'
    return render(request, template_path, context={'user': current_user, 'diagnoses': diagnoses})


@login_required
def desc_diagnosis(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    current_user = request.user
    owner = False
    if current_user.is_patient:
        if diagnosis.status == str(RegisterStatus.REGISTERED):
            if diagnosis.patient.user.id == current_user.id:
                owner = True
    elif current_user.is_doctor:
        if diagnosis.doctor.user.id == current_user.id:
            owner = True
    template_path = '../frontend/diagnoses/desc.html'
    return render(request, template_path,
                  context={'user': current_user, 'diagnosis': diagnosis, 'owner': owner})


@login_required
def create_diagnosis(request):
    current_user = request.user
    template_path = '../frontend/diagnoses/create.html'
    form = DiagnosisCreationForm(request.POST or None,
                                 request.FILES or None)
    if request.method == 'POST':
        if current_user.is_doctor:
            if form.is_valid():
                doctor = get_object_or_404(Doctor, user_id=current_user.id)
                form = DiagnosisCreationForm(request.POST,
                                             request.FILES, instance=doctor)
                form.save(request.FILES, doctor)
                return redirect('/diagnoses')
    return render(request, template_path, context={'user': current_user, 'form': form})


@login_required
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


@login_required
def complete_diagnosis(request, diagnosis_id):
    current_user = request.user
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    if diagnosis.doctor.user.id == current_user.id:
        if request.method == 'POST':
            if diagnosis.status == 'REGISTERED':
                diagnosis.status = RegisterStatus.COMPLETED
                diagnosis.save()
                return redirect('/diagnoses/{}/summary/create'.format(diagnosis_id))
            return redirect('/diagnoses')
        return redirect('/diagnoses')


# Summary Configuration
@login_required
def create_summary(request, diagnosis_id):
    current_user = request.user
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    template_path = '../frontend/diagnoses/summary/create.html'
    form = SummaryCreationForm()
    if diagnosis.status != 'COMPLETED':
        return redirect('/diagnoses/{}'.format(diagnosis_id))
    if request.method == 'POST':
        if current_user.is_doctor:
            form = SummaryCreationForm(request.POST or None,
                                       request.FILES or None, instance=diagnosis)
            if form.is_valid():
                form.save(diagnosis)
                return redirect('/diagnoses/{}/summary'.format(diagnosis_id))

    return render(request, template_path, context={'user': current_user, 'form': form, 'diagnosis': diagnosis})


@login_required
def desc_summary(request, diagnosis_id):
    current_user = request.user
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
    template_path = '../frontend/diagnoses/summary/desc.html'
    if diagnosis.status == 'COMPLETED':
        if diagnosis.doctor.user.id == current_user.id:
            summary = get_object_or_404(Summary, diagnosis_id=diagnosis_id)
            return render(request, template_path, context={'user': current_user, 'summary': summary})
        elif diagnosis.patient.user.id == current_user.id:
            summary = get_object_or_404(Summary, diagnosis_id=diagnosis_id)
            return render(request, template_path, context={'user': current_user, 'summary': summary})
    return redirect('/diagnoses/{}'.format(diagnosis_id))
