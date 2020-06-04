from django.shortcuts import render, get_object_or_404

from datetime import datetime

from .models import Artista
from tocata.models import Tocata

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca, parTocatas

# Create your views here.
def artistas(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    artistas_vista = Artista.objects.filter(estado=parToca['disponible'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'artistas': artistas_vista
    }

    return render(request, 'artista/artistas.html', context)

def artista(request, artista_id):

    artista = get_object_or_404(Artista, pk=artista_id)
    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    tocatas_art = Tocata.objects.filter(estado__in=[parToca['inicial'],parToca['publicado'],parToca['confirmado'],])
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
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocatas_art': tocatas_art,
        'artista': artista,
    }
    return render(request, 'artista/artista.html', context)
