from django import forms
from django.utils import timezone
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

    
    def clean_fecha_visita(self):
        fecha_visita = self.cleaned_data.get('fecha_visita')

        if fecha_visita and fecha_visita > timezone.localdate():
            raise forms.ValidationError(
                'La fecha de visita no puede ser futura.'
            )

        return fecha_visita