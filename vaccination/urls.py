import django.contrib.auth.views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('register/', views.register, name='register', ),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="auth-login", ),
    path('logout/', auth_views.LogoutView.as_view(), name="auth-logout"),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('agendar/', views.scheduling, name='scheduling'),
    path('voucher/<int:id>', views.voucher, name='voucher'),

    path('teste/', TemplateView.as_view(template_name="vaccination/base-home.html")),
]
