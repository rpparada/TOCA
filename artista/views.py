from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.http import Http404

from datetime import datetime

from .models import Artista, Estilo
from tocata.models import Tocata
from tocataabierta.models import TocataAbierta

from analytics.mixins import ObjectViewedMixin

from toca.parametros import parToca, parTocatas

# Create your views here.
class ArtistasListView(ListView):

    queryset = Artista.objects.disponible()
    paginate_by = parToca['artistas_pag']
    template_name = 'artista/artistas.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistasListView, self).get_context_data(*args, **kwargs)
        estilos = Estilo.objects.activo()
        context['estilos'] = estilos

        return context

class ArtistaDetailView(ObjectViewedMixin, DetailView):

    template_name = 'artista/artista.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistaDetailView, self).get_context_data(*args, **kwargs)
        artista = kwargs['object']
        tocatas = Tocata.objects.tocataartistadisponibles(artista)
        tocatasabiertas = TocataAbierta.objects.by_artista(artista)

        print(tocatasabiertas)

        context['tocata_list'] = tocatas
        context['tocatasabiertas'] = tocatasabiertas

        return context

    def get_object(self, *args, **kwargs):
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
