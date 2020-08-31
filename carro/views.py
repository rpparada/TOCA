import tbk
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import CarroCompra, ItemCarroCompra
from orden.models import OrdenCompra, OrdenTBK
from tocata.models import Tocata
from facturacion.models import FacturacionProfile
from lugar.models import Region, Comuna
from direccion.models import Direccion

from direccion.forms import DireccionForm
from cuentas.forms import IngresarForm
from orden.forms import AgregaEmailAdicional

# Transbank conexion inicial (parametrizado para pruebas)
CERTIFICATES_DIR = os.path.join('orden', "commerces")
HOST = os.getenv("HOST", "http://127.0.0.1")
PORT = os.getenv("PORT", 8000)
BASE_URL = "{host}:{port}".format(host=HOST, port=PORT)
NORMAL_COMMERCE_CODE = "597020000540"

def load_commerce_data(commerce_code):
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".key"), "r"
    ) as file:
        key_data = file.read()
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".crt"), "r"
    ) as file:
        cert_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, "tbk.pem"), "r") as file:
        tbk_cert_data = file.read()

    return {
        'key_data': key_data,
        'cert_data': cert_data,
        'tbk_cert_data': tbk_cert_data,
    }

normal_commerce_data = load_commerce_data(NORMAL_COMMERCE_CODE)
normal_commerce = tbk.commerce.Commerce(
    commerce_code=NORMAL_COMMERCE_CODE,
    key_data=normal_commerce_data["key_data"],
    cert_data=normal_commerce_data["cert_data"],
    tbk_cert_data=normal_commerce_data["tbk_cert_data"],
    environment=tbk.environments.DEVELOPMENT,
)
webpay_service = tbk.services.WebpayService(normal_commerce)

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
            transaction = webpay_service.init_transaction(
                amount=orden_obj.total,
                buy_order=orden_obj.orden_id,
                return_url=BASE_URL + "/carro/retornotbk",
                final_url=BASE_URL + "/carro/compraexitosa",
                session_id=orden_obj.facturacion_profile.id,
            )

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
        transaction = webpay_service.get_transaction_result(token)
        transaction_detail = transaction["detailOutput"][0]
        webpay_service.acknowledge_transaction(token)
        if transaction_detail["responseCode"] == 0:

            # Recuperar Orden
            orden_obj = OrdenCompra.objects.by_orden_id(transaction['buyOrder'])
            ordenTBK = OrdenTBK.objects.create(
                orden               = orden_obj,
                token               = token,
                accountingDate      = transaction['accountingDate'],
                buyOrder            = transaction['buyOrder'],
                cardNumber          = transaction['cardDetail']['cardNumber'],
                cardExpirationDate  = transaction['cardDetail']['cardExpirationDate'],
                sharesAmount        = transaction['detailOutput'][0]['sharesAmount'],
                sharesNumber        = transaction['detailOutput'][0]['sharesNumber'],
                amount              = transaction['detailOutput'][0]['amount'],
                commerceCode        = transaction['detailOutput'][0]['commerceCode'],
                authorizationCode   = transaction['detailOutput'][0]['authorizationCode'],
                paymentTypeCode     = transaction['detailOutput'][0]['paymentTypeCode'],
                responseCode        = transaction['detailOutput'][0]['responseCode'],
                sessionId           = transaction['sessionId'],
                transactionDate     = transaction['transactionDate'],
                urlRedirection      = transaction['urlRedirection'],
                VCI                 = transaction['VCI']
            )

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
            ordenTBK = OrdenTBK.objects.create(
                orden               = orden_obj,
                token               = token,
                accountingDate      = transaction['accountingDate'],
                buyOrder            = transaction['buyOrder'],
                cardNumber          = transaction['cardDetail']['cardNumber'],
                cardExpirationDate  = transaction['cardDetail']['cardExpirationDate'],
                sharesAmount        = transaction['detailOutput'][0]['sharesAmount'],
                sharesNumber        = transaction['detailOutput'][0]['sharesNumber'],
                amount              = transaction['detailOutput'][0]['amount'],
                commerceCode        = transaction['detailOutput'][0]['commerceCode'],
                authorizationCode   = transaction['detailOutput'][0]['authorizationCode'],
                paymentTypeCode     = transaction['detailOutput'][0]['paymentTypeCode'],
                responseCode        = transaction['detailOutput'][0]['responseCode'],
                sessionId           = transaction['sessionId'],
                transactionDate     = transaction['transactionDate'],
                urlRedirection      = transaction['urlRedirection'],
                VCI                 = transaction['VCI']
            )

            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'carro/errorenpago.html', context)

@csrf_exempt
def compraexitosa(request):

    print(request.user)

    token = ''
    if request.method == 'POST':
        token = request.POST.get('token_ws')
        print('request')
        print(request.POST)

    context = {
        'token': token,
    }

    return render(request, 'carro/compraexitosa.html', context)

def fincompra(request):

    # token = ''
    # orden = OrdenTBK.objects.none()

    print(request.user)

    if request.method == 'POST':
        pass
        # carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
        # fact_profile, fact_profile_created = FacturacionProfile.objects.new_or_get(request)
        # orden_obj, orden_obj_created = OrdenCompra.objects.new_or_get(fact_profile, carro_obj)
        # token = request.POST.get('token_ws')
        # ordenTBK = OrdenTBK.objects.get(token=token)

    context = {
        #'orden': orden_obj,
    }

    return render(request, 'carro/fincompra_old.html', context)

def finerrorcompra (request):

    token = ''
    orden = OrdenTBK.objects.none()
    if request.method == 'POST':
        token = request.POST.get('token_ws')
        ordenTBK = OrdenTBK.objects.get(token=token)

    context = {
        'ordenTBK': ordenTBK,
    }

    return render(request, 'carro/finerrorcompra.html', context)

def checkout_complete_view(request):
    return render(request, 'carro/fincompra.html', {})


# def carga_comunas_agregar(request):
#
#     region_id = request.GET.get('region')
#     comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
#     context = {
#         'comunas_reg': comunas,
#     }
#     return render(request, 'direccion/comuna_dropdown_list_options_agregar.html', context)
#
# def carga_comunas_actualizar(request):
#
#     region_id = request.GET.get('region')
#     comuna_id = request.GET.get('comuna')
#     comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
#
#     if comuna_id.isdigit():
#         context = {
#             'comunas_reg': comunas,
#             'comuna_id': int(comuna_id),
#         }
#     else:
#         context = {
#             'comunas_reg': comunas,
#             'comuna_id': comunas.first(),
#         }
#
#     return render(request, 'direccion/comuna_dropdown_list_options_actualizar.html', context)
