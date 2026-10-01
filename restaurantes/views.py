from django.shortcuts import render, redirect
from .models import Restaurante
from .forms import RestauranteForm
from django.contrib.auth.decorators import login_required


@login_required
def listar_restaurantes(request):
    restaurantes = Restaurante.objects.filter(usuario=request.user)

    tipos_disponibles = restaurantes.values_list(
        'tipo_comida',
        flat=True
    ).distinct().order_by('tipo_comida')

    tipo = request.GET.get('tipo')

    if tipo:
        restaurantes = restaurantes.filter(tipo_comida=tipo)

    return render(
        request,
        'listar.html',
        {
            'restaurantes': restaurantes,
            'tipos_disponibles': tipos_disponibles,
            'tipo_seleccionado': tipo,
        }
    )


@login_required
def crear_restaurante(request):

    if request.method == 'POST':
        form = RestauranteForm(request.POST)

        if form.is_valid():
            restaurante = form.save(commit=False)
            restaurante.usuario = request.user
            restaurante.save()

            return redirect('listar_restaurantes')

    else:
        form = RestauranteForm()

    return render(
        request,
        'crear.html',
        {
            'form': form
        }
    )