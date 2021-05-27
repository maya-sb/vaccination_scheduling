from django.db import models


class VaccinationCenter(models.Model):
    cnes = models.IntegerField(primary_key=True, verbose_name='CNES')
    name = models.CharField(max_length=200, verbose_name='Nome')
    address = models.CharField(max_length=200, verbose_name='Logradouro')
    neighborhood = models.CharField(max_length=200, verbose_name='Bairro')
    city = models.CharField(max_length=200, verbose_name='Cidade')

    class Meta:
        verbose_name = 'Local de Vacinação'
        verbose_name_plural = 'Locais de Vacinação'
        ordering = ['name', 'city']


class ServiceGroup(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    min_age = models.IntegerField(verbose_name="Idade mínima")

    class Meta:
        verbose_name = 'Grupo de Atendimento'
        verbose_name_plural = 'Grupos de Atendimento'
        ordering = ['-min_age']
