from django.contrib import admin
from .models import Restaurante


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista de restaurantes
    list_display = ('nombre', 'tipo_comida', 'calificacion', 'abierto', 'fecha_visita', 'usuario')

    # Barra de búsqueda: busca por estos campos
    search_fields = ('nombre', 'tipo_comida')

    # Filtros laterales
    list_filter = ('tipo_comida', 'calificacion', 'abierto', 'fecha_visita', 'usuario')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not change and not obj.usuario:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return ('usuario',)