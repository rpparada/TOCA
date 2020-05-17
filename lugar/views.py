from django.shortcuts import render, redirect, get_object_or_404
from .models import Lugar, Region, Provincia, Comuna
from .forms import LugarForm, RegionForm, ComunaForm
from django.contrib import messages

from django.utils import timezone

from home.views import getTocatasArtistasHeadIndex
from toca.parametros import parToca

# Create your views here.
def agregarLugar(request):

    if request.method == 'POST':
        form = LugarForm(request.POST)

        if form.is_valid():
            nuevoLugar = form.save(commit=False)
            nuevoLugar.provincia = Comuna.objects.get(id=request.POST.get('comuna')).provincia
            nuevoLugar.usuario = request.user
            nuevoLugar.save()
            messages.success(request, 'Lugar agregado exitosamente')
            return redirect('mislugares')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    lugar_form = LugarForm();

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'lugar_form': lugar_form,
    }

    return render(request, 'lugar/agregarlugar.html', context)


def atualizarLugar(request, lugar_id):

    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, pk=lugar_id)
        form = LugarForm(request.POST, instance=lugar)
        if form.is_valid():
            lugarActualizado = form.save(commit=False)
            lugarActualizado.provincia = Comuna.objects.get(id=request.POST.get('comuna')).provincia
            lugarActualizado.save()
            messages.success(request, 'Lugar editado exitosamente')
            return redirect('mislugares')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    lugar_form = LugarForm(instance=lugar);
    regcom_form = LugarForm();

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'lugar': lugar,
        'regcom_form': regcom_form
    }

    return render(request,'lugar/detalleslugar.html', context)

def detalleslugar(request, lugar_id):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    lugar = get_object_or_404(Lugar, pk=lugar_id)

    regcom_form = LugarForm();

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'lugar': lugar,
        'regcom_form': regcom_form
    }

    return render(request,'lugar/detalleslugar.html', context)


def misLugares(request):

    tocatas, artistas, usuario = getTocatasArtistasHeadIndex(request)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'tocatas_h': tocatas[:3],
        'artistas_h': artistas[:3],
        'usuario': usuario,
        'mislugares': mislugares,
    }

    return render(request,'lugar/mislugares.html', context)

def borrarlugar(request, lugar_id):

    lugar = get_object_or_404(Lugar, pk=lugar_id)
    lugar.estado = parToca['noDisponible']
    lugar.save()
    return redirect('mislugares')


def carga_comunas_agregar(request):

    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
    context = {
        'comunas_reg': comunas,
    }
    return render(request, 'lugar/comuna_dropdown_list_options_agregar.html', context)

def carga_comunas_actualizar(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
    context = {
        'comunas_reg': comunas,
        'comuna_id': int(comuna_id),
    }
    return render(request, 'lugar/comuna_dropdown_list_options_actualizar.html', context)
