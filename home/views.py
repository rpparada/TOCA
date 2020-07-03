from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from datetime import datetime
from itertools import chain

from tocata.models import Tocata, TocataAbierta
from artista.models import Artista
from usuario.models import Usuario
from home.models import Testimonios

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

    orden = 'fecha'
    filtro = 'todas'
    direccion = 'asc'
    busqueda = ' '
    if request.method == 'POST':
        orden = request.POST.get('orden')
        filtro = request.POST.get('filtro')
        direccion = request.POST.get('direccion')
        busqueda = request.POST.get('q2')

    if direccion == 'des':
        orden = '-' + orden

    queryset_list_tocatas = Tocata.objects.none()
    queryset_list_tocatasabiertas = TocataAbierta.objects.none()
    queryset_list_artistas = Artista.objects.none()

    if 'q' in request.GET:
        busqueda = request.GET['q']

    if busqueda:
        if filtro == 'todas':
            queryset_list_tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],]).order_by(orden)
            queryset_list_tocatas = queryset_list_tocatas.filter(
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
                tocata.tipo = 'cerrada'

            if orden != 'costo' and orden != '-costo':
                queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],]).order_by(orden)
            else:
                queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],]).order_by('fecha')

            queryset_list_tocatasabiertas = queryset_list_tocatasabiertas.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda) |
                Q(artista__nombre__icontains=busqueda)
            )
            for tocataabierta in queryset_list_tocatasabiertas:
                diff = datetime.today() - tocataabierta.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoTocata']:
                    tocataabierta.nuevo = 'SI'
                else:
                    tocataabierta.nuevo = 'NO'
                tocataabierta.tipo = 'abierta'

            queryset_list_artistas = Artista.objects.filter(estado=parToca['disponible']).order_by('nombre')
            queryset_list_artistas = queryset_list_artistas.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )
            for artista in queryset_list_artistas:
                diff = datetime.today() - artista.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoArtista']:
                    artista.nuevo = 'SI'
                else:
                    artista.nuevo = 'NO'
                artista.tipo = 'artista'

        elif filtro == 'cerradas':
            queryset_list_tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],]).order_by(orden)
            queryset_list_tocatas = queryset_list_tocatas.filter(
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
                tocata.tipo = 'cerrada'
        elif filtro == 'abiertas':
            if orden != 'costo' and orden != '-costo':
                queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],]).order_by(orden)
            else:
                queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],]).order_by('fecha')

            queryset_list_tocatasabiertas = queryset_list_tocatasabiertas.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda) |
                Q(artista__nombre__icontains=busqueda)
            )
            for tocataabierta in queryset_list_tocatasabiertas:
                diff = datetime.today() - tocataabierta.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoTocata']:
                    tocataabierta.nuevo = 'SI'
                else:
                    tocataabierta.nuevo = 'NO'
                tocataabierta.tipo = 'abierta'
        elif filtro == 'artistas':
            queryset_list_artistas = Artista.objects.filter(estado=parToca['disponible']).order_by('nombre')
            queryset_list_artistas = queryset_list_artistas.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )
            for artista in queryset_list_artistas:
                diff = datetime.today() - artista.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoArtista']:
                    artista.nuevo = 'SI'
                else:
                    artista.nuevo = 'NO'
                artista.tipo = 'artista'

    result_list = list(chain(queryset_list_tocatas, queryset_list_tocatasabiertas, queryset_list_artistas))

    paginador = Paginator(result_list, parToca['tocatas_pag'])
    pagina = request.GET.get('page')

    try:
        pagina_search = paginador.page(pagina)
    except PageNotAnInteger:
        pagina_search = paginador.page(1)
    except EmptyPage:
        pagina_search = paginador.page(paginador.num_pages)

    if orden[0] == '-':
        orden = orden[1:]
        
    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'resultado': pagina_search,
        'valores': busqueda,
        'orden': orden,
        'filtro': filtro,
        'direccion': direccion,
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
