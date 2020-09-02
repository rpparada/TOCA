from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth

from .models import CarroCompra, ItemCarroCompra
from orden.models import OrdenCompra, Cobro
from tocata.models import Tocata
from facturacion.models import FacturacionProfile
from lugar.models import Region, Comuna
from direccion.models import Direccion

from direccion.forms import DireccionForm
from cuentas.forms import IngresarForm
from orden.forms import AgregaEmailAdicional

from toca.utils import inicia_transaccion, retorna_transaccion, confirmar_transaccion


# Create your views here.
def carro_detalle_api_body_view(request):

    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)

    if carro_obj.item.all().count() > 0:
        listatocatas = {
            'items': carro_obj.item.all()
        }
        string_render = render_to_string('carro/snippets/bodyitemcarro.html', listatocatas, request=request)

        context = {
            'carroData': True,
            'html': string_render,
            'subtotal': '{0:,}'.format(int(carro_obj.subtotal)),
            'total': '{0:,}'.format(int(carro_obj.total))
        }

        return JsonResponse(context)

    return JsonResponse({'carroData': False})

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
        item, created = carro_obj.get_or_create_item(tocata)

        if created:
            carro_obj.item.add(item)
            added = True
        else:
            carro_obj.item.remove(item)
            item.delete()
            added = False

        request.session['carro_tocatas'] = carro_obj.item.count()

        if request.is_ajax():
            json_data = {
                'added': added,
                'removed': not added,
                'carroNumItem': carro_obj.item.count()
            }
            #return JsonResponse({'Mensaje Error':'Error 400'}, status=400)
            return JsonResponse(json_data, status=200)
    return redirect('carro')

def carro_actualizar_suma(request):

    tocata_id = request.POST.get('tocata_id')
    origen = request.POST.get('origen')
    if tocata_id is not None:
        try:
            tocata = Tocata.objects.get(id=tocata_id)
        except Tocata.DoesNotExist:
            # Mensaje de Error al usuario
            return redirect('carro:carro')

        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
        item, created = carro_obj.get_or_create_item(tocata)

        added = False
        if created:
            carro_obj.item.add(item)
            added = True
        else:
            if item.agrega_item():
                carro_obj.update_subtotal()

        request.session['carro_tocatas'] = carro_obj.item.count()

        if origen == 'tocata':
            context = {
                'tocata': tocata,
                'instance': item,
                'origen': origen
            }
            string_render = render_to_string('carro/snippets/cantidaditem.html', context, request=request)
            if request.is_ajax():
                json_data = {
                    'origenTocata': True,
                    'html': string_render,
                    'added': added,
                    'carroNumItem': carro_obj.item.count()
                }
                return JsonResponse(json_data, status=200)

        elif origen == 'tablacarro':
            listatocatas = {
                'items': carro_obj.item.all()
            }
            string_render = render_to_string('carro/snippets/bodyitemcarro.html', listatocatas, request=request)
            context = {
                'carroData': True,
                'html': string_render,
                'subtotal': '{0:,}'.format(int(carro_obj.subtotal)),
                'total': '{0:,}'.format(int(carro_obj.total)),
                'carroNumItem': carro_obj.item.count()
            }
            return JsonResponse(context)

    return redirect('carro:carro')

