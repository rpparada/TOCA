from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth

from .models import CarroCompra, ItemCarroCompra
from orden.models import OrdenCompra, Cobro, ControlCobro
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

        if is_done:
            # 1. Una vez seleccionado los bienes o servicios,
            # tarjetahabiente decide pagar a través de Webpay.
            # 2. El comercio inicia una transacción en Webpay,
            # invocando el método initTransaction().
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
        # 3. Webpay procesa el requerimiento y entrega como resultado
        # de la operación el token de la transacción y URL de
        # redireccionamiento a la cual se deberá redirigir al tarjetahabiente.

        # 4, 5, 6, 7, 8 y 9 son operaciones entre cliente y Transbank

        # 10. El navegador Web del tarjetahabiente realiza una petición
        # HTTPS al sitio del comercio, en base a la redirección generada
        # por Webpay en el punto 9.
        # 11. El sitio del comercio recibe la variable token_ws e invoca el
        # segundo método Web, getTransactionResult() (mientras se despliega la
        # página de transición), para obtener el resultado de la autorización.
        # Se recomienda que el resultado de la autorización sea persistida en
        # los sistemas del comercio, ya que este método se puede invocar una
        # única vez por transacción.
        token = request.POST.get('token_ws')
        control_obj = ControlCobro.objects.new_or_get(token=token)

        # 12. Comercio recibe el resultado de la invocación del método
        # getTransactionResult().
        transaction, transaction_detail = retorna_transaccion(token)

        if transaction_detail["responseCode"] == 0:

            # Recuperar Orden
            orden_obj = OrdenCompra.objects.by_orden_id(transaction['buyOrder'])
            cobro_obj = orden_obj.guarda_cobro(transaction, token)

            # 13. Para que el comercio informe a Webpay que el resultado de la
            # transacción se ha recibido sin problemas, el sistema del comercio
            # debe consumir el tercer método acknowledgeTransaction().
            # Si esto fue ejecutado correctamente el producto puede ser
            # liberado al cliente.
            # De no ser consumido acknowledgeTransaction() o demorar más de 30
            # segundos en su consumo, Webpay realizará la reversa de la transacción,
            # asumiendo que existieron problemas de comunicación.
            # En este caso el método retorna una Excepción indicando la situación,
            # el mensaje obtenido en la excepción será Timeout error (Transaction
            # is REVERSED)(272). Esta excepción debe ser manejada para no entregar
            # el producto o servicio en caso que ocurra.
            confirmar_transaccion(token)

            # Actualizar Orden
            orden_obj.mark_pagado()
            request.session['carro_tocatas'] = 0
            request.session.pop('carro_id', None)

            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }

            # 14. Una vez recibido el resultado de la transacción e informado a
            # Webpay su correcta recepción, el sitio del comercio debe redirigir
            # al tarjetahabiente nuevamente a Webpay, con la finalidad de desplegar
            # el comprobante de pago. Es importante realizar este punto para que
            # el tarjetahabiente entienda que el proceso de pago fue exitoso, y
            # que involucrará un cargo a su tarjeta bancaria. El redireccionamiento
            # a Webpay se hace utilizando como destino la URL informada por el
            # método getTransactionResult()enviando por método POST el token de
            # la transacción en la variable token_ws.
            return render(request, 'carro/envioexitosotbk.html', context)

        else:
            # Recuperar Orden
            orden_obj = OrdenCompra.objects.by_orden_id(transaction['buyOrder'])

            # Guardar trasaccion TBK
            cobro_obj = orden_obj.guarda_cobro(transaction, token)

            context = {
                #'cobro': cobro_obj,
            }
            return render(request, 'carro/comprafracasada.html', context)

    return render(request, 'carro/noseaun.html', {})

@csrf_exempt
def compraexitosa(request):

    # 15 y 16 son operaciones entre cliente y Transbank

    # 17. Una vez visualizado el comprobante de pago por un periodo
    # acotado de tiempo, el tarjetahabiente es redirigido de vuelta al
    # sitio del comercio, por medio de redireccionamiento con el token
    # en la variable token_ws enviada por método POST hacia la página
    # final informada por el comercio en el método initTransaction.

    # 18. Sitio del comercio despliega página final de pago
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

    return render(request, 'carro/compraexitosa.html', context)
