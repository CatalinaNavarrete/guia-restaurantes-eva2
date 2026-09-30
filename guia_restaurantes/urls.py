from django.contrib import admin
from django.urls import path
from restaurantes import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'restaurantes/',
        views.listar_restaurantes,
        name='listar_restaurantes'
    ),
]