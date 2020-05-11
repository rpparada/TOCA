from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages

from datetime import datetime
from django.utils import timezone
import operator

from .models import Tocata
from .forms import TocataForm
from artista.models import Artista
from lugar.models import Lugar
from usuario.models import UsuarioArtista

from home.views import getTocatasArtistasHeadIndex
from toca.parametros import parToca

# Create your views here.
def tocatas(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    hoy = datetime.today()
    tocatas = Tocata.objects.all()
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

    desc = str(tocata.artista.descripción)
    tocata.des_part1,tocata.des_part2 = desc[:round(len(desc)/2)], desc[round(len(desc)/2):]

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
    mistocatas = Tocata.objects.filter(artista=artista.artista)

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'mistocatas': mistocatas,
    }

    return render(request,'tocata/mistocatas.html', context)

def creartocata(request):

    if request.method == 'POST':

        form = TocataForm(request.POST)

        if form.is_valid():
            nuevaTocata = form.save(commit=False)

            if 'flayer_original' in request.FILES:
                nuevaTocata.flayer_original = request.FILES['flayer_original']
                nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
                nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

            nuevaTocata.usuario = request.user
            nuevaTocata.fecha_crea = timezone.now()
            nuevaTocata.fecha_actu = timezone.now()

            if nuevaTocata.lugar_def == parToca['cerrada']:
                nuevaTocata.estado = parToca['publicado']
            elif nuevaTocata.lugar_def == parToca['abierta']:
                nuevaTocata.estado = parToca['inicial']

            nuevaTocata.save()
            messages.success(request, 'Tocata creada exitosamente')
            return redirect('mistocatas')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    artista = UsuarioArtista.objects.get(user=request.user).artista
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    tocata_form = TocataForm();

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'artista': artista,
        'mislugares': mislugares,
        'tocata_form': tocata_form,
    }

    return render(request, 'tocata/creartocata.html', context)

def borrartocata(request, tocata_id):

    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.estado = parToca['suspendido']
    tocata.save()
    return redirect('mistocatas')

def proponerlugar(request, tocata_id):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    hoy = datetime.today()
    tocatas = Tocata.objects.all()
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

    return render(request, 'tocata/proponerlugar.html', context)
