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
