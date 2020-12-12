from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView

from .decorators import license_mods_eligibility, allowed_users, unauthenticated_user
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


def privacy_policy(request):
    template_path = '../frontend/terms.html'
    title = 'Privacy Policy'
    content = 'We may use such information in the following ways To personalize your experience on our site and to allow us to deliver the type of content and product offerings in which you are most interested.To improve our website in order to better serve you.To allow us to better service you in responding to your customer service requests.To administer a contest, promotion, survey or other site feature.To quickly process your transactions.To send periodic emails regarding your order or other products and services.'
    return render(request, template_path, context={'title': title, 'content': content})


def terms_use(request):
    template_path = '../frontend/terms.html'
    title = 'Terms and Condition'
    content = 'Harassment in any manner or form on the site, including via e-mail, chat, or by use of obscene or abusive language, is strictly forbidden. Impersonation of others, including a omcp.onejapanesedev.com or other licensed employee, host, or representative, as well as other members or visitors on the site is prohibited. You may not upload to, distribute, or otherwise publish through the site any content which is libelous, defamatory, obscene, threatening, invasive of privacy or publicity rights, abusive, illegal, or otherwise objectionable which may constitute or encourage a criminal offense, violate the rights of any party or which may otherwise give rise to liability or violate any law. You may not upload commercial content on the site or use the site to solicit others to join or become members of any other commercial online service or other organization.'
    return render(request, template_path, context={'title': title, 'content': content})


# Login & Signup Logic
@unauthenticated_user
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
    user = request.user
    template_path = '../frontend/profile/desc.html'
    profile_owner = False
    if user.is_patient:
        profile = get_object_or_404(Patient, user_id=profile_id)
        if profile.user_id == user.id:
            profile_owner = True
    elif user.is_doctor:
        profile = Doctor.objects.get(user_id=profile_id)
        if profile.user_id == user.id:
            profile_owner = True
    else:
        profile = ''
    return render(request, template_path, context={'user': user, 'profile': profile, 'profile_owner': profile_owner})


def update_profile(request, profile_id):
    user = request.user
    template_path = '../frontend/profile/edit.html'
    license_eligibility = False
    if user.is_patient:
        profile = get_object_or_404(Patient, user_id=profile_id)
        form = PatientProfileForm(request.POST or None,
                                  request.FILES or None, instance=profile)
        context = {'user': user, 'profile': profile, 'form': form, 'license_eligibility': license_eligibility}

        if user.id == profile_id:
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect("/profile/{}".format(profile_id))
                return redirect("/profile/{}".format(profile_id))

    elif user.is_doctor:
        profile = get_object_or_404(Doctor, user_id=profile_id)
        cert = get_object_or_404(License, doctor_id=profile_id)
        form = DoctorProfileForm(request.POST or None,
                                 request.FILES or None, instance=profile)
        if user.id == profile_id:
            if cert.doctor.validity == 'IN_REVIEW':
                license_eligibility = True
        context = {'user': user, 'profile': profile, 'form': form, 'license': cert, 'license_eligibility': license_eligibility}

        if user.id == profile_id:
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect("/profile/{}".format(user.id))
    else:
        return redirect('/login')

    return render(request, template_path, context=context)


# License Configuration
def desc_license(request):
    current_user = request.user
    template_path = '../frontend/license/desc.html'
    if current_user.is_patient:
        redirect('/diagnoses/')
    elif current_user.is_doctor:
        profile = get_object_or_404(Doctor, user_id=current_user.id)
        cert = get_object_or_404(License, doctor_id=current_user.id)
    else:
        redirect('/login')
    return render(request, template_path,
                  context={'user': current_user, 'profile': profile, 'license': cert})


@license_mods_eligibility
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
    return render(request, template_path,
                  context={'user': current_user, 'profile': profile, 'license': cert, 'form': form})


def error_404(request, exception, template_name='../frontend/400.html'):
    return render(request, template_name, status=404)


def error_500(request, *args, **argv):
    template_path = '../frontend/500.html'
    return render(request, template_path, status=500)
