from django.shortcuts import render
from django.http import HttpResponse

from tocata.models import Tocata
from artista.models import Artista

from django.db.models import Q
from datetime import datetime

from toca.parametros import parToca

# Create your views here.
def index(request):

    tocatas, artistas = getTocatasArtistasHeadIndex();
    context = {
        'tocatas': tocatas,
        'artistas': artistas,
    }

    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')

def busqueda(request):

    queryset_list_tocatas = Tocata.objects.all()
    queryset_list_artistas = Artista.objects.all()
    if 'q' in request.GET:
        busqueda = request.GET['q']
        if busqueda:
            queryset_list_tocatas = Tocata.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )

            queryset_list_artistas = Artista.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )

    context = {
        'tocatas': queryset_list_tocatas,
        'artistas': queryset_list_artistas,
        'valores': request.GET,
    }

    return render(request, 'home/busqueda.html', context)

def getTocatasArtistasHeadIndex():

        hoy = datetime.today()
        tocatas = Tocata.objects.all()[:parToca['muestraTocatas']]
        for tocata in tocatas:
            diff = hoy - tocata.fecha_crea.replace(tzinfo=None)
            if diff.days <= parToca['diasNuevoTocata']:
                tocata.nuevo = 'SI'
            else:
                tocata.nuevo = 'NO'
            tocata.evaluacionRange = range(tocata.evaluacion)
            tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

        artistas = Artista.objects.all()[:parToca['muestraArtistas']]
        for artista in artistas:
            diff = hoy - artista.fecha_crea.replace(tzinfo=None)
            if diff.days <= parToca['diasNuevoArtista']:
                artista.nuevo = 'SI'
            else:
                artista.nuevo = 'NO'

        return tocatas, artistas
