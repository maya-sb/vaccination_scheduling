from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email já está sendo utilizado.'})
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

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

    def clean_password(self):
        return self.initial['password']
