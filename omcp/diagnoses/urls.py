from django.urls import path
from . import views

urlpatterns = [
    path('diagnoses/', views.list_diagnosis, name='list_diagnosis'),
    path('diagnoses/create', views.create_diagnosis, name='create_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/', views.desc_diagnosis, name='desc_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/register', views.register_diagnosis, name='register_diagnosis'),
]