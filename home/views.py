from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from tocata.models import Tocata, TocataAbierta
from artista.models import Artista
from usuario.models import Usuario
from home.models import Testimonios

from django.db.models import Q
from datetime import datetime

from toca.parametros import parToca

# Create your views here.
def index(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],])
    tocatasabiertas = tocatasabiertas.filter(fecha__gte=datetime.today()).order_by('-fecha_crea')[:parToca['muestraTocatas']]

    testimonios = Testimonios.objects.filter(estado=parToca['disponible'])
    testimonios_art = testimonios.filter(objetivo=parToca['artistas'])[:3]
    testimonios_usu = testimonios.filter(objetivo=parToca['usuarios'])[:3]

    context = {
        # Cabecera
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        # Tocatas y Tocatas Abiertas nuevas
        'tocatas': tocatas,
        'tocatasabiertas': tocatasabiertas,
        # Artistas
        'artistas': artistas,
        # Testimonios
        'testimonios_art': testimonios_art,
        'testimonios_usu': testimonios_usu,
    }

    return render(request, 'home/index.html', context)

def busqueda(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    queryset_list_tocatas = Tocata.objects.filter(estado__in=[parToca['inicial'],parToca['publicado'],parToca['confirmado'],])

    if 'q' in request.GET:
        busqueda = request.GET['q']
        if busqueda:
            queryset_list_tocatas = Tocata.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda) |
                Q(artista__nombre__icontains=busqueda)
            )

            for tocata in queryset_list_tocatas:
                diff = datetime.today() - tocata.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoTocata']:
                    tocata.nuevo = 'SI'
                else:
                    tocata.nuevo = 'NO'
                tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    paginador = Paginator(queryset_list_tocatas, parToca['tocatas_pag'])
    pagina = request.GET.get('page')

    try:
        pagina_search = paginador.page(pagina)
    except PageNotAnInteger:
        pagina_search = paginador.page(1)
    except EmptyPage:
        pagina_search = paginador.page(paginador.num_pages)

    print(pagina_search)
    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'resultado': pagina_search,
        'valores': request.GET,
    }

    return render(request, 'home/busqueda.html', context)

def getTocatasArtistasHeadIndex(request):

    tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
    tocatas = tocatas.filter(fecha__gte=datetime.today()).order_by('-fecha_crea')[:parToca['muestraTocatas']]
    for tocata in tocatas:
        diff = datetime.today() - tocata.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoTocata']:
            tocata.nuevo = 'SI'
        else:
            tocata.nuevo = 'NO'
        tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    artistas = Artista.objects.filter(estado=parToca['disponible'])
    artistas = artistas.exclude(usuario__isnull=True).order_by('-fecha_crea')[:parToca['muestraArtistas']]
    for artista in artistas:
        diff = datetime.today() - artista.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoArtista']:
            artista.nuevo = 'SI'
        else:
            artista.nuevo = 'NO'
    if request.user.is_authenticated:
        usuario = Usuario.objects.filter(user=request.user)[0]
    else:
        usuario = None

    return tocatas, artistas, usuario
