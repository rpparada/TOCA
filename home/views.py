from django.views.generic import ListView

from tocata.models import Tocata
from tocataabierta.models import TocataAbierta
from artista.models import Artista
from .models import Testimonio, DescripcionTocatasIntimas

# Create your views here.
class IndexListView(ListView):

    queryset = Tocata.objects.get_mejores_tocatas(10)
    template_name = 'home/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexListView, self).get_context_data(*args, **kwargs)

        # Mejores Tocatas Abiertas
        tocatasabiertas = TocataAbierta.objects.get_mejores_tocatasabiertas(10)

        # Artistas Destacados
        artistas = Artista.objects.get_artistas_destacados(3)

        # Cuadros de descripcion
        descripciones = DescripcionTocatasIntimas.objects.get_descripcion_by_request(self.request)

        # Testimonos
        testimonios = Testimonio.objects.get_testimonio_by_request(self.request)

        context['tocatasabiertas'] = tocatasabiertas
        context['artistas'] = artistas
        context['descripciones'] = descripciones
        context['testimonios'] = testimonios

        return context
