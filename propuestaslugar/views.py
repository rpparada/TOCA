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
from lugar.models import Lugar, Comuna

from .forms import (
                CancelarPropuestaForm,
                BorrarPropuestaForm,
                CancelarPropuestaElegidaForm,
                ProponerLugarForm,
                SeleccionarPropuestasForm
            )
from lugar.forms import CrearLugarForm, CrearLugarPropuestaForm
from tocata.forms import TocataDesdeTocataAbiertaCreateForm

from toca.mixins import NextUrlMixin, RequestFormAttachMixin

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
        context['form_lugar'] = CrearLugarPropuestaForm(self.request, tocataabierta)

        return context

class SeleccionarLugarView(LoginRequiredMixin, View):

    form_class = ProponerLugarForm

    def post(self, request, *args, **kwargs):
        tocataabierta_id = request.POST.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)

        form = self.form_class(request, tocataabierta, request.POST or None)
        if form.is_valid():
            tocataabierta = form.cleaned_data['tocataabierta']
            lugar = form.cleaned_data['lugar']
            # Verificar si ya se envio propuesta
            propuesta, created = LugaresTocata.objects.new_or_get(tocataabierta, lugar)
            if not created:
                messages.error(request,'Ya habias enviado este lugar para esta tocata')

        return redirect('propuestaslugar:mispropuestas')

class AgregarYSeleccionarLugar(LoginRequiredMixin ,View):

    form_class = CrearLugarPropuestaForm

    def post(self, request, *args, **kwargs):
        tocataabierta_id = request.POST.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)
        form = self.form_class(request, tocataabierta, request.POST or none)
        if form.is_valid():
            # Direccion salvada
            lugar = form.save()

            #Crear Propuesta con nueva direccion
            propuesta, created = LugaresTocata.objects.new_or_get(tocataabierta, lugar)

        else:
            print('error')

        return redirect('propuestaslugar:mispropuestas')

class VerPropuestasLitsView(LoginRequiredMixin, ListView):

    template_name = 'propuestaslugar/propuestas.html'
    paginate_by = 12

    def get_queryset(self):
        tocataabierta_id = self.request.GET.get('tocataabierta')
        lugares = LugaresTocata.objects.ver_propuestas(tocataabierta_id)

        return lugares

    def get_context_data(self, *args, **kwargs):
        context = super(VerPropuestasLitsView, self).get_context_data(*args, **kwargs)

        tocataabierta_id = self.request.GET.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)
        context['tocataabierta'] = tocataabierta
        context['form_tocata'] = TocataDesdeTocataAbiertaCreateForm(self.request or None)

        return context
