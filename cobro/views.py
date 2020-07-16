from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from tbk.services import WebpayService
from tbk.commerce import Commerce
from tbk import INTEGRACION

from cobro.models import Carro, Orden, OrdenTocata
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

@csrf_exempt
def compraexitosa(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    if request.method == 'POST':
        print(request.POST.get('token_ws'))

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
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
            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'cobro/envioexitosotbk.html', context)
        else:
            context = {
                'transaction': transaction,
                'transaction_detail': transaction_detail,
                'token': token,
            }
            return render(request, 'cobro/mal.html', context)

@login_required(login_url='index')
def procesarorden(request, orden_id):

    if request.method == 'POST':

        orden = Orden.objects.get(pk=orden_id)

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
    # ver si ya tiene orden asociada
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
    else:
        orden = Orden(
            usuario=request.user,
            numerodeitems=contador,
            totalapagar=sumatotal
        )
        orden.save()

    # Agregar items a ordenitem
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

        # Agregar tocata a Carro
        item = Carro.objects.filter(tocata=tocata_id).filter(estado=parToca['pendiente'])

        if item:
            if item[0].cantidad == 2:
                messages.error(request,'Ya compraste dos entradas para esta Tocata Intima')
            else:
                if int(cantidad) == 2:
                    messages.error(request,'Ya compraste una entrada, solo puedes comprar una mas')
                else:
                    item[0].cantidad = 2
                    item[0].total = item[0].tocata.costo * 2
                    item[0].save()
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
