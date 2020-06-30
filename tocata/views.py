from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from datetime import datetime

import operator

from .forms import TocataForm, LugaresTocataForm, TocataAbiertaForm

from .models import Tocata, LugaresTocata, TocataAbierta
from artista.models import Artista
from lugar.models import Lugar, Comuna, Region
from usuario.models import UsuarioArtista, Usuario

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca, parTocatas, parTocatasAbiertas

# Create your views here.
def tocatas(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    tocatas = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
    for tocata in tocatas:
        dif = datetime.today() - tocata.fecha_crea.replace(tzinfo=None)
        if dif.days <= parToca['diasNuevoTocata']:
            tocata.nuevo = 'SI'
        else:
            tocata.nuevo = 'NO'
        tocata.asistentes_dif = tocata.asistentes_max - tocata.asistentes_total

    tocatasAbiertas = TocataAbierta.objects.filter(estado__in=[parToca['publicado'],])
    for tocataAbierta in tocatasAbiertas:
        dif = datetime.today() - tocataAbierta.fecha_crea.replace(tzinfo=None)
        if dif.days <= parToca['diasNuevoTocata']:
            tocataAbierta.nuevo = 'SI'
        else:
            tocataAbierta.nuevo = 'NO'


    paginador = Paginator(tocatas, parToca['tocatas_pag'])
    pagina = request.GET.get('page')
    pagina_tocatas = paginador.get_page(pagina)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'tocatas_vista': pagina_tocatas,
    }

    return render(request, 'tocata/tocatas.html', context)

def tocata(request, tocata_id):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(Tocata, pk=tocata_id)
    tocata.asistentes_dif = tocata.asistentes_max - tocata.asistentes_total

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'tocata_vista': tocata,
    }
    return render(request, 'tocata/tocata.html', context)

def tocataabierta(request, tocata_id):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)

    context = {
        'tocatas_h': toc_head,
        'artistas_h': art_head,
        'usuario': usuario,
        'tocata_vista': tocata,
    }

    return render(request, 'tocata/tocataabierta.html', context)

@login_required(login_url='index')
def mistocatas(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    artista = UsuarioArtista.objects.get(user=request.user)
    tocatascerradas = Tocata.objects.filter(artista=artista.artista).filter(estado__in=parTocatas['estado_tipos_vista'])
    tocatasabiertas = TocataAbierta.objects.filter(artista=artista.artista).filter(estado__in=parTocatasAbiertas['estado_tipos_vista'])

    for tocataabierta in tocatasabiertas:
        tocataabierta.numeropropuestas  = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado=parToca['pendiente']).count()

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocatascerradas': tocatascerradas,
        'tocatasabiertas': tocatasabiertas,
    }

    return render(request,'tocata/mistocatas.html', context)

@login_required(login_url='index')
def creartocata(request):

    if request.user.is_authenticated:
        usuario = Usuario.objects.filter(user=request.user)[0]
    else:
        usuario = None

    context = {
        'usuario': usuario,
    }

    return render(request, 'tocata/creartocata.html', context)

@login_required(login_url='index')
def creartocatacerrada(request):

    tocata_form = TocataForm();

    if request.method == 'POST':

        tocata_form = TocataForm(request.POST)

        if tocata_form.is_valid():

            nuevaTocata = tocata_form.save(commit=False)
            if 'flayer_original' in request.FILES:
                nuevaTocata.flayer_original = request.FILES['flayer_original']
                nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
                nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

            nuevaTocata.estado = parToca['publicado']
            nuevaTocata.region = nuevaTocata.lugar.region
            nuevaTocata.comuna = nuevaTocata.lugar.comuna

            nuevaTocata.usuario = request.user
            nuevaTocata.artista = Artista.objects.get(usuario=request.user)

            nuevaTocata.asistentes_max = nuevaTocata.lugar.capacidad

            nuevaTocata.save()

            messages.success(request, 'Tocata creada exitosamente')
            return redirect('mistocatas')
        else:
            print(tocata_form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,

        'mislugares': mislugares,
        'tocata_form': tocata_form,
    }

    return render(request, 'tocata/creartocatacerrada.html', context)

@login_required(login_url='index')
def creartocataabierta(request):

    tocata_form = TocataAbiertaForm()

    if request.method == 'POST':
        tocata_form = TocataAbiertaForm(request.POST)
        if tocata_form.is_valid():

            nuevaTocata = tocata_form.save(commit=False)
            if 'flayer_original' in request.FILES:
                nuevaTocata.flayer_original = request.FILES['flayer_original']
                nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
                nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

            nuevaTocata.estado = parToca['publicado']
            nuevaTocata.usuario = request.user
            nuevaTocata.artista = Artista.objects.get(usuario=request.user)
            nuevaTocata.save()

            messages.success(request, 'Tocata Abierta creada')
            return redirect('mistocatas')
        else:
            print(tocata_form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    artista = UsuarioArtista.objects.get(user=request.user).artista

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'artista': artista,
        'tocata_form': tocata_form,
    }

    return render(request, 'tocata/creartocataabierta.html', context)

