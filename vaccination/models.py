from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class VaccinationCenter(models.Model):
    cnes = models.IntegerField(primary_key=True, verbose_name='CNES')
    name = models.CharField(max_length=200, verbose_name='Nome')
    address = models.CharField(max_length=200, verbose_name='Logradouro')
    neighborhood = models.CharField(max_length=200, verbose_name='Bairro')
    city = models.CharField(max_length=200, verbose_name='Cidade')

    class Meta:
        verbose_name = 'Local de Vacinação'
        verbose_name_plural = 'Locais de Vacinação'
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    min_age = models.IntegerField(verbose_name="Idade mínima")

    class Meta:
        verbose_name = 'Grupo de Atendimento'
        verbose_name_plural = 'Grupos de Atendimento'
        ordering = ['-min_age']

    def __str__(self):
        return f'{self.name}'


class Citizen(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(verbose_name='Data de nascimento')

    def get_age(self):
        return (date.today() - self.birth_date) // timedelta(days=365.2425)

    get_age.short_description = 'Idade'

    class Meta:
        verbose_name = 'Cidadão'
        verbose_name_plural = 'Cidadãos'

    def __str__(self):
        return self.user.name
