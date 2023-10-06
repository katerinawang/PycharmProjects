from django.shortcuts import render
from .models import Resume
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

links = ['login', 'logout', 'signup', 'vacancies', 'resumes', 'home']


# Create your views here.
def menu(request):
    return render(request, 'main.html', context={'links': links})


def resumes(request):
    return render(request, 'resume.html', context={'resumes': Resume.objects.all()})


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'signup.html'


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
