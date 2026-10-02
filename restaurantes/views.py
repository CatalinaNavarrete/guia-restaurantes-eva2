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
        {
            'form': form
        }
    )


@login_required
def listar_restaurantes(request):
    # Todos los usuarios autenticados pueden ver los restaurantes
    restaurantes = Restaurante.objects.all()

    tipos_disponibles = restaurantes.values_list(
        'tipo_comida',
        flat=True
    ).distinct().order_by('tipo_comida')

    tipo = request.GET.get('tipo')

    if tipo:
        restaurantes = restaurantes.filter(
            tipo_comida=tipo
        )

    paginator = Paginator(
        restaurantes,
        5
    )

    pagina = request.GET.get('page')

    restaurantes = paginator.get_page(
        pagina
    )

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
                restaurante = form.save(
                    commit=False
                )

                restaurante.usuario = request.user

                restaurante.save()

                messages.success(
                    request,
                    'Restaurante creado correctamente.'
                )

                return redirect(
                    'listar_restaurantes'
                )

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
    # Solo el propietario puede editar el restaurante
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

                return redirect(
                    'listar_restaurantes'
                )

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
        form = RestauranteForm(
            instance=restaurante
        )

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
    # Solo el propietario puede eliminar el restaurante
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

        return redirect(
            'listar_restaurantes'
        )

    return render(
        request,
        'eliminar.html',
        {
            'restaurante': restaurante
        }
    )


@login_required
def reservar_restaurante(request, pk):
    # Busca el restaurante donde se realizará la reserva
    restaurante = get_object_or_404(
        Restaurante,
        pk=pk
    )

    if request.method == 'POST':
        form = ReservaForm(
            request.POST
        )

        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            cantidad = form.cleaned_data[
                'cantidad_personas'
            ]

            # Comprueba si el usuario ya tiene una reserva
            # para el mismo restaurante, fecha y hora
            reserva_existente = Reserva.objects.filter(
                usuario=request.user,
                restaurante=restaurante,
                fecha=fecha,
                hora=hora
            ).exclude(
                estado='cancelada'
            ).exists()

            if reserva_existente:
                form.add_error(
                    None,
                    'Ya tienes una reserva para este restaurante en la misma fecha y hora.'
                )

            else:
                # Suma la cantidad de personas ya reservadas
                # para ese restaurante, fecha y hora
                reservados = Reserva.objects.filter(
                    restaurante=restaurante,
                    fecha=fecha,
                    hora=hora
                ).exclude(
                    estado='cancelada'
                ).aggregate(
                    total=Sum(
                        'cantidad_personas'
                    )
                )['total'] or 0

                # Calcula los cupos disponibles
                disponibles = (
                    restaurante.capacidad
                    - reservados
                )

                # Impide superar la capacidad máxima
                if cantidad > disponibles:
                    form.add_error(
                        'cantidad_personas',
                        f'Solo quedan {disponibles} cupos disponibles.'
                    )

                else:
                    try:
                        reserva = form.save(
                            commit=False
                        )

                        reserva.usuario = request.user
                        reserva.restaurante = restaurante

                        reserva.save()

                        messages.success(
                            request,
                            'Reserva realizada correctamente.'
                        )

                        return redirect(
                            'mis_reservas'
                        )

                    except DatabaseError:
                        messages.error(
                            request,
                            'Ocurrió un error al guardar la reserva.'
                        )

    else:
        form = ReservaForm()

    return render(
        request,
        'reservar.html',
        {
            'form': form,
            'restaurante': restaurante
        }
    )


@login_required
def mis_reservas(request):
    # Cada usuario solamente puede ver sus propias reservas
    reservas = Reserva.objects.filter(
        usuario=request.user
    )

    return render(
        request,
        'mis_reservas.html',
        {
            'reservas': reservas
        }
    )


@login_required
def detalle_restaurante(request, pk):
    # Busca el restaurante seleccionado
    restaurante = get_object_or_404(
        Restaurante,
        pk=pk
    )

    # Obtiene toda la información relacionada
    # con el restaurante
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