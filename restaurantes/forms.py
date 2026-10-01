from django import forms
from .models import Restaurante


class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = [
            'nombre',
            'tipo_comida',
            'calificacion',
            'abierto',
            'fecha_visita',
        ]