from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cobro.models import Carro

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca, parCarro

# Create your views here.
@login_required(login_url='index')
def micarro(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    listacarro = Carro.objects.filter(usuario=request.user).filter(estado=parToca['pendiente'])

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'listacarro': listacarro,
    }

    return render(request, 'cobro/micarro.html', context)
