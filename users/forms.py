from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'is_staff', 'password')


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Senha',
        help_text=("<a href=\"../password/\">Altere a senha aqui</a>"))
    class Meta:
        model = User
        fields = ('name', 'email', 'is_staff', 'password')
