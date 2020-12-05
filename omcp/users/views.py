from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PatientSignUpForm, DoctorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User


def home(request):
    return render(request, '../frontend/index.html')


def signup(request):
    return render(request, '../frontend/signup/index.html')


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
    return render(request, '../frontend/login.html',
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')
