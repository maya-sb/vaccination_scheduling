from django.contrib import admin

from vaccination.models import *


class RoomInline(admin.TabularInline):
    model = Room
    extra = 3


@admin.register(VaccinationCenter)
class VaccinationCenterAdmin(admin.ModelAdmin):
    model = VaccinationCenter
    list_display = ('name', 'cnes', 'city', 'neighborhood', 'address')
    search_fields = ('name', 'city')
    inlines = [RoomInline]


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    model = ServiceGroup
    list_display = ('name', 'min_age')


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    model = Vaccine
    list_display = ('name', 'manufacturer')


class VaccinationCenterInline(admin.TabularInline):
    model = VaccinationCenter
    extra = 3


class RoomSchedulingInline(admin.TabularInline):
    model = RoomScheduling
    extra = 3
    fields = ('num_vacancies', 'room__name', )
    inlines = [VaccinationCenterInline]


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    model = Scheduling
    inlines = [RoomSchedulingInline]
    list_display = ('__str__', 'get_total_vacancies', 'get_available_vacancies', 'vaccine', 'group')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ('name', 'center',)


admin.site.register(Citizen)
# admin.site.site_header = "Sistema de Vacinação LAIS"
# admin.site.site_title = "Vacinação LAIS"
# admin.site.index_title = "Administração"
