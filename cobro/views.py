from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cobro.models import Carro
from tocata.models import Tocata

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca, parCarro

# Create your views here.
@login_required(login_url='index')
def micarro(request):

    toc_head, art_head, usuario, numitemscarro = getTocatasArtistasHeadIndex(request)

    listacarro = Carro.objects.filter(usuario=request.user).filter(estado=parToca['pendiente'])

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'listacarro': listacarro,
    }

    return render(request, 'cobro/micarro.html', context)

@login_required(login_url='index')
def agregaracarro(request, tocata_id):

    if request.method == 'POST':

        next = request.POST.get('next', '/')
        cantidad = request.POST.get('numeroentradas')

        # Agregar tocata a Carro
        try:
            item = Carro.objects.get(tocata=tocata_id)
        except Carro.DoesNotExist:
            item = None
        #item = Carro.objects.get(tocata=tocata_id)
        if item:
            if item.cantidad == 2:
                messages.error(request,'Ya compraste dos entradas para esta Tocata Intima')
            else:
                if int(cantidad) == 2:
                    messages.error(request,'Ya compraste una entrada, solo puedes comprar una mas')
                else:
                    item.cantidad = 2
                    item.total = item.tocata.costo * 2
                    item.save()
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
