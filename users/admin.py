from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('name', 'email', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissões', {'fields': ('is_staff',)})
    )
    add_fieldsets = (
        (None,
         {'fields': ('name', 'email', 'password')}),
        ('Permissões', {'fields': ('is_staff',)})
    )
    search_fields = ['email', 'name']
    filter_horizontal = ()
    ordering = ['name']


admin.site.register(User, UserAdmin)



