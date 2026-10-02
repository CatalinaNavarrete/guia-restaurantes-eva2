from django.contrib import admin
from django.urls import path, include
from restaurantes import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),

    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    path(
        'restaurantes/',
        views.listar_restaurantes,
        name='listar_restaurantes'
    ),

    path(
        'restaurantes/nuevo/',
        views.crear_restaurante,
        name='crear_restaurante'
    ),

    path(
        'restaurantes/<int:pk>/editar/',
        views.editar_restaurante,
        name='editar_restaurante'
    ),

    path(
        'restaurantes/<int:pk>/eliminar/',
        views.eliminar_restaurante,
        name='eliminar_restaurante'
    ),

    path(
        'restaurantes/<int:pk>/reservar/',
        views.reservar_restaurante,
        name='reservar_restaurante'
    ),

    path(
        'mis-reservas/',
        views.mis_reservas,
        name='mis_reservas'
    ),

    path(
        'restaurantes/<int:pk>/',
        views.detalle_restaurante,
        name='detalle_restaurante'
    ),
]