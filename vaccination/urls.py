from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('cadastrar/', views.register, name='register', ),
    path('entrar/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="auth-login", ),
    path('sair/', auth_views.LogoutView.as_view(), name="auth-logout"),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('agendar/', views.scheduling, name='scheduling'),
    path('voucher/', views.voucher, name='voucher'),
]
