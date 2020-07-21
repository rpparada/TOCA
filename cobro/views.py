from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from tbk.services import WebpayService
from tbk.commerce import Commerce
from tbk import INTEGRACION

from cobro.models import Carro, Orden, OrdenTocata, OrdenTBK
from tocata.models import Tocata

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca, parCarro

# Create your views here.
import tbk
import os

CERTIFICATES_DIR = os.path.join(os.path.dirname(__file__), "commerces")
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
        "key_data": key_data,
        "cert_data": cert_data,
        "tbk_cert_data": tbk_cert_data,
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


def detalleorden(request, orden_id):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    orden = Orden.objects.get(pk=orden_id)
    ordentocata = OrdenTocata.objects.filter(orden=orden)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'orden': orden,
        'ordentocata': ordentocata,
    }

    return render(request, 'cobro/detalleorden.html', context)


def finerrorcompra (request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    token = ''
    orden = OrdenTBK.objects.none()
    if request.method == 'POST':
        token = request.POST.get('token_ws')
        ordenTBK = OrdenTBK.objects.get(token=token)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'ordenTBK': ordenTBK,
    }

    return render(request, 'cobro/finerrorcompra.html', context)


def fincompra(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    token = ''
    orden = OrdenTBK.objects.none()
    if request.method == 'POST':
        token = request.POST.get('token_ws')
        ordenTBK = OrdenTBK.objects.get(token=token)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'ordenTBK': ordenTBK,
    }

    return render(request, 'cobro/fincompra.html', context)


@csrf_exempt
def compraexitosa(request):

    token = ''
    if request.method == 'POST':
        token = request.POST.get('token_ws')

    context = {
        'token': token,
    }

    return render(request, 'cobro/compraexitosa.html', context)

@csrf_exempt
def retornotbk(request):

    if request.method == 'POST':

        token = request.POST.get('token_ws')
        transaction = webpay_service.get_transaction_result(token)
        transaction_detail = transaction["detailOutput"][0]
        webpay_service.acknowledge_transaction(token)
        if transaction_detail["responseCode"] == 0:

            # Recuperar Orden
            orden = Orden.objects.get(pk=transaction['buyOrder'])

            # Guardar trasaccion TBK
            ordentbk = OrdenTBK(
                orden = orden,
                token = token,
                accountingDate = transaction['accountingDate'],
                buyOrder = transaction['buyOrder'],
                cardNumber = transaction['cardDetail']['cardNumber'],
                cardExpirationDate = transaction['cardDetail']['cardExpirationDate'],
                sharesAmount = transaction['detailOutput'][0]['sharesAmount'],
                sharesNumber = transaction['detailOutput'][0]['sharesNumber'],
                amount = transaction['detailOutput'][0]['amount'],
                commerceCode = transaction['detailOutput'][0]['commerceCode'],
                authorizationCode = transaction['detailOutput'][0]['authorizationCode'],
                paymentTypeCode = transaction['detailOutput'][0]['paymentTypeCode'],
                responseCode = transaction['detailOutput'][0]['responseCode'],
                sessionId = transaction['sessionId'],
                transactionDate = transaction['transactionDate'],
                urlRedirection = transaction['urlRedirection'],
                VCI = transaction['VCI']
            )
            ordentbk.save()

            # Actualizar Orden
            orden.estado = parToca['pagado']
            orden.save()

            # Actualizar Carro y Tocatas
            listacarro = Carro.objects.filter(orden=orden)
            for item in listacarro:
                item.estado = parToca['pagado']
                item.save()
                tocata = Tocata.objects.get(pk=item.tocata.pk)
                tocata.asistentes_total += item.cantidad
                tocata.save()

            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'cobro/envioexitosotbk.html', context)

        else:

            # Recuperar Orden
            orden = Orden.objects.get(pk=transaction['buyOrder'])

            # Guardar trasaccion TBK
            ordentbk = OrdenTBK(
                orden = orden,
                token = token,
                accountingDate = transaction['accountingDate'],
                buyOrder = transaction['buyOrder'],
                cardNumber = transaction['cardDetail']['cardNumber'],
                cardExpirationDate = transaction['cardDetail']['cardExpirationDate'],
                sharesAmount = transaction['detailOutput'][0]['sharesAmount'],
                sharesNumber = transaction['detailOutput'][0]['sharesNumber'],
                amount = transaction['detailOutput'][0]['amount'],
                commerceCode = transaction['detailOutput'][0]['commerceCode'],
                authorizationCode = transaction['detailOutput'][0]['authorizationCode'],
                paymentTypeCode = transaction['detailOutput'][0]['paymentTypeCode'],
                responseCode = transaction['detailOutput'][0]['responseCode'],
                sessionId = transaction['sessionId'],
                transactionDate = transaction['transactionDate'],
                urlRedirection = transaction['urlRedirection'],
                VCI = transaction['VCI']
            )
            ordentbk.save()
            
            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'cobro/errorenpago.html', context)

