from datetime import datetime, timedelta, date

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from plotly.offline import plot
import plotly.graph_objects as go

from vaccination.forms import RegisterCitizenForm, RegisterUserForm, SchedulingForm
from vaccination.models import Citizen, Scheduling, SchedulingCitizen, Vaccine


@login_required
def index(request):
    return render(request, 'vaccination/index.html')


def home(request):
    graphs = []

    labels = []
    values = []

    manufacturers = Vaccine.objects.order_by().values_list('manufacturer', flat=True).distinct()
    for manufacturer in manufacturers:
        num_schedulings = SchedulingCitizen.objects.filter(scheduling__vaccine__manufacturer=manufacturer).count()
        if num_schedulings > 0:
            labels.append(manufacturer)
            values.append(num_schedulings)

    graphs.append(go.Pie(labels=labels, values=values, text=values, textinfo='label+percent', textposition='outside'))

    labels = []
    values = []

    today = datetime.now()
    six_days_ago = today - timedelta(days=6)
    days = [six_days_ago + timedelta(days=i) for i in range(0, 7)]

    for day in days:
        labels.append(day.strftime("%d/%m"))
        num_schedulings = SchedulingCitizen.objects.filter(date=day).count()
        values.append(num_schedulings)

    graphs.append(go.Bar(x=labels, y=values, text=values, textposition='outside'), )

    layout_fabricantes = {
        'title': 'Agendamentos por fabricante',
        'height': 460,
        'width': 550,
    }

    layout_agendamentos = {
        'title': 'Agendamentos por dia',
        'height': 460,
        'width': 550,
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'yaxis': {'visible': False, },
    }

    fabricantes = plot({'data': graphs[0], 'layout': layout_fabricantes}, output_type='div')
    agendamentos = plot({'data': graphs[1], 'layout': layout_agendamentos}, output_type='div')

    return render(request, 'vaccination/index.html',
                  context={'fabricantes': fabricantes, 'agendamentos': agendamentos})


@login_required
def voucher(request):
    scheduling_citizen = SchedulingCitizen.objects.filter(citizen__user=request.user)
    if scheduling_citizen.exists():
        return render(request, 'vaccination/voucher.html', {'scheduling_citizen': scheduling_citizen.first()})
    else:
        messages.info(request, "Não foi realizado nenhum agendamento.")
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
                schedulings = Scheduling.objects.filter(date=date, group=group, center__city=city,
                                                        num_available_vacancies__gt=0)
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
                        scheduling_citizen = SchedulingCitizen.objects.create(scheduling=scheduling,
                                                                              citizen=request.user.citizen)
                        scheduling.change_num_vacancies(-1)
                        scheduling.save(force_update=True)
                    return redirect('voucher')
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
