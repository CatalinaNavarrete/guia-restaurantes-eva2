from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Restaurante(models.Model):

    # Opciones permitidas para la calificación del restaurante
    CALIFICACION_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]

    # Nombre del restaurante
    nombre = models.CharField(max_length=200)

    # Tipo de comida que ofrece
    tipo_comida = models.CharField(max_length=100)

    # Calificación entre 1 y 5 estrellas
    calificacion = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        default=3
    )

    # Indica si el restaurante está abierto o cerrado
    abierto = models.BooleanField(default=True)

    # Fecha en que el usuario visitó el restaurante
    fecha_visita = models.DateField(
        null=True,
        blank=True
    )

    # Capacidad máxima de personas del restaurante
    # El valor 20 se usa también para restaurantes que ya existían
    capacidad = models.PositiveIntegerField(
        default=20
    )

    # Usuario propietario o creador del restaurante
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='restaurantes',
    )

    # Define cómo se muestra el restaurante en el administrador de Django
    def __str__(self):
        return self.nombre

    class Meta:
        # Ordena los restaurantes desde la mayor calificación a la menor
        ordering = ['-calificacion']


class Reserva(models.Model):

    # Estados posibles de una reserva
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    # Usuario que realiza la reserva
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    # Restaurante donde se realiza la reserva
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    # Día de la reserva
    fecha = models.DateField()

    # Hora de la reserva
    hora = models.TimeField()

    # Cantidad de personas que asistirán
    # MinValueValidator(1) evita reservas de 0 personas
    cantidad_personas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    # Estado actual de la reserva
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    # Comentario adicional del cliente
    # blank=True significa que este campo es opcional
    nota = models.TextField(
        blank=True
    )

    # Define cómo aparece la reserva en el administrador de Django
    def __str__(self):
        return f'{self.restaurante.nombre} - {self.usuario.username}'

    class Meta:
        # Ordena las reservas primero por fecha y luego por hora
        ordering = ['fecha', 'hora']