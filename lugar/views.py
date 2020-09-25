from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View, CreateView

from .models import Lugar, Region, Provincia, Comuna
from tocata.models import Tocata
from propuestaslugar.models import LugaresTocata

from .forms import LugarForm, RegionForm, ComunaForm

from toca.parametros import parToca

# Create your views here.

class MisLugaresListView(LoginRequiredMixin, ListView):

    template_name = 'lugar/mislugares.html'
    paginate_by = 12
    ordering = ['-fecha_crea']

    def get_queryset(self, *args, **kwargs):
        request = self.request

        mislugares = Lugar.objects.by_request(request)
        #tocataslugar = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
        tocataslugar = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])
        for milugar in mislugares:
            tocata = tocataslugar.filter(lugar=milugar).values('id','nombre')
            if tocata:
                milugar.borra = 'NO'
                milugar.tocata = tocata
            else:
                milugar.borra = 'SI'

        return mislugares


@login_required(login_url='index')
def misLugares(request):

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
        'mislugares': mislugares,
    }

    return render(request,'lugar/mislugares.html', context)


@login_required(login_url='index')
def agregarLugar(request):

    form = LugarForm(request.POST or None);

    if form.is_valid():

        nuevoLugar = form.save(commit=False)
        nuevoLugar.provincia = Comuna.objects.get(id=request.POST.get('comuna')).provincia
        nuevoLugar.usuario = request.user
        nuevoLugar.save()
        messages.success(request, 'Lugar agregado exitosamente')
        return redirect('lugar:mislugares')
    #else:
        #print(form.errors.as_data())
        #messages.error(request,'Error en form')

    context = {
        'form': form,
    }
    return render(request, 'lugar/agregarlugar.html', context)

@login_required(login_url='index')
def actualizarLugar(request, lugar_id):

    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, pk=lugar_id)
        lugar.descripción = request.POST.get('descripción')
        lugar.save()
        messages.success(request, 'Lugar editado exitosamente')

    return redirect('mislugares')



@login_required(login_url='index')
def mispropuestas(request):

    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)
    mispropuestas = mispropuestas.exclude(estado__in=[parToca['borrado']])

    context = {
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)

@login_required(login_url='index')
def cancelarpropuesta(request, propuesta_id):

    if request.method == 'POST':
        propuesta = get_object_or_404(LugaresTocata, pk=propuesta_id)
        if propuesta.estado == parToca['pendiente']:
            propuesta.estado = parToca['cancelado']
            propuesta.save()
        else:
            messages.success(request, 'Solo puede cancelar un propuesta cuando esta pendiente')

    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)
    mispropuestas = mispropuestas.exclude(estado__in=[parToca['borrado']])

    context = {
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)

@login_required(login_url='index')
def cancelarpropuestaelegida(request, propuesta_id):

    if request.method == 'POST':
        propuesta = get_object_or_404(LugaresTocata, pk=propuesta_id)
        tocata = Tocata.objects.get(pk=propuesta.tocataabierta.tocata.id)

        propuesta.estado = parToca['cancelado']
        propuesta.save()

        tocata.estado = parToca['suspendido']
        tocata.save()

        messages.success(request, 'Solo puede cancelar un propuesta cuando esta pendiente')

    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)
    mispropuestas = mispropuestas.exclude(estado__in=[parToca['borrado']])

    context = {
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)

@login_required(login_url='index')
def borrarpropuesta(request, propuesta_id):

    if request.method == 'POST':
        propuesta = get_object_or_404(LugaresTocata, pk=propuesta_id)
        if propuesta.estado in [parToca['noelegido'], parToca['cancelado'],parToca['completado']]:
            propuesta.estado = parToca['borrado']
            propuesta.save()
        else:
            messages.success(request, 'No puedes borrar un propuesta mintras tenga tocatas activas')

    mispropuestas = LugaresTocata.objects.filter(lugar__usuario=request.user)
    mispropuestas = mispropuestas.exclude(estado__in=[parToca['borrado']])

    context = {
        'mispropuestas': mispropuestas,
    }

    return render(request,'lugar/mispropuestas.html', context)

@login_required(login_url='index')
def borrarlugar(request, lugar_id):

    if request.method == 'POST':
        lugar = get_object_or_404(Lugar, pk=lugar_id)
        lugar.estado = parToca['noDisponible']
        lugar.save()

    return redirect('mislugares')

@login_required(login_url='index')
def carga_comunas_agregar(request):

    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region=region_id).order_by('nombre')
    context = {
        'comunas_reg': comunas,
    }
    return render(request, 'lugar/comuna_dropdown_list_options_agregar.html', context)

@login_required(login_url='index')
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
