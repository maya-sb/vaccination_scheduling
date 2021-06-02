from django.contrib import admin
from django_plotly_dash.models import DashAppAdmin

from vaccination.models import VaccinationCenter, ServiceGroup, Citizen, Vaccine, Scheduling, SchedulingCitizen


@admin.register(VaccinationCenter)
class VaccinationCenterAdmin(admin.ModelAdmin):
    model = VaccinationCenter
    list_display = ('name', 'cnes', 'city', 'neighborhood', 'address')
    search_fields = ('name', 'city')


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    model = ServiceGroup
    list_display = ('id', 'name', 'min_age')


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    model = Vaccine
    list_display = ('name', 'manufacturer')


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    model = Scheduling
    list_display = ('vaccine', 'date', 'slot', 'group', 'num_vacancies', 'num_available_vacancies', 'center',)


admin.site.register(Citizen)
admin.site.register(SchedulingCitizen)
#admin.site.unregister(DashAppAdmin)
# admin.site.site_header = "Sistema de Vacinação LAIS"
# admin.site.site_title = "Vacinação LAIS"
# admin.site.index_title = "Administração"
