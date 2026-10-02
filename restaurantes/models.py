from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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

    # Descripción general del restaurante
    descripcion = models.TextField(
        blank=True
    )

    # Tipo de comida que ofrece
    tipo_comida = models.CharField(
        max_length=100
    )

    # Ciudad donde se encuentra
    ciudad = models.CharField(
        max_length=100,
        blank=True
    )

    # Dirección física
    direccion = models.CharField(
        max_length=255,
        blank=True
    )

    # Teléfono de contacto
    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    # Calificación entre 1 y 5 estrellas
    calificacion = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        default=3
    )

    # Indica si el restaurante está abierto o cerrado
    abierto = models.BooleanField(
        default=True
    )

    # Fecha en que el usuario visitó el restaurante
    fecha_visita = models.DateField(
        null=True,
        blank=True
    )

    # Capacidad máxima del restaurante
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

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-calificacion']


class Reserva(models.Model):

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

    # Restaurante reservado
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    fecha = models.DateField()

    hora = models.TimeField()

    # Impide reservas para 0 personas
    cantidad_personas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    nota = models.TextField(
        blank=True
    )

    def __str__(self):
        return f'{self.restaurante.nombre} - {self.usuario.username}'

    class Meta:
        ordering = ['fecha', 'hora']


class Resena(models.Model):

    # Usuario que escribe la reseña
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resenas'
    )

    # Restaurante evaluado
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='resenas'
    )

    # Puntuación entre 1 y 5
    puntuacion = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    texto = models.TextField()

    fecha_visita = models.DateField()

    # Cantidad de personas que marcaron la reseña como útil
    util_count = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f'{self.restaurante.nombre} - {self.puntuacion} estrellas'

    class Meta:
        ordering = ['-util_count']


class Horario(models.Model):

    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    # Restaurante al que pertenece el horario
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    dia_semana = models.CharField(
        max_length=20,
        choices=DIAS_SEMANA
    )

    hora_apertura = models.TimeField(
        null=True,
        blank=True
    )

    hora_cierre = models.TimeField(
        null=True,
        blank=True
    )

    # Permite indicar que ese día el restaurante no abre
    cerrado = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f'{self.restaurante.nombre} - {self.get_dia_semana_display()}'

    class Meta:
        ordering = ['restaurante', 'id']


class Promocion(models.Model):

    # Restaurante que ofrece la promoción
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='promociones'
    )

    titulo = models.CharField(
        max_length=200
    )

    descripcion = models.TextField(
        blank=True
    )

    # Porcentaje de descuento entre 0 y 100
    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    def __str__(self):
        return f'{self.titulo} - {self.restaurante.nombre}'

    class Meta:
        ordering = ['-fecha_inicio']


class Foto(models.Model):

    # Restaurante al que pertenece la fotografía
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='fotos'
    )

    # Imagen asociada al restaurante
    imagen = models.ImageField(
        upload_to='restaurantes/'
    )

    descripcion = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f'Foto de {self.restaurante.nombre}'