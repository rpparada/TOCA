from django.shortcuts import render
from django.http import HttpResponse

from tocata.models import Tocata
from artista.models import Artista
from usuario.models import Usuario

from django.db.models import Q
from datetime import datetime

from toca.parametros import parToca

# Create your views here.
def index(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    context = {
        'tocatas': tocatas,
        'artistas': artistas,
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
    }

    return render(request, 'home/index.html', context)

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

def getTocatasArtistasHeadIndex(request):

    hoy = datetime.today()
    tocatas = Tocata.objects.all().order_by('-fecha_crea')[:parToca['muestraTocatas']]
    for tocata in tocatas:
        diff = hoy - tocata.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoTocata']:
            tocata.nuevo = 'SI'
        else:
            tocata.nuevo = 'NO'
        tocata.evaluacionRange = range(tocata.evaluacion)
        tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    artistas = Artista.objects.all().order_by('-fecha_crea')[:parToca['muestraArtistas']]
    for artista in artistas:
        diff = hoy - artista.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoArtista']:
            artista.nuevo = 'SI'
        else:
            artista.nuevo = 'NO'

    if request.user.is_authenticated:
        usuario = Usuario.objects.filter(user=request.user)[0]
    else:
        usuario = None

    return tocatas, artistas, usuario
