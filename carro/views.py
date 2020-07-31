from django.shortcuts import render

from .models import CarroCompra

# Create your views here.
def carro_home(request):

    carro_id =request.session.get("carro_id", None)
    #if carro_id is None and isinstance(carro_id, int):
    if carro_id is None:
        print('nuevo')
        carro_obj = CarroCompra.objects.create(usuario=None)
        request.session['carro_id'] = carro_obj.id
    else:
        print('existe')
        carro_obj = CarroCompra.objects.get(id=carro_id)

    return render(request, 'carro/carro_home.html', {})
