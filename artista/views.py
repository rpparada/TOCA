from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from datetime import datetime

from .models import Artista, Estilo
from tocata.models import Tocata

from home.utils import getDataHeadIndex

from toca.parametros import parToca, parTocatas

# Create your views here.
class ArtistasListView(ListView):
    queryset = Artista.objects.disponible()
    paginate_by = parToca['artistas_pag']
    template_name = 'artista/artistas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistasListView, self).get_context_data(*args, **kwargs)

        usuario, numitemscarro = getDataHeadIndex(self.request)

        estilos = Estilo.objects.activo()

        context['usuario'] = usuario
        context['numitemscarro'] = numitemscarro
        context['estilos'] = estilos

        return context

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
