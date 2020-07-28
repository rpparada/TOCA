from django.shortcuts import render, get_object_or_404

from datetime import datetime

from .models import Artista
from tocata.models import Tocata

from home.utils import getDataHeadIndex

from toca.parametros import parToca, parTocatas

# Create your views here.
def artistas(request):

    usuario, numitemscarro = getDataHeadIndex(request)

    artistas_vista = Artista.objects.filter(estado=parToca['disponible'])

    for art in artistas_vista:
        art.cats = art.estilos.split()

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'artistas': artistas_vista
    }

    return render(request, 'artista/artistas.html', context)

def artista(request, artista_id):

    artista = get_object_or_404(Artista, pk=artista_id)
    usuario, numitemscarro = getDataHeadIndex(request)

    tocatas_art = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado']])
    tocatas_art = tocatas_art.filter(artista=artista_id)
    hoy = datetime.today()
    for tocata_art in tocatas_art:
        diff = hoy - tocata_art.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoTocata']:
            tocata_art.nuevo = 'SI'
        else:
            tocata_art.nuevo = 'NO'
        tocata_art.asistentes_diff = tocata_art.asistentes_max - tocata_art.asistentes_total

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'tocatas_art': tocatas_art,
        'artista': artista,
    }
    return render(request, 'artista/artista.html', context)
