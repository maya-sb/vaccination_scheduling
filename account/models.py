from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password

from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        user = self.model(email=self.normalize_email(email), name=name,)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", unique=True)
    name = models.CharField(verbose_name="Nome completo", max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, verbose_name="Administrador")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['name']
