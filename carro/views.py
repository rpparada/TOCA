from django.shortcuts import render, redirect

from .models import CarroCompra
from tocata.models import Tocata

from home.utils import getDataHeadIndex

# Create your views here.
def carro_home(request):

    usuario, numitemscarro = getDataHeadIndex(request)
    carro_obj, nuevo_carro = CarroCompra.objects.nuevo_or_entrega(request)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
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
