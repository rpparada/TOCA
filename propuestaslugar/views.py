from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                                DetailView,
                                ListView,
                                View,
                                CreateView
                            )

from .models import LugaresTocata
from tocataabierta.models import TocataAbierta
from lugar.models import Lugar

from .forms import (
                CancelarPropuestaForm,
                BorrarPropuestaForm,
                CancelarPropuestaElegidaForm,
                ProponerLugarForm
            )
from lugar.forms import CrearLugarForm

# Create your views here.
class MisPropuestasListView(LoginRequiredMixin, ListView):
    template_name = 'propuestaslugar/mispropuestas.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        request = self.request
        mis_propuestas = LugaresTocata.objects.mis_propuestas_by_request(request)
        return mis_propuestas

class CancelarPropuestaView(LoginRequiredMixin, View):

    form_class = CancelarPropuestaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.cancelar()

        return redirect('propuestaslugar:mispropuestas')

class BorrarPropuestaView(LoginRequiredMixin, View):

    form_class = BorrarPropuestaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.borrar()

        return redirect('propuestaslugar:mispropuestas')

class CancelarPropuestaElegidaView(LoginRequiredMixin, View):

    form_class = CancelarPropuestaElegidaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.cancelar_elegido()

            # Suspender Tocata Abierta
            # Este proceso tambien suspende Tocata Publicada
            propuesta.tocataabierta.suspender_tocata_confirmado()

        return redirect('propuestaslugar:mispropuestas')


class ProponerLugarListView(LoginRequiredMixin, ListView):

    template_name = 'propuestaslugar/prestalacasa.html'
    #paginate_by = 12

    def get_queryset(self):
        request = self.request

        tocataabierta_id = request.GET.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)

        lugares = Lugar.objects.none()
        if tocataabierta.comuna.nombre == 'Todas':
            # Buscar por region
            lugares = Lugar.objects.by_region(tocataabierta, request)
        else:
            # Buscar por comuna
            lugares = Lugar.objects.by_comuna(tocataabierta, request)

        return lugares

    def get_context_data(self, *args, **kwargs):
        context = super(ProponerLugarListView, self).get_context_data(*args, **kwargs)

        tocataabierta_id = self.request.GET.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)

        context['tocataabierta'] = tocataabierta
        context['form_prestalacasa'] = ProponerLugarForm(self.request or None, tocataabierta or None)
        context['form_lugar'] = CrearLugarForm(self.request)

        return context

# class ProponerLugarView(LoginRequiredMixin, View):
#
#     form_class = ProponerLugarForm
#     template_name = 'propuestaslugar/prestalacasa.html'
#
#     def post(self, request, *args, **kwargs):
#         tocataabierta_id = request.POST.get('tocataabierta')
#         tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)
#
#         form = self.form_class(request, tocataabierta, request.POST or None)
#         if form.is_valid():
#             tocataabierta = form.cleaned_data['tocataabierta']
#             lugar = form.cleaned_data['lugar']
#             # Verificar si ya se envio propuesta
#             propuesta, created = LugaresTocata.objects.new_or_get(tocataabierta, lugar)
#             if not created:
#                 messages.error(request,'Ya habias enviado este lugar para esta tocata')
#
#         return redirect('propuestaslugar:mispropuestas')

class VerPropuestasLitsView(LoginRequiredMixin, ListView):

    template_name = 'propuestaslugar/propuestas.html'
    paginate_by = 12

    def get_queryset(self):
        tocataabierta_id = self.request.GET.get('tocataabierta')
        lugares = LugaresTocata.objects.filter(tocataabierta=tocataabierta_id).filter(estado='pendiente')

        return lugares

    def get_context_data(self, *args, **kwargs):
        context = super(VerPropuestasLitsView, self).get_context_data(*args, **kwargs)

        tocataabierta_id = self.request.GET.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)
        context['tocataabierta'] = tocataabierta

        return context

@login_required(login_url='index')
def verpropuestas(request, tocata_id):

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
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

        tocata.estilos.set(tocataabierta.artista.estilos.all())

        tocataabierta.tocata = tocata
        tocataabierta.save()

        messages.success(request, 'Lugar seleccionado con exito y Tocata publicada')
        return redirect('mistocatas')

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)