@login_required(login_url='index')
def procesarorden(request, orden_id):

    if request.method == 'POST':
        email = request.POST.get('altemail')
        orden = Orden.objects.get(pk=orden_id)
        if email:
            orden.email = email
        else:
            orden.email = request.user.email
        orden.save()

        transaction = webpay_service.init_transaction(
            amount=orden.totalapagar,
            buy_order=orden_id,
            return_url=BASE_URL + "/cobro/retornotbk",
            final_url=BASE_URL + "/cobro/compraexitosa",
            session_id=request.user.email,
        )

        context = {
            'transaction': transaction,
        }

        return render(request, 'cobro/enviotbk.html', context)

@login_required(login_url='index')
def comprar(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    listacarro = Carro.objects.filter(usuario=request.user).filter(estado=parToca['pendiente'])
    sumatotal = 0
    contador = 0
    orden = Orden.objects.none()

    # Calcular totales y verificar si ya tiene orden asociada
    for compra in listacarro:
        sumatotal = sumatotal + compra.total
        contador = contador + compra.cantidad
        if compra.orden:
            orden = compra.orden

    # Actualiza orden si existe o crear orden
    if orden:
        orden.numerodeitems = contador
        orden.totalapagar = sumatotal
        orden.save()
        OrdenTocata.objects.filter(orden=orden).delete()
    else:
        orden = Orden(
            usuario=request.user,
            numerodeitems=contador,
            totalapagar=sumatotal
        )
        orden.save()

    # Agregar Tocatas a OrdenTocata
    ordentocata = []
    for compra in listacarro:
        item = OrdenTocata(
            orden = orden,
            tocata = compra.tocata,
            cantidad = compra.cantidad,
            total = compra.total,
        )
        item.save()
        ordentocata.append(item)
        compra.orden = orden
        compra.save()

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'orden': orden,
        'ordentocata': ordentocata,

    }

    return render(request, 'cobro/comprar.html', context)

@login_required(login_url='index')
def micarro(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    listacarro = Carro.objects.filter(usuario=request.user).filter(estado=parToca['pendiente'])

    sumatotal = 0
    for compra in listacarro:
        sumatotal = sumatotal + compra.total

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'listacarro': listacarro,
        'sumatotal': sumatotal,
    }

    return render(request, 'cobro/micarro.html', context)

@login_required(login_url='index')
def agregaracarro(request, tocata_id):

    if request.method == 'POST':

        next = request.POST.get('next', '/')
        cantidad = request.POST.get('numeroentradas')

        # Verifica si ya compro entradas para esta tocata
        item = Carro.objects.filter(tocata=tocata_id).filter(usuario=request.user)
        listapagados = item.filter(estado=parToca['pagado'])
        if listapagados:
            totalpagados = 0
            for pagado in listapagados:
                totalpagados += pagado.cantidad

            if totalpagados == 2:
                messages.error(request,'Ya compraste dos entradas para esta Tocata Intima')
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return redirect('tocatas')
            else:
                if int(cantidad) == 2:
                    messages.error(request,'Ya compraste una entrada, solo puedes comprar una mas')
                    if next:
                        return HttpResponseRedirect(next)
                    else:
                        return redirect('tocatas')

        # Verifica si ya tiene entradas en el carro y cuantas tiene (solo puede comprar maximo 2)
        listapendientes = item.filter(estado=parToca['pendiente'])
        if listapendientes:
            totalpendientes = 0
            for pendiente in listapendientes:
                totalpendientes += pendiente.cantidad

            if totalpendientes == 2:
                messages.error(request,'Ya tienes en tu canasta dos entradas')
                if next:
                    return HttpResponseRedirect(next)
                else:
                    return redirect('tocatas')
            else:
                if int(cantidad) == 2:
                    messages.error(request,'Ya tienes en tu canasta una entrada, solo puedes agregar una mas')
                    if next:
                        return HttpResponseRedirect(next)
                    else:
                        return redirect('tocatas')
                else:
                    pendiente.cantidad = 2
                    pendiente.total = pendiente.tocata.costo * 2
                    pendiente.save()
                    messages.success(request,'Tocata Agregada a Carro')

        else:
            tocata = Tocata.objects.get(pk=tocata_id)
            itemcarro = Carro(
                tocata = tocata,
                usuario = request.user,
                cantidad = cantidad,
                total = tocata.costo * int(cantidad)
            )
            itemcarro.save()
            messages.success(request,'Tocata Agregada a Carro')

    if next:
        return HttpResponseRedirect(next)
    else:
        return redirect('tocatas')

@login_required(login_url='index')
def quitarcarro(request, item_id):

    next = request.GET.get('next', '/')

    # Quitar item de carro
    item = Carro.objects.get(pk=item_id)
    item.estado = parToca['cancelado']
    item.save()
    messages.success(request,'Item quitado de carro')

    if next:
        return HttpResponseRedirect(next)
    else:
        return redirect('tocatas')

@login_required(login_url='index')
def miscompras(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    listaorden = Orden.objects.filter(usuario=request.user)

    for orden in listaorden:
        orden.detalles = OrdenTocata.objects.filter(orden=orden)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'listaorden': listaorden,
    }

    return render(request, 'usuario/miscompras.html', context)
