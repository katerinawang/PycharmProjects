"""hyperjob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from resume.views import menu, resumes, SignupView, Login
from django.contrib.auth.views import LogoutView
from vacancy.views import vacancies, UserValidView, new_vacancy, new_resume

urlpatterns = [
    path('', menu),
    path('admin/', admin.site.urls),
    path('resumes', resumes),
    path('vacancies', vacancies),
    path('vacancy/new', new_vacancy),
    path('resume/new', new_resume),
    path('home', UserValidView.as_view()),
    path('signup', SignupView.as_view()),
    path('login', Login.as_view()),
    path('logout', LogoutView.as_view())
]
