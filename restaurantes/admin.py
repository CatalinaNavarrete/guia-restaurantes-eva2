from django.contrib import admin
from django.db.models import Avg
from django.utils import timezone

from .models import (
    Restaurante,
    Reserva,
    Resena,
    Horario,
    Promocion,
    Foto,
)


# ---------------------------------------------------------
# RESTAURANTES
# ---------------------------------------------------------

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):

    # Columnas visibles en el listado del administrador
    list_display = (
        'nombre',
        'ciudad',
        'tipo_comida',
        'calificacion',
        'calificacion_promedio',
        'capacidad',
        'abierto',
        'tiene_promocion_activa',
        'usuario',
    )

    # Permite buscar restaurantes por estos campos
    search_fields = (
        'nombre',
        'tipo_comida',
        'ciudad',
        'direccion',
        'usuario__username',
    )

    # Filtros laterales
    list_filter = (
        'ciudad',
        'tipo_comida',
        'calificacion',
        'abierto',
        'usuario',
    )

    # Calcula el promedio de las reseñas relacionadas
    @admin.display(description='Promedio reseñas')
    def calificacion_promedio(self, obj):
        promedio = obj.resenas.aggregate(
            promedio=Avg('puntuacion')
        )['promedio']

        if promedio is None:
            return 'Sin reseñas'

        return round(promedio, 1)

    # Indica si existe una promoción vigente
    @admin.display(
        boolean=True,
        description='Promoción activa'
    )
    def tiene_promocion_activa(self, obj):
        hoy = timezone.localdate()

        return obj.promociones.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).exists()

    # Superusuario ve todos.
    # Staff normal solamente ve sus restaurantes.
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            usuario=request.user
        )

    # Cuando un staff crea un restaurante desde Admin,
    # se asigna automáticamente como propietario.
    def save_model(self, request, obj, form, change):

        if not change and not obj.usuario:
            obj.usuario = request.user

        super().save_model(
            request,
            obj,
            form,
            change
        )

    # El usuario normal no puede cambiar el propietario.
    def get_exclude(self, request, obj=None):

        if request.user.is_superuser:
            return ()

        return ('usuario',)


# ---------------------------------------------------------
# CLASE BASE PARA MODELOS RELACIONADOS CON RESTAURANTE
# ---------------------------------------------------------

class RestauranteRelacionadoAdmin(admin.ModelAdmin):
    """
    Los usuarios staff solamente pueden trabajar con
    información perteneciente a sus propios restaurantes.
    El superusuario puede ver todo.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            restaurante__usuario=request.user
        )

    # También limita los restaurantes disponibles
    # en los formularios del administrador.
    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs
    ):
        if (
            db_field.name == 'restaurante'
            and not request.user.is_superuser
        ):
            kwargs['queryset'] = (
                Restaurante.objects.filter(
                    usuario=request.user
                )
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )


# ---------------------------------------------------------
# RESERVAS
# ---------------------------------------------------------

@admin.register(Reserva)
class ReservaAdmin(RestauranteRelacionadoAdmin):

    list_display = (
        'restaurante',
        'usuario',
        'fecha',
        'hora',
        'cantidad_personas',
        'estado',
    )

    search_fields = (
        'restaurante__nombre',
        'usuario__username',
        'usuario__email',
    )

    list_filter = (
        'estado',
        'fecha',
        'restaurante',
    )


# ---------------------------------------------------------
# RESEÑAS
# ---------------------------------------------------------

@admin.register(Resena)
class ResenaAdmin(RestauranteRelacionadoAdmin):

    list_display = (
        'restaurante',
        'usuario',
        'puntuacion',
        'fecha_visita',
        'util_count',
    )

    search_fields = (
        'restaurante__nombre',
        'usuario__username',
        'texto',
    )

    list_filter = (
        'puntuacion',
        'fecha_visita',
        'restaurante',
    )


# ---------------------------------------------------------
# HORARIOS
# ---------------------------------------------------------

@admin.register(Horario)
class HorarioAdmin(RestauranteRelacionadoAdmin):

    list_display = (
        'restaurante',
        'dia_semana',
        'hora_apertura',
        'hora_cierre',
        'cerrado',
    )

    search_fields = (
        'restaurante__nombre',
    )

    list_filter = (
        'dia_semana',
        'cerrado',
        'restaurante',
    )


# ---------------------------------------------------------
# PROMOCIONES
# ---------------------------------------------------------

@admin.register(Promocion)
class PromocionAdmin(RestauranteRelacionadoAdmin):

    list_display = (
        'titulo',
        'restaurante',
        'descuento',
        'fecha_inicio',
        'fecha_fin',
        'promocion_activa',
    )

    search_fields = (
        'titulo',
        'restaurante__nombre',
        'descripcion',
    )

    list_filter = (
        'fecha_inicio',
        'fecha_fin',
        'restaurante',
    )

    @admin.display(
        boolean=True,
        description='Activa'
    )
    def promocion_activa(self, obj):
        hoy = timezone.localdate()

        return (
            obj.fecha_inicio <= hoy
            <= obj.fecha_fin
        )


# ---------------------------------------------------------
# FOTOS
# ---------------------------------------------------------

@admin.register(Foto)
class FotoAdmin(RestauranteRelacionadoAdmin):

    list_display = (
        'restaurante',
        'descripcion',
    )

    search_fields = (
        'restaurante__nombre',
        'descripcion',
    )

    list_filter = (
        'restaurante',
    )