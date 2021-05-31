# Generated by Django 3.2.3 on 2021-05-31 03:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('min_age', models.IntegerField(verbose_name='Idade mínima')),
            ],
            options={
                'verbose_name': 'Grupo de Atendimento',
                'verbose_name_plural': 'Grupos de Atendimento',
                'ordering': ['-min_age'],
            },
        ),
        migrations.CreateModel(
            name='VaccinationCenter',
            fields=[
                ('cnes', models.IntegerField(primary_key=True, serialize=False, verbose_name='CNES')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('address', models.CharField(max_length=200, verbose_name='Logradouro')),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Bairro')),
                ('city', models.CharField(max_length=200, verbose_name='Cidade')),
            ],
            options={
                'verbose_name': 'Local de Vacinação',
                'verbose_name_plural': 'Locais de Vacinação',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(verbose_name='Data de nascimento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cidadão',
                'verbose_name_plural': 'Cidadãos',
            },
        ),
    ]