def carro_actualizar_resta(request):

    tocata_id = request.POST.get('tocata_id')
    origen = request.POST.get('origen')

    if tocata_id is not None:
        try:
            tocata = Tocata.objects.get(id=tocata_id)
        except Tocata.DoesNotExist:
            # Mensaje de Error al usuario
            return redirect('carro:carro')

        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
        item, created = carro_obj.get_or_create_item(tocata)

        removed = False
        if created:
            item.delete()
        else:
            if item.quita_item():
                carro_obj.update_subtotal()
            else:
                carro_obj.item.remove(item)
                item.delete()
                item = None
                removed = True

        request.session['carro_tocatas'] = carro_obj.item.count()

        if origen == 'tocata':
            context = {
                'tocata': tocata,
                'instance': item,
                'origen': origen
            }
            string_render = render_to_string('carro/snippets/cantidaditem.html', context, request=request)
            if request.is_ajax():
                json_data = {
                    'origenTocata': True,
                    'html': string_render,
                    'removed': removed,
                    'carroNumItem': carro_obj.item.count()
                }
                return JsonResponse(json_data, status=200)
        elif origen == 'tablacarro':
            listatocatas = {
                'items': carro_obj.item.all()
            }
            string_render = render_to_string('carro/snippets/bodyitemcarro.html', listatocatas, request=request)
            context = {
                'carroData': True,
                'html': string_render,
                'subtotal': '{0:,}'.format(int(carro_obj.subtotal)),
                'total': '{0:,}'.format(int(carro_obj.total)),
                'carroNumItem': carro_obj.item.count()
            }
            return JsonResponse(context)

    return redirect('carro:carro')

@login_required
def checkout_home(request):

    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
    orden_obj = None
    if nuevo_carro or carro_obj.item.count() == 0:
        return redirect('carro')

    fact_profile, fact_profile_created = FacturacionProfile.objects.new_or_get(request)
    orden_obj, orden_obj_created = OrdenCompra.objects.new_or_get(fact_profile, carro_obj)

    email_adicional = AgregaEmailAdicional()

    if request.method == 'POST':
        email = request.POST.get('email')
        orden_obj.email_adicional = email
        orden_obj.save()
        is_done = orden_obj.check_done()
        # if is_done:
        #     orden_obj.mark_pagado()
        #     request.session['carro_tocatas'] = 0
        #     del request.session['carro_id']
        #     return redirect('carro:checkout_complete')
        if is_done:

            transaction = inicia_transaccion(orden_obj)

            context = {
                'transaction': transaction,
            }
            return render(request, 'carro/enviotbk.html', context)

    context = {
        'email_adicional': email_adicional,
        'object': orden_obj
    }
    return render(request, 'carro/checkout.html', context)

@csrf_exempt
def retornotbk(request):

    if request.method == 'POST':

        token = request.POST.get('token_ws')
        transaction, transaction_detail = retorna_transaccion(token)
        confirmar_transaccion(token)

        if transaction_detail["responseCode"] == 0:
            # Recuperar Orden
            orden_obj = OrdenCompra.objects.by_orden_id(transaction['buyOrder'])
            cobro_obj = orden_obj.guarda_cobro(transaction, token)

            # Actualizar Orden
            orden_obj.mark_pagado()
            request.session['carro_tocatas'] = 0
            request.session.pop('carro_id', None)

            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'carro/envioexitosotbk.html', context)

        else:
            # Recuperar Orden
            orden_obj = OrdenCompra.objects.by_orden_id(transaction['buyOrder'])

            # Guardar trasaccion TBK
            cobro_obj = orden_obj.guarda_cobro(transaction, token)

            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'carro/errorenpago.html', context)

@csrf_exempt
def compraexitosa(request):

    token = ''
    if request.method == 'POST':
        token = request.POST.get('token_ws')

    context = {
        'token': token,
    }

    return render(request, 'carro/compraexitosa.html', context)

def fincompra(request):

    if request.method == 'POST':

        # ¿Es esta la unica solucion? Investigar
        token = request.POST.get('token_ws')
        qs = Cobro.objects.select_related('orden__facturacion_profile__usuario').filter(token=token)
        user = qs[0].orden.facturacion_profile.usuario
        orden_obj = qs[0].orden

        auth.login(request, user)

    context = {
        'orden': orden_obj,
    }

    return render(request, 'carro/fincompra_old.html', context)

def finerrorcompra (request):

    token = ''
    cobro_obj = Cobro.objects.none()
    if request.method == 'POST':
        token = request.POST.get('token_ws')
        cobro_obj = Cobro.objects.get(token=token)

    context = {
        'cobro': cobro_obj,
    }

    return render(request, 'carro/finerrorcompra.html', context)

def checkout_complete_view(request):
    return render(request, 'carro/fincompra.html', {})
