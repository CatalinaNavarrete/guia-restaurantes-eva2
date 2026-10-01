from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def editar_restaurante(request, pk):
    restaurante = get_object_or_404(
        Restaurante,
        pk=pk,
        usuario=request.user,
    )

    if request.method == 'POST':
        form = RestauranteForm(
            request.POST,
            instance=restaurante,
        )

        if form.is_valid():
            form.save()
            return redirect('listar_restaurantes')
    else:
        form = RestauranteForm(instance=restaurante)

    return render(
        request,
        'editar.html',
        {
            'form': form,
            'restaurante': restaurante,
        },
    )
@login_required
def eliminar_restaurante(request, pk):
    restaurante = get_object_or_404(
        Restaurante,
        pk=pk,
        usuario=request.user,
    )

    if request.method == 'POST':
        restaurante.delete()
        return redirect('listar_restaurantes')

    return render(
        request,
        'eliminar.html',
        {'restaurante': restaurante},
    )