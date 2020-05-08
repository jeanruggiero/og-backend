from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('patients/id', views.patient_id),
    #path('patients/<str:id>/', views.update_patient),
    path('intake', views.new_intake),
    path('intake/<str:id>/', views.update_intake),
]
