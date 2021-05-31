from django import forms
from django.forms import ModelForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import Citizen
from account.models import User


class RegisterCitizenForm(ModelForm):
    class Meta:
        model = Citizen
        exclude = ('user', )


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email')

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(label='Confirmação da senha', widget=forms.PasswordInput(render_value=True))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação de senha não confere.')
        return password1

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email já está sendo utilizado.'})
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
