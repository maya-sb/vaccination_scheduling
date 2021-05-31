from django.contrib import admin
from vaccination.models import VaccinationCenter, ServiceGroup, Citizen


@admin.register(VaccinationCenter)
class VaccinationCenterAdmin(admin.ModelAdmin):
    model = VaccinationCenter
    list_display = ('name', 'cnes', 'city', 'neighborhood', 'address')
    search_fields = ('name', 'city')


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    model = ServiceGroup
    list_display = ('name', 'min_age')


admin.site.register(Citizen)
#admin.site.site_header = "Sistema de Vacinação LAIS"
#admin.site.site_title = "Vacinação LAIS"
#admin.site.index_title = "Administração"