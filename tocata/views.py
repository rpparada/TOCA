from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages

from datetime import datetime
from django.utils import timezone
import operator

from .models import Tocata, LugaresTocata
from .forms import TocataForm, LugaresTocataForm
from artista.models import Artista
from lugar.models import Lugar, Comuna, Region
from usuario.models import UsuarioArtista

from home.views import getTocatasArtistasHeadIndex
from toca.parametros import parToca, parTocatas

# Create your views here.
def tocatas(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    hoy = datetime.today()
    tocatas = Tocata.objects.all().filter(estado__in=[parToca['inicial'],parToca['publicado'],parToca['confirmado'],])
    for tocata in tocatas:
        diff = hoy - tocata.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoTocata']:
            tocata.nuevo = 'SI'
        else:
            tocata.nuevo = 'NO'
        tocata.evaluacionRange = range(tocata.evaluacion)
        tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    paginador = Paginator(tocatas, parToca['tocatas_pag'])
    pagina = request.GET.get('page')
    pagina_tocatas = paginador.get_page(pagina)

    tocatas_evaluacion = sorted(tocatas, key=operator.attrgetter('evaluacion'), reverse=True)

    context = {
        'tocatas_vista': pagina_tocatas,
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'tocatas_evaluacion': tocatas_evaluacion[:3],
        'usuario': usuario,
    }

    return render(request, 'tocata/tocatas.html', context)

def tocata(request, tocata_id):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    #desc = str(tocata.artista.descripción)
    #tocata.des_part1,tocata.des_part2 = desc[:round(len(desc)/2)], desc[round(len(desc)/2):]

    context = {
        'tocata_vista': tocata,
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'usuario': usuario,
    }
    return render(request, 'tocata/tocata.html', context)

def mistocatas(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    artista = UsuarioArtista.objects.get(user=request.user)
    mistocatas = Tocata.objects.filter(artista=artista.artista).filter(estado__in=parTocatas['estado_tipos_vista'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'mistocatas': mistocatas,
    }

    return render(request,'tocata/mistocatas.html', context)

def creartocata(request):

    tocata_form = TocataForm();

    if request.method == 'POST':

        tocata_form = TocataForm(request.POST)

        if tocata_form.is_valid():

            nuevaTocata = tocata_form.save(commit=False)
            if 'flayer_original' in request.FILES:
                nuevaTocata.flayer_original = request.FILES['flayer_original']
                nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
                nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

            if nuevaTocata.lugar_def == parToca['cerrada']:
                nuevaTocata.estado = parToca['publicado']
                nuevaTocata.region = nuevaTocata.lugar.region
                nuevaTocata.comuna = nuevaTocata.lugar.comuna
                nuevaTocata.provincia = nuevaTocata.lugar.provincia
            elif nuevaTocata.lugar_def == parToca['abierta']:
                nuevaTocata.estado = parToca['inicial']

            nuevaTocata.usuario = request.user

            nuevaTocata.save()

            messages.success(request, 'Tocata creada exitosamente')
            return redirect('mistocatas')
        else:
            print(tocata_form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    artista = UsuarioArtista.objects.get(user=request.user).artista
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'artista': artista,
        'mislugares': mislugares,
        'tocata_form': tocata_form,
    }

    return render(request, 'tocata/creartocata.html', context)

def borrartocata(request, tocata_id):

    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.estado = parToca['borrado']
    tocata.save()
    return redirect('mistocatas')

def suspendertocata(request, tocata_id):

    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.estado = parToca['suspendido']
    tocata.save()
    return redirect('mistocatas')

def proponerlugar(request, tocata_id):

    if request.method == 'POST':
        form = LugaresTocataForm(request.POST)

        if form.is_valid():

            lugartocata = form.save(commit=False)
            if LugaresTocata.objects.filter(tocata=tocata_id).filter(lugar=lugartocata.lugar):

                messages.error(request,'Ya habias enviado este ligar para esta tocata')
            else:

                if Tocata.objects.filter(region=lugartocata.lugar.region).filter(comuna=lugartocata.lugar.comuna):

                    lugartocata.usuario = request.user
                    lugartocata.save()
                    messages.success(request, 'Lugar enviado al artista')
                    return redirect('tocatas')
                else:

                    messages.error(request,'Lugar no esta en la Region/Comuna')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(Tocata, pk=tocata_id)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'tocata': tocata,
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'mislugares': mislugares,
    }

    return render(request, 'tocata/proponerlugar.html', context)

def seleccionarPropuestas(request, tocata_id):

    if request.method == 'POST':
        form = LugaresTocataForm(request.POST)
        if form.is_valid():
            lugartocata = form.save(commit=False)
            lugartocata.estado = parToca['elegido']

            tocata = get_object_or_404(Tocata, pk=tocata_id)
            tocata.lugar = lugartocata.lugar
            tocata.comuna = lugartocata.lugar.comuna
            tocata.region = lugartocata.lugar.region
            tocata.provincia = lugartocata.lugar.provincia

            tocata.estado = parToca['publicado']
            tocata.lugar_def = parToca['cerrada']

            if lugartocata.lugar.capacidad < tocata.asistentes_min:
                tocata.asistentes_min = lugartocata.lugar.capacidad
                tocata.asistentes_max = lugartocata.lugar.capacidad
            else:
                tocata.asistentes_max = lugartocata.lugar.capacidad

            lugartocata.save()
            tocata.save()

            messages.success(request, 'Lugar enviado al artista')
            return redirect('mistocatas')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(Tocata, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocata=tocata)
    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)

def carga_comunas_tocata(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=int(region_id)).order_by('codigo')

    context = {
        'comunas_reg': comunas,
    }

    return render(request, 'tocata/comuna_dropdown_list_options_tocata.html', context)
