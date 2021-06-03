from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('vaccination.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/vaccination/')),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]
