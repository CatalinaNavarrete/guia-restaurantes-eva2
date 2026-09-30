from django.contrib import admin
from .models import Restaurante


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista de restaurantes
    list_display = ('nombre', 'tipo_comida', 'calificacion', 'abierto', 'fecha_visita')

    # Barra de búsqueda: busca por estos campos
    search_fields = ('nombre', 'tipo_comida')

    # Filtros laterales
    list_filter = ('tipo_comida', 'calificacion', 'abierto', 'fecha_visita')