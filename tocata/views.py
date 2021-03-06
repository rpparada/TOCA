from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
                                DetailView,
                                ListView,
                                View,
                                CreateView,
                                UpdateView
                            )
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tocata
from carro.models import CarroCompra

from .forms import (
            CrearTocataForm,
            SuspenderTocataForm,
            BorrarTocataForm,
            TocataDesdeTocataAbiertaCreateForm,
            SeleccionarLugarTocataForm
        )
from lugar.forms import CrearLugarForm, CrearLugarPropuestaForm

from analytics.mixins import ObjectViewedMixin

from toca.mixins import NextUrlMixin, RequestFormAttachMixin

# Create your views here.
class TocataListView(ListView):

    queryset = Tocata.objects.disponible()
    paginate_by = 12
    template_name = 'tocata/tocatas.html'
    ordering = ['-fecha']

    def get_ordering(self):
        orden = self.request.GET.get('orden','fecha')
        direccion = self.request.GET.get('direccion','asc')
        if direccion == 'asc':
            return orden
        else:
            return '-'+orden

    def get_context_data(self, *args, **kwargs):
        context = super(TocataListView, self).get_context_data(*args, **kwargs)

        orden = self.request.GET.get('orden','fecha')
        direccion = self.request.GET.get('direccion','asc')

        context['orden'] = orden
        context['direccion'] = direccion

        return context

class TocataDetailView(DetailView):

    template_name = 'tocata/tocata.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataDetailView, self).get_context_data(*args, **kwargs)
        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(self.request)

        tocata = context['object']
        item = carro_obj.get_item(tocata)
        otras_tocatas = Tocata.objects.tocataartistadisponibles(tocata.artista).exclude(id=tocata.id)

        context['item'] = item
        context['listatocatascarro'] = carro_obj.get_tocata_list()
        context['tocata_list'] = otras_tocatas

        return context

    def get_object(self, queryset=None):

        request = self.request
        slug = self.kwargs.get('slug')

        try:
            tocata = Tocata.objects.get(slug=slug)
        except Tocata.DoesNotExist:
            raise Http404('Tocata No Encontrada')
        except Tocata.MultipleObjectsReturned:
            tocatas = Tocata.objects.filter(slug=slug)
            tocata = tocatas.first()
        except:
            raise Http404('Error Desconocido')

        return tocata

class TocatasArtistaListView(LoginRequiredMixin, ListView):

    queryset = None
    paginate_by = 10
    template_name = 'tocata/mistocatas.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        tocatas = Tocata.objects.tocataartista_by_request(request).order_by('fecha')

        return tocatas

    def get_context_data(self, *args, **kwargs):
        context = super(TocatasArtistaListView, self).get_context_data(*args, **kwargs)
        return context

class SuspenderTocataView(LoginRequiredMixin, View):

    form_class = SuspenderTocataForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            tocata = form.cleaned_data['tocata']
            tocata.suspender_tocata(request, 'artista')

        return redirect('tocata:mistocatas')

class BorrarTocataView(LoginRequiredMixin, View):

    form_class = BorrarTocataForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            tocata = form.cleaned_data['tocata']
            tocata.borrar_tocata()

        return redirect('tocata:mistocatas')

class TocataCreateView(NextUrlMixin, RequestFormAttachMixin, LoginRequiredMixin, CreateView):

    form_class = CrearTocataForm
    template_name = 'tocata/creartocata.html'

    def get_success_url(self):
        return reverse_lazy('tocata:seleccionardireccion', kwargs={'slug':self.object.slug})

class SeleccionarLugarTocataView(NextUrlMixin, RequestFormAttachMixin, LoginRequiredMixin, UpdateView):

    form_class = SeleccionarLugarTocataForm
    template_name = 'tocata/seleccionalugar.html'

    def get_object(self):
        return Tocata.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, *args, **kwargs):
        context = super(SeleccionarLugarTocataView, self).get_context_data(*args, **kwargs)

        tocata = Tocata.objects.get(slug=self.kwargs['slug'])
        context['tocata'] = tocata
        context['form_lugar'] = CrearLugarForm(self.request)

        return context

    def form_valid(self, form):
        request = self.request
        msg = 'Tocata Íntima publicada'
        messages.success(request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        request = self.request
        msg = 'Error en formulario'
        messages.error(request, msg)
        return super().form_invalid(form)

class AgregarYSeleccionaDireccionView(LoginRequiredMixin ,View):

    form_class = CrearLugarForm

    def post(self, request, *args, **kwargs):
        tocata_id = request.POST.get('tocata')
        tocata = Tocata.objects.get(id=tocata_id)
        form = self.form_class(request, request.POST or none)
        if form.is_valid():
            # Direccion salvada
            lugar = form.save()

            # Agrega dirección a tocata y publicar
            tocata.agrega_lugar(lugar)
            tocata.publicar()

            msg = 'Tocata Íntima publicada'
            messages.success(request, msg)

        #return redirect('propuestaslugar:mispropuestas')
        #return reverse_lazy('tocata:tocata', kwargs={'slug':tocata.slug})
        return redirect('tocata:tocata', slug=tocata.slug)

class TocataDesdeTocataAbiertaCreateView(RequestFormAttachMixin, LoginRequiredMixin, CreateView):

    form_class = TocataDesdeTocataAbiertaCreateForm
    template_name = 'tocata/creartocatadesdetocataabierta.html'

    def form_valid(self, form):
        request = self.request
        msg = 'Tocata publicada'
        messages.success(request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        request = self.request
        msg = 'Error en formulario'
        messages.error(request, msg)
        return super().form_invalid(form)

class UserTocatasHistoryView(LoginRequiredMixin, ListView):

    template_name = 'tocata/historico-user-tocatas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserTocatasHistoryView, self).get_context_data(*args, **kwargs)

        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Tocata)

        return views
