from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

from .patient import Patient
from .doctor import Doctor


# Home
def home(request):
    template_path = '../frontend/index.html'
    return render(request, template_path)


# Login & Signup Logic
def signup(request):
    template_path = '../frontend/signup/index.html'
    return render(request, template_path)


class patient_signup(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = '../frontend/signup/patient.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class doctor_signup(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = '../frontend/signup/doctor.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    template_path =  '../frontend/login.html'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, template_path,
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


# Profile Configuration
def desc_own_profile(request):
    current_user = request.user
    template_path = '../frontend/profile/own_desc.html'
    if current_user.is_patient:
        profile = Patient.objects.get(user_id=current_user.id)
    elif current_user.is_doctor:
        profile = Doctor.objects.get(user_id=current_user.id)
    else:
        profile = ''
    return render(request, template_path, context={'user': current_user, 'profile': profile})


def desc_profile(request, user_id):
    req_user = User.objects.get(id=user_id)
    template_path = '../frontend/profile/desc.html'
    if req_user.is_patient:
        profile = Patient.objects.get(user_id=req_user.id)
    elif req_user.is_doctor:
        profile = Doctor.objects.get(user_id=req_user.id)
    else:
        profile = ''
    return render(request, template_path, context={'user': req_user, 'profile': profile})


def update_profile(request):
    current_user = request.user
    template_path = '../frontend/profile/edit.html'
    if current_user.is_patient:
        profile = Patient.objects.get(user_id=current_user.id)
    elif current_user.is_doctor:
        profile = Doctor.objects.get(user_id=current_user.id)
    else:
        redirect('/login')
    return render(request, template_path, context={'user': current_user, 'profile': profile})


def handle_update_profile(request):
    current_user = request.user
    template_path = '../frontend/profile/desc.html'
    if current_user.is_patient:
        profile = Patient.objects.get(user_id=current_user.id)
    elif current_user.is_doctor:
        profile = Doctor.objects.get(user_id=current_user.id)
    else:
        redirect('/login')
    return render(request, template_path, context={'user': current_user, 'profile': profile})
