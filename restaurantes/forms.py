from django import forms
from django.utils import timezone
from .models import Restaurante, Reserva
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RestauranteForm(forms.ModelForm):
    class Meta:
        model = Restaurante
        fields = [
            'nombre',
            'tipo_comida',
            'calificacion',
            'abierto',
            'fecha_visita',
            'capacidad',
        ]

    
    def clean_fecha_visita(self):
        fecha_visita = self.cleaned_data.get('fecha_visita')

        if fecha_visita and fecha_visita > timezone.localdate():
            raise forms.ValidationError(
                'La fecha de visita no puede ser futura.'
            )

        return fecha_visita

#aprovecha el sistema de usuarios que Django ya trae.
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class ReservaForm(forms.ModelForm):
    # Formulario que utilizará el cliente para realizar una reserva
    class Meta:
        model = Reserva

        # El usuario y el restaurante se asignan automáticamente
        # desde la vista, por eso no aparecen en el formulario
        fields = [
            'fecha',
            'hora',
            'cantidad_personas',
            'nota',
        ]

        # Muestra selectores adecuados para fecha y hora
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }