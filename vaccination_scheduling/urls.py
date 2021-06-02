from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('', include('vaccination.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
    url(r'^chaining/', include('smart_selects.urls'))
]
