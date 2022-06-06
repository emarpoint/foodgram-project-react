"""
Создание корневого маршрутизатора Foodgram проекта.
Creating the root router of the Foodgram project.
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]


