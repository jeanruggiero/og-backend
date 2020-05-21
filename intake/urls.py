from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('patients/id', views.patient_id),
    #path('patients/<str:id>/', views.update_patient),
    path('intake', views.new_intake),
    path('intake/<str:id>/', views.update_intake),
    path('appointment_request/', views.appointment_request),
    path('forms/', views.form_list),
    path('forms/<str:id>/', views.form_detail)
]
