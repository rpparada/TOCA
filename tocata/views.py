from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView

from django.http import Http404

from itertools import chain
from operator import attrgetter

from .forms import TocataForm, LugaresTocataForm, TocataAbiertaForm

from .models import Tocata, LugaresTocata, TocataAbierta
from artista.models import Artista
from lugar.models import Lugar, Comuna, Region
from usuario.models import UsuarioArtista, Usuario
from carro.models import CarroCompra

from home.utils import getDataHeadIndex

from toca.parametros import parToca, parTocatas, parTocatasAbiertas

# Create your views here.
class TocataListView(ListView):

    queryset = Tocata.objects.disponible()
    paginate_by = parToca['tocatas_pag']
    template_name = 'tocata/tocatas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataListView, self).get_context_data(*args, **kwargs)

        usuario, numitemscarro = getDataHeadIndex(self.request)

        orden = self.request.GET.get('orden','fecha')
        filtro = self.request.GET.get('filtro','todas')
        direccion = self.request.GET.get('direccion','asc')

        context['usuario'] = usuario
        context['numitemscarro'] = numitemscarro

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
        usuario, numitemscarro = getDataHeadIndex(self.request)
        carro_obj, nuevo_carro = CarroCompra.objects.nuevo_or_entrega(self.request)

        context['usuario'] = usuario
        context['numitemscarro'] = numitemscarro
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

class TocataAbiertaDetailView(DetailView):

    queryset = TocataAbierta.objects.all()
    template_name = 'tocata/tocataabierta.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TocataAbiertaDetailView, self).get_context_data(*args, **kwargs)
        usuario, numitemscarro = getDataHeadIndex(self.request)

        context['usuario'] = usuario
        context['numitemscarro'] = numitemscarro

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

@login_required(login_url='index')
def mistocatas(request):

    usuario, numitemscarro = getDataHeadIndex(request)

    artista = UsuarioArtista.objects.get(user=request.user)
    tocatascerradas = Tocata.objects.filter(artista=artista.artista).filter(estado__in=parTocatas['estado_tipos_vista'])
    tocatasabiertas = TocataAbierta.objects.filter(artista=artista.artista).filter(estado__in=parTocatasAbiertas['estado_tipos_vista'])

    print(request.build_absolute_uri())
    for tocataabierta in tocatasabiertas:
        tocataabierta.numeropropuestas  = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado=parToca['pendiente']).count()

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
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

    usuario, numitemscarro = getDataHeadIndex(request)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'form': form,
    }

    return render(request, 'tocata/creartocatacerrada.html', context)

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

    usuario, numitemscarro = getDataHeadIndex(request)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'form': form,
    }

    return render(request, 'tocata/creartocataabierta.html', context)

@login_required(login_url='index')
def detallestocata(request, tocata_id):

    usuario, numitemscarro = getDataHeadIndex(request)
    tocata = get_object_or_404(Tocata, pk=tocata_id)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'tocata': tocata,
    }

    return render(request, 'tocata/detallestocatacerrada.html', context)

@login_required(login_url='index')
def detallestocataabierta(request, tocata_id):

    usuario, numitemscarro = getDataHeadIndex(request)
    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
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

    usuario, numitemscarro = getDataHeadIndex(request)
    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'mislugares': mislugares,
        'tocata': tocata,
    }

    return render(request, 'tocata/proponerlugar.html', context)

@login_required(login_url='index')
def verpropuestas(request, tocata_id):

    usuario, numitemscarro = getDataHeadIndex(request)

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
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

    usuario, numitemscarro = getDataHeadIndex(request)

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
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
