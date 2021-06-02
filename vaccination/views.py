from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from vaccination.forms import RegisterCitizenForm, RegisterUserForm, SchedulingForm
from vaccination.models import Citizen, Scheduling, SchedulingCitizen


@login_required
def index(request):
    return render(request, 'vaccination/home.html')


def home(request):
    return render(request, 'vaccination/home.html')


@login_required
def voucher(request, id):
    scheduling_citizen = SchedulingCitizen.objects.filter(citizen__user=request.user, pk=id)
    if scheduling_citizen.exists():
        return render(request, 'vaccination/voucher.html', {'scheduling_citizen': scheduling_citizen.first()})
    else:
        messages.error(request, "Usuário sem permissão.")
        return redirect('index')

@login_required
def scheduling(request):
    form = SchedulingForm(request.user)
    resul = {}
    date = ""

    if request.method == "POST":
        if 'consultar' in request.POST:
            form = SchedulingForm(request.user, request.POST)
            if form.is_valid():
                date = datetime.strptime(form.cleaned_data.get('date'), '%Y-%m-%d').date()
                city = form.cleaned_data.get('city')
                group = form.cleaned_data.get('service_group')
                schedulings = Scheduling.objects.filter(date=date, group=group, center__city=city, num_available_vacancies__gt=0)
                locals = {}
                for sche in schedulings:
                    locals[sche.center.name] = []
                for sche in schedulings:
                    locals[sche.center.name].append(sche)
                if locals == {}:
                    messages.info(request, "Não há horários para os filtros selecionados.")
                resul = locals

        elif 'agendar' in request.POST:
            id_scheduling = request.POST.get('options')
            if id_scheduling:
                scheduling = Scheduling.objects.get(pk=int(id_scheduling))
                if SchedulingCitizen.objects.filter(citizen=request.user.citizen).exists():
                    messages.error(request, "Não é possível realizar mais de um agendamento por usuário!")
                else:
                    with transaction.atomic():
                        scheduling_citizen = SchedulingCitizen.objects.create(scheduling=scheduling, citizen=request.user.citizen)
                        scheduling.change_num_vacancies(-1)
                        scheduling.save(force_update=True)
                    return redirect('voucher', id=scheduling_citizen.id)
            else:
                messages.info(request, "Selecione algum horário para agendamento.")

    return render(request, 'vaccination/scheduling.html', {'form': form, 'resul': resul, 'date': date})


def register(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form_user = RegisterUserForm(request.POST)
        form_citizen = RegisterCitizenForm(request.POST)

        if form_user.is_valid() and form_citizen.is_valid():
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
