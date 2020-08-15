from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.http import Http404

from itertools import chain
from operator import attrgetter

from .models import Tocata
from tocataabierta.models import TocataAbierta
from propuestaslugar.models import LugaresTocata
from artista.models import Artista
from lugar.models import Lugar, Comuna, Region
from usuario.models import UsuarioArtista, Usuario
from carro.models import CarroCompra

from .forms import TocataForm
from tocataabierta.forms import TocataAbiertaForm
from propuestaslugar.forms import LugaresTocataForm

from toca.parametros import parToca, parTocatas, parTocatasAbiertas

# Create your views here.
class TocataListView(ListView):

    queryset = Tocata.objects.disponible()
    paginate_by = parToca['tocatas_pag']
    template_name = 'tocata/tocatas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataListView, self).get_context_data(*args, **kwargs)

        orden = self.request.GET.get('orden','fecha')
        filtro = self.request.GET.get('filtro','todas')
        direccion = self.request.GET.get('direccion','asc')
        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(self.request)

        context['carro'] = carro_obj
        context['orden'] = orden
        context['filtro'] = filtro
        context['direccion'] = direccion

        return context

    def get_queryset(self):
        queryset = super(TocataListView, self).get_queryset()

        orden = self.request.GET.get('orden','fecha')
        filtro = self.request.GET.get('filtro','todas')
        direccion = self.request.GET.get('direccion','asc')

        tocatas = Tocata.objects.none()
        tocatasabiertas = TocataAbierta.objects.none()

        if filtro == 'todas':
            tocatas = Tocata.objects.disponible()
            for tocata in tocatas:
                tocata.tipo = 'cerrada'
            tocatasabiertas = TocataAbierta.objects.disponible()
            for tocataabierta in tocatasabiertas:
                tocataabierta.tipo = 'abierta'

        elif filtro == 'cerradas':
            tocatas = Tocata.objects.disponible()
            for tocata in tocatas:
                tocata.tipo = 'cerrada'

        elif filtro == 'abiertas':
            tocatasabiertas = TocataAbierta.objects.disponible()
            for tocataabierta in tocatasabiertas:
                tocataabierta.tipo = 'abierta'

        if direccion == 'asc':
            result_list = sorted(chain(tocatas, tocatasabiertas,), key=attrgetter(orden), reverse=False)
        else:
            result_list = sorted(chain(tocatas, tocatasabiertas,), key=attrgetter(orden), reverse=True)

        return result_list

class TocataDetailView(DetailView):

    template_name = 'tocata/tocata.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataDetailView, self).get_context_data(*args, **kwargs)
        carro_obj, nuevo_carro = CarroCompra.objects.new_or_get(self.request)

        context['carro'] = carro_obj

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

@login_required(login_url='index')
def mistocatas(request):

    artista = UsuarioArtista.objects.get(user=request.user)
    tocatascerradas = Tocata.objects.filter(artista=artista.artista).filter(estado__in=parTocatas['estado_tipos_vista'])
    tocatasabiertas = TocataAbierta.objects.filter(artista=artista.artista).filter(estado__in=parTocatasAbiertas['estado_tipos_vista'])

    print(request.build_absolute_uri())
    for tocataabierta in tocatasabiertas:
        tocataabierta.numeropropuestas  = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado=parToca['pendiente']).count()

    context = {
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

    form = TocataForm(request.user, request.POST or None)

    if form.is_valid():

        nuevaTocata = form.save(commit=False)
        if 'flayer_original' in request.FILES:
            nuevaTocata.flayer_original = request.FILES['flayer_original']
            nuevaTocata.flayer_380_507 = request.FILES['flayer_original']
            nuevaTocata.flayer_1920_1280 = request.FILES['flayer_original']

        nuevaTocata.estado = parToca['publicado']
        nuevaTocata.region = nuevaTocata.lugar.region
        nuevaTocata.comuna = nuevaTocata.lugar.comuna

        nuevaTocata.usuario = request.user
        artista = Artista.objects.get(usuario=request.user)
        nuevaTocata.artista = artista
        nuevaTocata.asistentes_max = nuevaTocata.lugar.capacidad

        nuevaTocata.save()

        nuevaTocata.estilos.set(artista.estilos.all())

        messages.success(request, 'Tocata creada exitosamente')
        return redirect('mistocatas')
    #$else:
    #    print(form.errors.as_data())
    #    messages.error(request,'Error en form')

    context = {
        'form': form,
    }

    return render(request, 'tocata/creartocatacerrada.html', context)

@login_required(login_url='index')
def detallestocata(request, tocata_id):

    tocata = get_object_or_404(Tocata, pk=tocata_id)

    context = {
        'tocata': tocata,
    }

    return render(request, 'tocata/detallestocatacerrada.html', context)

@login_required(login_url='index')
def borrartocata(request, tocata_id):

    if request.method == 'POST':
        tocata = get_object_or_404(Tocata, pk=tocata_id)
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
def carga_comunas_tocata(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=int(region_id)).order_by('codigo')

    context = {
        'comunas_reg': comunas,
    }

    return render(request, 'tocata/comuna_dropdown_list_options_tocata.html', context)
