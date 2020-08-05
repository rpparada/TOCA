from django.shortcuts import render, redirect

from .models import CarroCompra
from orden.models import OrdenCompra
from tocata.models import Tocata
from facturacion.models import FacturacionProfile

from direccion.forms import DireccionForm

from usuario.forms import IngresarForm

# Create your views here.
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
        else:
            carro_obj.tocata.add(tocata)

        request.session['carro_tocatas'] = carro_obj.tocata.count()

    return redirect('carro')

def checkout_home(request):
    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)
    orden_obj = None
    if nuevo_carro or carro_obj.tocata.count() == 0:
        return redirect('carro')

    ingreso_form = IngresarForm()
    direccion_form = DireccionForm()
    facturacion_form = DireccionForm()

    fact_profile, fact_profile_created = FacturacionProfile.objects.new_or_get(request)

    if fact_profile is not None:
        orden_obj, orden_obj_created = OrdenCompra.objects.new_or_get(fact_profile, carro_obj)

    context = {
        'object': orden_obj,
        'fact_profile': fact_profile,
        'form': ingreso_form,
        'direccion_form': direccion_form,
        'facturacion_form': facturacion_form
    }
    return render(request, 'carro/checkout.html', context)
