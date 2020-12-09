from django.urls import path
from . import views

urlpatterns = [
    path('diagnoses/', views.list_diagnosis, name='list_diagnosis'),
    path('diagnoses/create', views.create_diagnosis, name='create_diagnosis'),
    path('diagnoses/personal', views.list_own_diagnosis, name='list_own_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/', views.desc_diagnosis, name='desc_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/register', views.register_diagnosis, name='register_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/complete', views.complete_diagnosis, name='complete_diagnosis'),
    path('diagnoses/<int:diagnosis_id>/summary', views.desc_summary, name='desc_summary'),
    path('diagnoses/<int:diagnosis_id>/summary/create', views.create_summary, name='create_summary'),
]