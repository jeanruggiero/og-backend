"""og_backend URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include('intake.urls')),
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_auth_token),
]
