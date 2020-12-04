from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('signup/', views.signup, name='signup'),
     path('signup/patient/', views.patient_signup.as_view(), name='signup_patient'),
     path('signup/doctor/', views.doctor_signup.as_view(), name='signup_doctor'),
     path('login/', views.login_request, name='login'),
     path('logout/', views.logout_view, name='logout'),
]