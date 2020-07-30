from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from datetime import datetime

from .models import Artista
from tocata.models import Tocata

from home.utils import getDataHeadIndex

from toca.parametros import parToca, parTocatas

# Create your views here.

class ArtistasListView(ListView):
    queryset = Artista.objects.disponible()
    paginate_by = parToca['artistas_pag']

    template_name = 'artista/artistas.html'

def artistas(request):

    usuario, numitemscarro = getDataHeadIndex(request)

    artistas_vista = Artista.objects.filter(estado=parToca['disponible'])

    for art in artistas_vista:
        art.cats = art.estilos.split()

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'artistas': artistas_vista
    }

    return render(request, 'artista/artistas.html', context)

class ArtistaDetailView(DetailView):

    template_name = 'artista/artista.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistaDetailView, self).get_context_data(*args, **kwargs)
        usuario, numitemscarro = getDataHeadIndex(self.request)

        tocatas = Tocata.objects.tocataartistadisponibles(context['object'])

        context['usuario'] = usuario
        context['numitemscarro'] = numitemscarro
        context['tocatas'] = tocatas

        return context

    def get_object(self, queryset=None):

        request = self.request
        slug = self.kwargs.get('slug')
        try:
            artista = Artista.objects.get(slug=slug)
        except Artista.DoesNotExist:
            raise Http404('Artista No Encontrado')
        except Artista.MultipleObjectsReturned:
            artistas = Artista.objects.filter(slug=slug)
            artista = tocatas.first()
        except:
            raise Http404('Error Desconocido')

        return artista

def artista(request, artista_id):

    artista = get_object_or_404(Artista, pk=artista_id)
    usuario, numitemscarro = getDataHeadIndex(request)

    tocatas_art = Tocata.objects.filter(estado__in=[parToca['publicado'],parToca['confirmado']])
    tocatas_art = tocatas_art.filter(artista=artista_id)
    hoy = datetime.today()
    for tocata_art in tocatas_art:
        diff = hoy - tocata_art.fecha_crea.replace(tzinfo=None)
        if diff.days <= parToca['diasNuevoTocata']:
            tocata_art.nuevo = 'SI'
        else:
            tocata_art.nuevo = 'NO'
        tocata_art.asistentes_diff = tocata_art.asistentes_max - tocata_art.asistentes_total

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'tocatas_art': tocatas_art,
        'artista': artista,
    }
    return render(request, 'artista/artista.html', context)
