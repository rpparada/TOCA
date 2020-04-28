from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages

from datetime import datetime
import operator

from .models import Tocata, CompraTocata
from artista.models import Artista
from lugar.models import Lugar
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

    toc_head, art_head = getTocatasArtistasHeadIndex()

    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total

    desc = str(tocata.artista.descripción)
    tocata.des_part1,tocata.des_part2 = desc[:round(len(desc)/2)], desc[round(len(desc)/2):]

    context = {
        'tocata_vista': tocata,
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
    }
    return render(request, 'tocata/tocata.html', context)


# Cambiar a aplicacion de pago
def mediopago(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            usuario = request.user
            tocata_id = request.POST['tocata_id']
            tocata = Tocata.objects.get(id=tocata_id)

            ha_compradro = CompraTocata.objects.all().filter(usuario=usuario, tocata=tocata)
            if ha_compradro:
                messages.error(request,'Ya tienes tu entreda')
                return redirect('/tocatas/'+tocata_id)
            else:
                compra = CompraTocata(tocata=tocata, usuario=usuario, estado='AC')
                compra.save()

                # send_mail(
                #    'subject_Prueba',
                #    'body_Prueba',
                #    'rpparada@gmail.com',
                #    ['rpparada@gmail.com','rpparada@hotmail.com'],
                #    fail_silently=False
                #)

                messages.success(request, 'Compra exitosa')
                return render(request, 'tocata/mediopago.html')
    else:
        context = {
            'valores': request.POST
        }
        return render(request, 'usuario/ingresar.html', context)
