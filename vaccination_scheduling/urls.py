from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('vaccination.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
]
