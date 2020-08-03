from django.shortcuts import render, redirect

from .models import CarroCompra
from orden.models import OrdenCompra
from tocata.models import Tocata

# Create your views here.
def carro_home(request):

    carro_obj, nuevo_carro = CarroCompra.objects.nuevo_or_entrega(request)

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

        carro_obj, nuevo_carro = CarroCompra.objects.nuevo_or_entrega(request)
        if tocata in carro_obj.tocata.all():
            carro_obj.tocata.remove(tocata)
        else:
            carro_obj.tocata.add(tocata)

        request.session['carro_tocatas'] = carro_obj.tocata.count()

    return redirect('carro')

def checkout_home(request):
    carro_obj, nuevo_carro = CarroCompra.objects.nuevo_or_entrega(request)
    orden_obj = None
    if nuevo_carro or carro_obj.tocata.count() == 0:
        return redirect('carro')
    else:
        orden_obj, nueva_orden = OrdenCompra.objects.get_or_create(carro=carro_obj)
        context = {
            'object': orden_obj
        }
        return render(request, 'carro/checkout.html', context)
