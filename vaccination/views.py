from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from vaccination.forms import RegisterCitizenForm, RegisterUserForm
from vaccination.models import Citizen

@login_required
def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'vaccination/home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form_user = RegisterUserForm(request.POST)
        form_citizen = RegisterCitizenForm(request.POST)

        if form_user.is_valid() and form_citizen.is_valid():
            print(form_user)
            user = form_user.save()
            citizen = Citizen(user=user, birth_date=form_citizen.cleaned_data['birth_date'])
            citizen.save()
            password = form_user.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=password)
            auth_login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
    else:
        form_user = RegisterUserForm()
        form_citizen = RegisterCitizenForm()

    return render(request, 'registration/register.html', {'form_user': form_user, 'form_citizen': form_citizen})