from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from datetime import datetime
from itertools import chain
from operator import attrgetter

from tocata.models import Tocata, TocataAbierta
from artista.models import Artista
from usuario.models import Usuario
from home.models import Testimonio
from cobro.models import Carro
from carro.models import CarroCompra

from toca.parametros import parToca

# Create your views here.
def index(request):

    #tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
    tocatas = Tocata.objects.disponible()
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

    tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],])
    tocatasabiertas = tocatasabiertas.filter(fecha__gte=datetime.today()).order_by('-fecha_crea')[:parToca['muestraTocatas']]

    testimonios = Testimonio.objects.filter(estado=parToca['disponible'])
    testimonios_art = testimonios.filter(objetivo=parToca['artistas'])[:3]
    testimonios_usu = testimonios.filter(objetivo=parToca['usuarios'])[:3]

    carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(request)

    context = {
        # Tocatas y Tocatas Abiertas nuevas
        'tocatas': tocatas,
        'tocatasabiertas': tocatasabiertas,
        # Artistas
        'artistas': artistas,
        # Carro
        'carro': carro_obj,
        # Testimonios
        'testimonios_art': testimonios_art,
        'testimonios_usu': testimonios_usu,
    }

    return render(request, 'home/index.html', context)

def busqueda(request):

    orden = 'fecha'
    filtro = 'todas'
    direccion = 'asc'
    busqueda = ' '
    if request.method == 'POST':
        orden = request.POST.get('orden')
        filtro = request.POST.get('filtro')
        direccion = request.POST.get('direccion')
        busqueda = request.POST.get('q2')

    queryset_list_tocatas = Tocata.objects.none()
    queryset_list_tocatasabiertas = TocataAbierta.objects.none()

    if 'q' in request.GET:
        busqueda = request.GET['q']

    if busqueda:
        if filtro == 'todas':
            queryset_list_tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
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

            queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],])
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

        elif filtro == 'cerradas':
            queryset_list_tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
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
            queryset_list_tocatasabiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],])
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

    if direccion == 'asc':
        result_list = sorted(chain(queryset_list_tocatas, queryset_list_tocatasabiertas,), key=attrgetter(orden), reverse=False)
    else:
        result_list = sorted(chain(queryset_list_tocatas, queryset_list_tocatasabiertas,), key=attrgetter(orden), reverse=True)

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
        'resultado': pagina_search,
        'valores': busqueda,
        'orden': orden,
        'filtro': filtro,
        'direccion': direccion,
    }

    return render(request, 'home/busqueda.html', context)
