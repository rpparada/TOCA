from django.shortcuts import render
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TocataAbierta
from carro.models import CarroCompra

from .forms import TocataAbiertaForm

from toca.parametros import parToca

# Create your views here.
class TocataAbiertaListView(ListView):

    queryset = TocataAbierta.objects.disponible()
    paginate_by = parToca['tocatas_pag']
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
        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(self.request)

        context['carro'] = carro_obj
        context['orden'] = orden
        context['direccion'] = direccion

        return context


class TocataAbiertaDetailView(DetailView):

    queryset = TocataAbierta.objects.all()
    template_name = 'tocataabierta/tocataabierta.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataAbiertaDetailView, self).get_context_data(*args, **kwargs)

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
        tocatasabiertas = TocataAbierta.objects.tocataartista_by_request(request)

        return tocatasabiertas

    def get_context_data(self, *args, **kwargs):
        context = super(TocatasAbiertasArtistaListView, self).get_context_data(*args, **kwargs)
        return context

@login_required(login_url='index')
def creartocataabierta(request):

    form = TocataAbiertaForm(request.POST or None)

    if form.is_valid():

        nuevaTocata = form.save(commit=False)
        if 'flayer_original' in request.FILES:
            nuevaTocata.flayer_original = request.FILES['flayer_original']
            nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
            nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

        nuevaTocata.estado = parToca['publicado']
        nuevaTocata.usuario = request.user
        artista = Artista.objects.get(usuario=request.user)
        nuevaTocata.artista = artista
        nuevaTocata.save()

        nuevaTocata.estilos.set(artista.estilos.all())

        messages.success(request, 'Tocata Abierta creada')
        return redirect('mistocatas')
    #else:
    #    print(form.errors.as_data())
    #    messages.error(request,'Error en form')

    context = {
        'form': form,
    }

    return render(request, 'tocata/creartocataabierta.html', context)

@login_required(login_url='index')
def detallestocataabierta(request, tocata_id):

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)

    context = {
        'tocata': tocata,
    }

    return render(request, 'tocata/detallestocataabierta.html', context)

@login_required(login_url='index')
def borrartocataabierta(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
        tocata.estado = parToca['borrado']
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
def carga_comunas_tocata(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=int(region_id)).order_by('codigo')

    context = {
        'comunas_reg': comunas,
    }

    return render(request, 'tocata/comuna_dropdown_list_options_tocata.html', context)
