from django.db import models

class Restaurante(models.Model):
    CALIFICACION_CHOICES = [
        (1, '1 estrella'),
        (2, '2 estrellas'),
        (3, '3 estrellas'),
        (4, '4 estrellas'),
        (5, '5 estrellas'),
    ]

    nombre = models.CharField(max_length=200)
    tipo_comida = models.CharField(max_length=100)
    calificacion = models.IntegerField(choices=CALIFICACION_CHOICES, default=3)
    abierto = models.BooleanField(default=True)
    fecha_visita = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-calificacion']