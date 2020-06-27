from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Lugar, Region, Provincia, Comuna
from .forms import LugarForm, RegionForm, ComunaForm
from tocata.models import Tocata, LugaresTocata

from home.views import getTocatasArtistasHeadIndex
from toca.parametros import parToca

# Create your views here.
@login_required
def agregarLugar(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    lugar_form = LugarForm();

    if request.method == 'POST':
        lugar_form = LugarForm(request.POST)

        if lugar_form.is_valid():
            nuevoLugar = lugar_form.save(commit=False)
            nuevoLugar.provincia = Comuna.objects.get(id=request.POST.get('comuna')).provincia
            nuevoLugar.usuario = request.user
            nuevoLugar.save()
            messages.success(request, 'Lugar agregado exitosamente')
            return redirect('mislugares')
        else:
            print(lugar_form.errors.as_data())
            messages.error(request,'Error en form')

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'lugar_form': lugar_form,
    }
    return render(request, 'lugar/agregarlugar.html', context)

@login_required
def actualizarLugar(request, lugar_id):

    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, pk=lugar_id)
        lugar.descripción = request.POST.get('descripción')
        lugar.save()
        messages.success(request, 'Lugar editado exitosamente')

    return redirect('mislugares')

@login_required
def misLugares(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])
    tocataslugar = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])

    for milugar in mislugares:
        tocata = tocataslugar.filter(lugar=milugar).values('id','nombre')
        if tocata:
            milugar.borra = 'NO'
            milugar.tocata = tocata
        else:
            milugar.borra = 'SI'

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'mislugares': mislugares,
    }

    return render(request,'lugar/mislugares.html', context)

@login_required
def mispropuestas(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)

    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)

def cancelarpropuesta(request, propuesta_id):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)

    context = {
        'tocatas_h': tocatas,
        'artistas_h': artistas,
        'usuario': usuario,
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)



@login_required
def borrarlugar(request, lugar_id):

    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, pk=lugar_id)
        lugar.estado = parToca['noDisponible']
        lugar.save()

    return redirect('mislugares')

@login_required
def carga_comunas_agregar(request):

    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
    context = {
        'comunas_reg': comunas,
    }
    return render(request, 'lugar/comuna_dropdown_list_options_agregar.html', context)

@login_required
def carga_comunas_actualizar(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')

    if comuna_id.isdigit():
        context = {
            'comunas_reg': comunas,
            'comuna_id': int(comuna_id),
        }
    else:
        context = {
            'comunas_reg': comunas,
            'comuna_id': comunas.first(),
        }

    return render(request, 'lugar/comuna_dropdown_list_options_actualizar.html', context)
