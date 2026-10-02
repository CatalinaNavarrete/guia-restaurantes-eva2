from django.contrib import admin
from django.urls import path, include
from restaurantes import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

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
]