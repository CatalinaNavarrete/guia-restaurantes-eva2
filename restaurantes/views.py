from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.db.models import Sum

from .models import Restaurante, Reserva
from .forms import RestauranteForm, RegistroForm, ReservaForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('listar_restaurantes')

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Cuenta creada correctamente. Ahora puedes iniciar sesión.'
            )
            return redirect('login')
    else:
        form = RegistroForm()

    return render(
        request,
        'registration/registro.html',
        {'form': form}
    )


@login_required
def listar_restaurantes(request):
    restaurantes = Restaurante.objects.all()

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
            restaurante = form.save(commit=False)
            restaurante.usuario = request.user

            try:
                restaurante.save()
            except DatabaseError:
                messages.error(
                    request,
                    'Ocurrió un error al guardar el restaurante.'
                )
            else:
                messages.success(
                    request,
                    'Restaurante creado correctamente.'
                )
                return redirect('listar_restaurantes')
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
        {'form': form}
    )


@login_required
def editar_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)

    if restaurante.usuario != request.user:
        messages.error(
            request,
            'No tienes permiso para editar este restaurante.'
        )
        return redirect('listar_restaurantes')

    if request.method == 'POST':
        form = RestauranteForm(
            request.POST,
            instance=restaurante,
        )

        if form.is_valid():
            try:
                form.save()
            except DatabaseError:
                messages.error(
                    request,
                    'Ocurrió un error al actualizar el restaurante.'
                )
            else:
                messages.success(
                    request,
                    'Restaurante actualizado correctamente.'
                )
                return redirect('listar_restaurantes')
        else:
            messages.error(
                request,
                'No se pudo actualizar el restaurante. '
                'Revisa los datos ingresados.'
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
    restaurante = get_object_or_404(Restaurante, pk=pk)

    if restaurante.usuario != request.user:
        messages.error(
            request,
            'No tienes permiso para eliminar este restaurante.'
        )
        return redirect('listar_restaurantes')

    if request.method == 'POST':
        try:
            restaurante.delete()
        except DatabaseError:
            messages.error(
                request,
                'Ocurrió un error al eliminar el restaurante.'
            )
        else:
            messages.success(
                request,
                'Restaurante eliminado correctamente.'
            )

        return redirect('listar_restaurantes')

    return render(
        request,
        'eliminar.html',
        {'restaurante': restaurante}
    )


@login_required
def reservar_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST)

        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            cantidad = form.cleaned_data['cantidad_personas']

            reserva_existente = Reserva.objects.filter(
                usuario=request.user,
                restaurante=restaurante,
                fecha=fecha,
                hora=hora,
            ).exclude(
                estado='cancelada'
            ).exists()

            if reserva_existente:
                form.add_error(
                    None,
                    'Ya tienes una reserva para este restaurante '
                    'en la misma fecha y hora.'
                )
            else:
                reservados = Reserva.objects.filter(
                    restaurante=restaurante,
                    fecha=fecha,
                    hora=hora,
                ).exclude(
                    estado='cancelada'
                ).aggregate(
                    total=Sum('cantidad_personas')
                )['total'] or 0

                disponibles = restaurante.capacidad - reservados

                if cantidad > disponibles:
                    form.add_error(
                        'cantidad_personas',
                        f'Solo quedan {disponibles} cupos disponibles.'
                    )
                else:
                    reserva = form.save(commit=False)
                    reserva.usuario = request.user
                    reserva.restaurante = restaurante

                    try:
                        reserva.save()
                    except DatabaseError:
                        messages.error(
                            request,
                            'Ocurrió un error al guardar la reserva. '
                            'Intenta nuevamente.'
                        )
                    else:
                        messages.success(
                            request,
                            'Reserva realizada correctamente.'
                        )
                        return redirect('mis_reservas')
    else:
        form = ReservaForm()

    return render(
        request,
        'reservar.html',
        {
            'form': form,
            'restaurante': restaurante,
        }
    )


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)

    return render(
        request,
        'mis_reservas.html',
        {'reservas': reservas}
    )


@login_required
def detalle_restaurante(request, pk):
    restaurante = get_object_or_404(Restaurante, pk=pk)

    horarios = restaurante.horarios.all()
    promociones = restaurante.promociones.all()
    resenas = restaurante.resenas.all()
    fotos = restaurante.fotos.all()

    return render(
        request,
        'detalle.html',
        {
            'restaurante': restaurante,
            'horarios': horarios,
            'promociones': promociones,
            'resenas': resenas,
            'fotos': fotos,
        }
    )