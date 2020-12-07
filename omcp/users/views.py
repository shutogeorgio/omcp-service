from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from .forms import PatientSignUpForm, DoctorSignUpForm, PatientProfileForm, DoctorProfileForm, LicenseReForm
from django.contrib.auth.forms import AuthenticationForm

from .license import License
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
    template_path = '../frontend/login.html'
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
def desc_profile(request, profile_id):
    req_user = get_object_or_404(User, id=profile_id)
    template_path = '../frontend/profile/desc.html'
    if req_user.is_patient:
        profile = get_object_or_404(Patient, user_id=req_user.id)
    elif req_user.is_doctor:
        profile = Doctor.objects.get(user_id=req_user.id)
    else:
        profile = ''
    return render(request, template_path, context={'user': req_user, 'profile': profile})


def update_profile(request, profile_id):
    req_user = get_object_or_404(User, id=profile_id)
    template_path = '../frontend/profile/edit.html'

    if req_user.is_patient:
        profile = get_object_or_404(Patient, user_id=req_user.id)
        form = PatientProfileForm(request.POST or None,
                                  request.FILES or None, instance=profile)
        context = {'user': req_user, 'profile': profile, 'form': form}
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect("/profile/{}".format(req_user.id))

    elif req_user.is_doctor:
        profile = get_object_or_404(Doctor, user_id=req_user.id)
        cert = get_object_or_404(License, doctor_id=req_user.id)
        form = DoctorProfileForm(request.POST or None,
                                 request.FILES or None, instance=profile)
        context = {'user': req_user, 'profile': profile, 'form': form, 'license': cert}
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect("/profile/{}".format(req_user.id))
    else:
        redirect('/login')

    return render(request, template_path, context=context)


# License Configuration
def desc_license(request):
    current_user = request.user
    template_path = '../frontend/license/desc.html'
    if current_user.is_patient:
        redirect('/')
    elif current_user.is_doctor:
        profile = get_object_or_404(Doctor, user_id=current_user.id)
        cert = get_object_or_404(License, doctor_id=current_user.id)
    else:
        redirect('/login')
    return render(request, template_path,
                  context={'user': current_user, 'profile': profile, 'license': cert})

def update_license(request):
    current_user = request.user
    template_path = '../frontend/license/edit.html'
    if current_user.is_patient:
        redirect('/')
    elif current_user.is_doctor:
        profile = get_object_or_404(Doctor, user_id=current_user.id)
        cert = get_object_or_404(License, doctor_id=current_user.id)
        form = LicenseReForm(request.POST,
                             request.FILES, instance=cert)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect("/profile/{}".format(current_user.id))
    else:
        redirect('/login')
    return render(request, template_path, context={'user': current_user, 'profile': profile, 'license': cert, 'form': form})