@login_required(login_url='index')
def detallestocata(request, tocata_id):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(Tocata, pk=tocata_id)

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocata': tocata,
    }

    return render(request, 'tocata/detallestocatacerrada.html', context)

@login_required(login_url='index')
def detallestocataabierta(request, tocata_id):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocata': tocata,
    }

    return render(request, 'tocata/detallestocataabierta.html', context)

@login_required(login_url='index')
def borrartocata(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(Tocata, pk=tocata_id)
        tocata.estado = parToca['borrado']
        tocata.save()

    return redirect('mistocatas')

@login_required(login_url='index')
def borrartocataabierta(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
        tocata.estado = parToca['borrado']
        tocata.save()

    return redirect('mistocatas')

@login_required(login_url='index')
def suspendertocata(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(Tocata, pk=tocata_id)
        tocata.estado = parToca['suspendido']
        tocata.save()

    return redirect('mistocatas')

@login_required(login_url='index')
def suspendertocataabierta(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
        tocata.estado = parToca['suspendido']
        tocata.save()

    return redirect('mistocatas')

@login_required(login_url='index')
def proponerlugar(request, tocata_id):

    if request.method == 'POST':
        form = LugaresTocataForm(request.POST)

        if form.is_valid():

            lugartocata = form.save(commit=False)
            if LugaresTocata.objects.filter(tocataabierta=tocata_id).filter(lugar=lugartocata.lugar).exclude(estado__in=[parToca['cancelado'],parToca['borrado']]):
                messages.error(request,'Ya habias enviado este lugar para esta tocata')
            else:
                tocataabierta = TocataAbierta.objects.get(pk=tocata_id)
                if tocataabierta.comuna.nombre == 'Todas':
                    if tocataabierta.region.nombre == lugartocata.lugar.region.nombre:
                        lugartocata.save()
                        messages.success(request, 'Lugar enviado al artista')
                        return redirect('index')
                    else:
                        messages.error(request,'Lugar no esta en la Region')
                else:
                    if tocataabierta.region.nombre == lugartocata.lugar.region.nombre\
                     and tocataabierta.comuna.nombre == lugartocata.lugar.comuna.nombre:
                     lugartocata.save()
                     messages.success(request, 'Lugar enviado al artista')
                     return redirect('index')
                    else:
                        messages.error(request,'Lugar no esta en la Region y/o Comuna')

        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'mislugares': mislugares,
        'tocata': tocata,
    }

    return render(request, 'tocata/proponerlugar.html', context)

@login_required(login_url='index')
def verpropuestas(request, tocata_id):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)

@login_required(login_url='index')
def seleccionarpropuestas(request, tocata_id, lugar_id):

    if request.method == 'POST':

        # Cambia estado de TocataAbierta a confirmado
        tocataabierta = get_object_or_404(TocataAbierta, pk=tocata_id)
        tocataabierta.estado = parToca['confirmado']

        # Cambia estado del lugar elegido a "Elegido"
        lugartocata = get_object_or_404(LugaresTocata, pk=lugar_id)
        lugartocata.estado = parToca['elegido']
        lugartocata.save()

        # Cambiar las otras propuestas a "no elegido"
        listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado=parToca['pendiente'])
        for lugar in listaLugares:
            lugar.estado = parToca['noelegido']
            lugar.save()

        # Define capacidades
        asis_min = tocataabierta.asistentes_min
        if lugartocata.lugar.capacidad < tocataabierta.asistentes_min:
            asis_min = lugartocata.lugar.capacidad
            asis_max = lugartocata.lugar.capacidad
        else:
            asis_max = lugartocata.lugar.capacidad

        # Costo
        costotocata = request.POST.get('costo')

        # Crear Tocata oficial (tabla Tocata)
        tocata = Tocata(
            artista=tocataabierta.artista,
            usuario=tocataabierta.usuario,
            nombre=tocataabierta.nombre,
            lugar=lugartocata.lugar,
            region=lugartocata.lugar.region,
            comuna=lugartocata.lugar.comuna,
            descripción=tocataabierta.descripción,
            costo=int(costotocata),
            fecha=tocataabierta.fecha,
            hora=tocataabierta.hora,
            asistentes_total=0,
            asistentes_min=asis_min,
            asistentes_max=asis_max,
            flayer_original=tocataabierta.flayer_original,
            flayer_1920_1280=tocataabierta.flayer_1920_1280,
            flayer_380_507=tocataabierta.flayer_380_507,
            evaluacion=0,
            estado=parToca['publicado'],
        )
        tocata.save()

        tocataabierta.tocata = tocata
        tocataabierta.save()

        messages.success(request, 'Lugar seleccionado con exito y Tocata publicada')
        return redirect('mistocatas')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)

@login_required(login_url='index')
def carga_comunas_tocata(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=int(region_id)).order_by('codigo')

    context = {
        'comunas_reg': comunas,
    }

    return render(request, 'tocata/comuna_dropdown_list_options_tocata.html', context)
