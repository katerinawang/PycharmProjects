from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Vacancy
from resume.models import Resume
from django.views import View
from django.forms import ModelForm


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['description']


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['description']


# Create your views here.
def vacancies(request):
    return render(request, 'vacancies.html', context={'vacancies': Vacancy.objects.all()})


class UserValidView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            link = 'vacancy/new'
            name = 'New Vacancy: '
            form = VacancyForm()
        elif request.user.is_authenticated:
            link = 'resume/new'
            name = 'New Resume: '
            form = ResumeForm()
        else:
            link = None
            name = None
            form = None
        return render(request, 'home.html', context={'link': link, 'name': name, 'form': form})


def new_vacancy(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    else:
        form = VacancyForm(request.POST)
        if form.is_valid():
            obj = Vacancy()
            obj.author = request.user
            obj.description = form.cleaned_data['description']
            obj.save()
            return redirect('/home', {'form': form})
        else:
            form = VacancyForm()
        return render(request, 'home.html', {'form': form})


def new_resume(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return HttpResponseForbidden()
    else:
        form = ResumeForm(request.POST)
        if form.is_valid():
            obj = Resume()
            obj.author = request.user
            obj.description = form.cleaned_data['description']
            obj.save()
            return redirect('/home', {'form': form})
        else:
            form = ResumeForm()
        return render(request, 'home.html', {'form': form})
