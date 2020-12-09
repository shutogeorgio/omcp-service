from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('privacy-policy', views.privacy_policy, name='privacy_policy'),
     path('terms-use', views.terms_use, name='terms_use'),
     path('signup/', views.signup, name='signup'),
     path('profile/<int:profile_id>/', views.desc_profile, name='profile_desc'),
     path('profile/<int:profile_id>/edit/', views.update_profile, name='profile_update'),
     path('license/', views.desc_license, name='license_desc'),
     path('license/edit/', views.update_license, name='license_update'),
     path('signup/patient/', views.patient_signup.as_view(), name='signup_patient'),
     path('signup/doctor/', views.doctor_signup.as_view(), name='signup_doctor'),
     path('login/', views.login_request, name='login'),
     path('logout/', views.logout_view, name='logout'),
]