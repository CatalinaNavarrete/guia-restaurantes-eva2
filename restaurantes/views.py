from django.shortcuts import render
from .models import Restaurante

def listar_restaurantes(request):
    restaurantes = Restaurante.objects.all()

    tipo = request.GET.get('tipo')
    if tipo:
        restaurantes = restaurantes.filter(tipo_comida=tipo)

    tipos_disponibles = Restaurante.objects.values_list('tipo_comida', flat=True).distinct().order_by('tipo_comida')

    return render(
        request,
        'listar.html',
        {
            'restaurantes': restaurantes,
            'tipos_disponibles': tipos_disponibles,
            'tipo_seleccionado': tipo,
        }
    )