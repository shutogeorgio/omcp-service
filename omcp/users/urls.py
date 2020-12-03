from django.urls import path
from . import views

urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('signup/patient/', views.patient_signup.as_view(), name='patient_signup'),
     path('signup/doctor/', views.doctor_signup.as_view(), name='doctor_signup'),
     path('login/', views.login_request, name='login'),
     path('logout/', views.logout_view, name='logout'),
]