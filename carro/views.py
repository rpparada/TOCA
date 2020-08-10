from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import CarroCompra
from orden.models import OrdenCompra
from tocata.models import Tocata
from facturacion.models import FacturacionProfile
from lugar.models import Region, Comuna
from direccion.models import Direccion

from direccion.forms import DireccionForm

from usuario.forms import IngresarForm

# Create your views here.
def carro_detalle_api_view(request):

    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
    tocatas = [{
        'id': x.id,
        'url': x.get_absolute_url(),
        'nombre': x.nombre,
        'costo': x.costo
    } for x in carro_obj.tocata.all()]

    carro_data = {
        'tocatas': tocatas,
        'subtotal': carro_obj.subtotal,
        'total': carro_obj.total
    }
    return JsonResponse(carro_data)

def carro_home(request):

    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)

    context = {
        'carro': carro_obj
    }

    return render(request, 'carro/carro_home.html', context)

def carro_actualizar(request):
    tocata_id = request.POST.get('tocata_id')
    if tocata_id is not None:
        try:
            tocata = Tocata.objects.get(id=tocata_id)
        except Tocata.DoesNotExist:
            # Mensaje de Error al usuario
            return redirect('carro')
        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
        if tocata in carro_obj.tocata.all():
            carro_obj.tocata.remove(tocata)
            added = False
        else:
            carro_obj.tocata.add(tocata)
            added = True

        request.session['carro_tocatas'] = carro_obj.tocata.count()

        if request.is_ajax():
            json_data = {
                'added': added,
                'removed': not added,
                'carroNumItem': carro_obj.tocata.count()
            }
            return JsonResponse(json_data)

    return redirect('carro')

def checkout_home(request):
    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
    orden_obj = None
    if nuevo_carro or carro_obj.tocata.count() == 0:
        return redirect('carro')

    ingreso_form = IngresarForm()
    direccion_form = DireccionForm()

    direccion_envio_id = request.session.get('direccion_envio_id', None)
    direccion_facturacion_id = request.session.get('direccion_facturacion_id', None)

    fact_profile, fact_profile_created = FacturacionProfile.objects.new_or_get(request)

    direccion_qs = None
    if fact_profile is not None:
        if request.user.is_authenticated:
            direccion_qs = Direccion.objects.filter(facturacion_profile=fact_profile)
        orden_obj, orden_obj_created = OrdenCompra.objects.new_or_get(fact_profile, carro_obj)
        if direccion_envio_id:
            orden_obj.direccion_envio = Direccion.objects.get(id=direccion_envio_id)
            del request.session['direccion_envio_id']
        if direccion_facturacion_id:
            orden_obj.direccion_facturacion = Direccion.objects.get(id=direccion_facturacion_id)
            del request.session['direccion_facturacion_id']
        if direccion_envio_id or direccion_facturacion_id:
            orden_obj.save()

    if request.method == 'POST':
        is_done = orden_obj.check_done()
        if is_done:
            orden_obj.mark_pagado()
            request.session['carro_tocatas'] = 0
            del request.session['carro_id']
            return redirect('checkout_complete')

    context = {
        'object': orden_obj,
        'fact_profile': fact_profile,
        'ingreso_form': ingreso_form,
        'direccion_form': direccion_form,
        'direccion_qs': direccion_qs,
    }
    return render(request, 'carro/checkout.html', context)

def checkout_complete_view(request):
    return render(request, 'carro/fincompra.html', {})


def carga_comunas_agregar(request):

    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
    context = {
        'comunas_reg': comunas,
    }
    return render(request, 'direccion/comuna_dropdown_list_options_agregar.html', context)

def carga_comunas_actualizar(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')

    if comuna_id.isdigit():
        context = {
            'comunas_reg': comunas,
            'comuna_id': int(comuna_id),
        }
    else:
        context = {
            'comunas_reg': comunas,
            'comuna_id': comunas.first(),
        }

    return render(request, 'direccion/comuna_dropdown_list_options_actualizar.html', context)
