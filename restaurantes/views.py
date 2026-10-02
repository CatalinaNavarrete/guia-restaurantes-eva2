from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError
from .models import Restaurante
from .forms import RestauranteForm


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

    paginator = Paginator(restaurantes, 5)
    pagina = request.GET.get('page')
    restaurantes = paginator.get_page(pagina)

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
            try:
                restaurante = form.save(commit=False)
                restaurante.usuario = request.user
                restaurante.save()

                messages.success(
                    request,
                    'Restaurante creado correctamente.'
                )
                return redirect('listar_restaurantes')

            except DatabaseError:
                messages.error(
                    request,
                    'Ocurrió un error al guardar el restaurante.'
                )

        else:
            messages.error(
                request,
                'No se pudo crear el restaurante. Revisa los datos ingresados.'
            )

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
            try:
                form.save()

                messages.success(
                    request,
                    'Restaurante actualizado correctamente.'
                )
                return redirect('listar_restaurantes')

            except DatabaseError:
                messages.error(
                    request,
                    'Ocurrió un error al actualizar el restaurante.'
                )

        else:
            messages.error(
                request,
                'No se pudo actualizar el restaurante. Revisa los datos ingresados.'
            )

    else:
        form = RestauranteForm(instance=restaurante)

    return render(
        request,
        'editar.html',
        {
            'form': form,
            'restaurante': restaurante,
        }
    )


@login_required
def eliminar_restaurante(request, pk):
    restaurante = get_object_or_404(
        Restaurante,
        pk=pk,
        usuario=request.user,
    )

    if request.method == 'POST':
        try:
            restaurante.delete()

            messages.success(
                request,
                'Restaurante eliminado correctamente.'
            )

        except DatabaseError:
            messages.error(
                request,
                'Ocurrió un error al eliminar el restaurante.'
            )

        return redirect('listar_restaurantes')

    return render(
        request,
        'eliminar.html',
        {
            'restaurante': restaurante
        }
    )