import django.contrib.auth.views
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register', ),
    path('', views.index, name='index'),
    path('agendar/', views.scheduling, name='scheduling'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="auth-login", ),
    path('logout/', auth_views.LogoutView.as_view(), name="auth-logout"),
]
