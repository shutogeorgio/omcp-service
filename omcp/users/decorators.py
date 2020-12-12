from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from users.doctor import Doctor

from diagnoses.models import Diagnosis


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator


def diagnosis_owner_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'patient':
            return redirect('/diagnoses')

        if group == 'doctor':
            return view_func(request, *args, **kwargs)

    return wrapper_function


# Doctor Validation
def doctor_validity(view_func):
    def wrapper_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_doctor:
            doctor = get_object_or_404(Doctor, user_id=current_user.id)
            if doctor.validity == 'VALID':
                return view_func(request, *args, **kwargs)
        return redirect('/diagnoses')

    return wrapper_function


# License Editability
def license_mods_eligibility(view_func):
    def wrapper_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_doctor:
            doctor = get_object_or_404(Doctor, user_id=current_user.id)
            if doctor.validity != 'VALID':
                return view_func(request, *args, **kwargs)
        return redirect('/profile/{}'.format(current_user.id))

    return wrapper_function


def summary_required(view_func):
    def wrapper_function(request, diagnosis_id, *args, **kwargs):
        current_user = request.user
        diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)
        if diagnosis.status == 'COMPLETED':
            if current_user.is_doctor & current_user.id == diagnosis.doctor.user_id:
                return view_func(request, diagnosis_id, *args, **kwargs)
        return redirect('/diagnoses/{}'.format(diagnosis_id))

    return wrapper_function
