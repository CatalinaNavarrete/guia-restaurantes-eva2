from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.db.models import Sum

from .models import Restaurante, Reserva
from .forms import RestauranteForm, RegistroForm, ReservaForm


# =========================================================
# REGISTRO DE USUARIOS
# =========================================================

def registro(request):

    if request.user.is_authenticated:
        return redirect('listar_restaurantes')

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            try:
                form.save()

                messages.success(
                    request,
                    'Usuario registrado correctamente. Ahora puedes iniciar sesión.'
                )

                return redirect('login')

            except DatabaseError:

                messages.error(
                    request,
                    'Ocurrió un error al registrar el usuario.'
                )

    else:
        form = RegistroForm()

    return render(
        request,
        'registration/registro.html',
        {
            'form': form
        }
    )


# =========================================================
# LISTAR RESTAURANTES
# =========================================================

@login_required
def listar_restaurantes(request):

    # Todos los usuarios autenticados pueden ver el catálogo completo
    restaurantes = Restaurante.objects.all()

    tipos_disponibles = (
        Restaurante.objects
        .values_list(
            'tipo_comida',
            flat=True
        )
        .distinct()
        .order_by('tipo_comida')
    )

    tipo = request.GET.get('tipo', '')

    if tipo:
        restaurantes = restaurantes.filter(
            tipo_comida=tipo
        )

    paginator = Paginator(
        restaurantes,
        5
    )

    numero_pagina = request.GET.get('page')

    restaurantes_paginados = paginator.get_page(
        numero_pagina
    )

    return render(
        request,
        'listar.html',
        {
            'restaurantes': restaurantes_paginados,
            'tipos_disponibles': tipos_disponibles,
            'tipo_seleccionado': tipo,
        }
    )


# =========================================================
# CREAR RESTAURANTE
# =========================================================

@login_required
def crear_restaurante(request):

    if request.method == 'POST':

        form = RestauranteForm(
            request.POST
        )

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
                'Revisa los datos ingresados.'
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


# =========================================================
# EDITAR RESTAURANTE
# =========================================================

@login_required
def editar_restaurante(request, pk):

    # El superusuario puede modificar cualquier restaurante.
    # Un usuario normal solo puede modificar los propios.
    if request.user.is_superuser:

        restaurante = get_object_or_404(
            Restaurante,
            pk=pk
        )

    else:

        restaurante = get_object_or_404(
            Restaurante,
            pk=pk,
            usuario=request.user
        )

    if request.method == 'POST':

        form = RestauranteForm(
            request.POST,
            instance=restaurante
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
                'Revisa los datos ingresados.'
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


# =========================================================
# ELIMINAR RESTAURANTE
# =========================================================

@login_required
def eliminar_restaurante(request, pk):

    # El superusuario puede eliminar cualquier restaurante.
    # Un usuario normal solo puede eliminar los propios.
    if request.user.is_superuser:

        restaurante = get_object_or_404(
            Restaurante,
            pk=pk
        )

    else:

        restaurante = get_object_or_404(
            Restaurante,
            pk=pk,
            usuario=request.user
        )

    if request.method == 'POST':

        try:

            restaurante.delete()

            messages.success(
                request,
                'Restaurante eliminado correctamente.'
            )

            return redirect(
                'listar_restaurantes'
            )

        except DatabaseError:

            messages.error(
                request,
                'Ocurrió un error al eliminar el restaurante.'
            )

    return render(
        request,
        'eliminar.html',
        {
            'restaurante': restaurante
        }
    )


# =========================================================
# RESERVAR RESTAURANTE
# =========================================================

@login_required
def reservar_restaurante(request, pk):

    restaurante = get_object_or_404(
        Restaurante,
        pk=pk
    )

    if request.method == 'POST':

        form = ReservaForm(
            request.POST
        )

        if form.is_valid():

            fecha = form.cleaned_data[
                'fecha'
            ]

            hora = form.cleaned_data[
                'hora'
            ]

            cantidad_personas = form.cleaned_data[
                'cantidad_personas'
            ]

            # -------------------------------------------------
            # EVITAR TOPES DE HORARIO DEL MISMO USUARIO
            # -------------------------------------------------
            # El usuario no puede tener dos reservas
            # el mismo día y a la misma hora,
            # aunque sean en restaurantes diferentes.

            reserva_existente = (
                Reserva.objects
                .filter(
                    usuario=request.user,
                    fecha=fecha,
                    hora=hora
                )
                .exclude(
                    estado='cancelada'
                )
                .exists()
            )

            if reserva_existente:

                form.add_error(
                    'hora',
                    'Ya tienes una reserva para este día y horario.'
                )

            else:

                # -------------------------------------------------
                # CALCULAR PERSONAS YA RESERVADAS
                # -------------------------------------------------

                reservados = (
                    Reserva.objects
                    .filter(
                        restaurante=restaurante,
                        fecha=fecha,
                        hora=hora
                    )
                    .exclude(
                        estado='cancelada'
                    )
                    .aggregate(
                        total=Sum(
                            'cantidad_personas'
                        )
                    )['total']
                    or 0
                )

                # -------------------------------------------------
                # CAPACIDAD DISPONIBLE
                # -------------------------------------------------

                disponibles = (
                    restaurante.capacidad
                    - reservados
                )

                if cantidad_personas > disponibles:

                    form.add_error(
                        'cantidad_personas',
                        f'Solo quedan {disponibles} cupos disponibles '
                        f'para este horario.'
                    )

                else:

                    # -------------------------------------------------
                    # GUARDAR RESERVA AUTOMÁTICAMENTE CONFIRMADA
                    # -------------------------------------------------

                    try:

                        reserva = form.save(
                            commit=False
                        )

                        reserva.usuario = request.user
                        reserva.restaurante = restaurante

                        # La reserva válida queda confirmada
                        reserva.estado = 'confirmada'

                        reserva.save()

                        messages.success(
                            request,
                            'Reserva confirmada correctamente.'
                        )

                        return redirect(
                            'mis_reservas'
                        )

                    except DatabaseError:

                        messages.error(
                            request,
                            'Ocurrió un error al guardar la reserva. '
                            'Inténtalo nuevamente.'
                        )

        else:

            messages.error(
                request,
                'Revisa los datos ingresados en la reserva.'
            )

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


# =========================================================
# MIS RESERVAS
# =========================================================

@login_required
def mis_reservas(request):

    reservas = (
        Reserva.objects
        .filter(
            usuario=request.user
        )
        .select_related(
            'restaurante'
        )
        .order_by(
            'fecha',
            'hora'
        )
    )

    return render(
        request,
        'mis_reservas.html',
        {
            'reservas': reservas
        }
    )


# =========================================================
# DETALLE DEL RESTAURANTE
# =========================================================

@login_required
def detalle_restaurante(request, pk):

    restaurante = get_object_or_404(
        Restaurante,
        pk=pk
    )

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