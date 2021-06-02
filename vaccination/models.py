from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum


class VaccinationCenter(models.Model):
    cnes = models.IntegerField(primary_key=True, verbose_name='CNES')
    name = models.CharField(max_length=200, verbose_name='Nome')
    address = models.CharField(max_length=200, verbose_name='Logradouro')
    neighborhood = models.CharField(max_length=200, verbose_name='Bairro')
    city = models.CharField(max_length=200, verbose_name='Cidade')

    class Meta:
        verbose_name = 'Local de Vacinação'
        verbose_name_plural = 'Locais de Vacinação'
        ordering = ['city', 'name']

    def __str__(self):
        return f'{self.city} - {self.name}'


class ServiceGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    min_age = models.IntegerField(verbose_name="Idade mínima")

    class Meta:
        verbose_name = 'Grupo de Atendimento'
        verbose_name_plural = 'Grupos de Atendimento'
        ordering = ['-min_age']

    def __str__(self):
        return f'{self.name} - {self.min_age} anos'


class Citizen(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citizen')
    birth_date = models.DateField(verbose_name='Data de nascimento')

    def get_age(self):
        return (date.today() - self.birth_date) // timedelta(days=365.2425)

    get_age.short_description = 'Idade'

    class Meta:
        verbose_name = 'Cidadão'
        verbose_name_plural = 'Cidadãos'

    def __str__(self):
        return self.user.name


class Vaccine(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=200)
    manufacturer = models.CharField(verbose_name='Fabricante', max_length=200)

    class Meta:
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Scheduling(models.Model):
    date = models.DateField(verbose_name='Data')
    slot = models.TimeField(verbose_name='Horário')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, verbose_name='Vacina')
    group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, verbose_name='Grupo de Atendimento')
    num_vacancies = models.IntegerField(verbose_name='Vagas')
    num_available_vacancies = models.IntegerField(verbose_name='Vagas disponíveis')
    center = models.ForeignKey(VaccinationCenter, verbose_name='Local', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-date']

    def change_num_vacancies(self, vacancies):
        self.num_available_vacancies += vacancies

    def __str__(self):
        return f'{self.vaccine.name} - {self.center}'


class SchedulingCitizen(models.Model):
    STATUS_CHOICES = (
        ('a', 'Agendado'),
        ('v', 'Vacinado'),
        ('c', 'Cancelado'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=200, default='a')
    scheduling = models.ForeignKey(Scheduling, verbose_name='Agendamento', on_delete=models.CASCADE)
    citizen = models.OneToOneField(Citizen, verbose_name='Cidadão', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Agendamento-Cidadão'
        verbose_name_plural = 'Agendamentos-Cidadãos'


#Scheduling.objects.filter(date=datetime.date(2021,6,1), group__id='6', roomscheduling__room__center__city='Aracaju').distinct()
