"""
URL configuration for Backend_Server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from core.views import mark_attendance_api, add_student_api, start_session_api

# Simple homepage view
def home(request):
    return HttpResponse("<h1>Backend Server is Running! </h1><p>Go to <a href='/admin'>/admin</a> to login.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mark_attendance/', mark_attendance_api),
    path('', home),
    path('api/start_session/', start_session_api), # This handles the empty homepage
    path('api/add_student/', add_student_api),
]
