from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import DetailView, ListView, View, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import TocataAbierta
from tocata.models import Tocata
from lugar.models import Comuna

from .forms import (
                CrearTocataAbiertaForm,
                SuspenderTocataAbiertaForm,
                BorrarTocataAbiertaForm
            )

from toca.mixins import NextUrlMixin, RequestFormAttachMixin

from toca.parametros import parToca

# Create your views here.
class TocataAbiertaListView(ListView):

    queryset = TocataAbierta.objects.disponible()
    paginate_by = 12
    template_name = 'tocataabierta/tocatasabiertas.html'
    ordering = ['-fecha']

    def get_ordering(self):
        orden = self.request.GET.get('orden','fecha')
        direccion = self.request.GET.get('direccion','asc')
        if direccion == 'asc':
            return orden
        else:
            return '-'+orden

    def get_context_data(self, *args, **kwargs):
        context = super(TocataAbiertaListView, self).get_context_data(*args, **kwargs)

        orden = self.request.GET.get('orden','fecha')
        direccion = self.request.GET.get('direccion','asc')

        context['orden'] = orden
        context['direccion'] = direccion

        return context


class TocataAbiertaDetailView(DetailView):

    template_name = 'tocataabierta/tocataabierta.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataAbiertaDetailView, self).get_context_data(*args, **kwargs)

        tocataabierta = context['object']
        otras_tocatas = Tocata.objects.tocataartistadisponibles(tocataabierta.artista)

        context['tocata_list'] = otras_tocatas

        return context

    def get_object(self, queryset=None):

        request = self.request
        slug = self.kwargs.get('slug')

        try:
            tocataabierta = TocataAbierta.objects.get(slug=slug)
        except TocataAbierta.DoesNotExist:
            raise Http404('Tocata No Encontrada')
        except TocataAbierta.MultipleObjectsReturned:
            tocataabiertas = Tocata.objects.filter(slug=slug)
            tocataabierta = tocataabiertas.first()
        except:
            raise Http404('Error Desconocido')

        return tocataabierta

class TocatasAbiertasArtistaListView(LoginRequiredMixin, ListView):

    paginate_by = 12
    template_name = 'tocataabierta/mistocatasabiertas.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        tocatasabiertas = TocataAbierta.objects.tocataartista_by_request(request).order_by('fecha')

        return tocatasabiertas

    def get_context_data(self, *args, **kwargs):
        context = super(TocatasAbiertasArtistaListView, self).get_context_data(*args, **kwargs)
        return context

class TocataAbiertaCreateView(NextUrlMixin, RequestFormAttachMixin, LoginRequiredMixin, CreateView):

    form_class = CrearTocataAbiertaForm
    template_name = 'tocataabierta/creartocataabierta.html'

    def form_valid(self, form):
        request = self.request
        msg = 'Busqueda publicada'
        messages.success(request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        request = self.request
        msg = 'Error en formulario'
        messages.error(request, msg)
        return super().form_invalid(form)

class SuspenderTocataAbiertaView(LoginRequiredMixin, View):
    form_class = SuspenderTocataAbiertaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            tocataabierta = form.cleaned_data['tocataabierta']
            tocataabierta.suspender_tocata()

        return redirect('tocataabierta:mistocatasabiertas')

class BorrarTocataAbiertaView(LoginRequiredMixin, View):
    form_class = BorrarTocataAbiertaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            tocata = form.cleaned_data['tocataabierta']
            tocata.borrar_tocata()

        return redirect('tocataabierta:mistocatasabiertas')

@login_required(login_url='index')
def carga_comunas_tocata(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=int(region_id)).order_by('codigo')

    context = {
        'comunas_reg': comunas,
    }

    return render(request, 'tocata/comuna_dropdown_list_options_tocata.html', context)
