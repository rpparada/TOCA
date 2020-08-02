from django.shortcuts import render
from django.views.generic.list import ListView

from itertools import chain
from operator import attrgetter

from tocata.models import Tocata, TocataAbierta

from toca.parametros import parToca

# Create your views here.
class BusquedaTocataView(ListView):

    template_name = 'busqueda/busqueda.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BusquedaTocataView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')

        orden = self.request.GET.get('orden','fecha')
        filtro = self.request.GET.get('filtro','todas')
        direccion = self.request.GET.get('direccion','asc')

        context['orden'] = orden
        context['filtro'] = filtro
        context['direccion'] = direccion

        return context

    def get_queryset(self, *args, **kwargs):
        #queryset = super(BusquedaTocataView, self).get_queryset()

        method_dict = self.request.GET
        query = method_dict.get('q', None)

        orden = self.request.GET.get('orden','fecha')
        filtro = self.request.GET.get('filtro','todas')
        direccion = self.request.GET.get('direccion','asc')

        tocatas = Tocata.objects.none()
        tocatasabiertas = TocataAbierta.objects.none()

        if query is not None:

            if filtro == 'todas':
                tocatas = Tocata.objects.busqueda(query)
                for tocata in tocatas:
                    tocata.tipo = 'cerrada'
                tocatasabiertas = TocataAbierta.objects.busqueda(query)
                for tocataabierta in tocatasabiertas:
                    tocataabierta.tipo = 'abierta'

            elif filtro == 'cerradas':
                tocatas = Tocata.objects.busqueda(query)
                for tocata in tocatas:
                    tocata.tipo = 'cerrada'

            elif filtro == 'abiertas':
                tocatasabiertas = TocataAbierta.objects.busqueda(query)
                for tocataabierta in tocatasabiertas:
                    tocataabierta.tipo = 'abierta'

            if direccion == 'asc':
                result_list = sorted(chain(tocatas, tocatasabiertas,), key=attrgetter(orden), reverse=False)
            else:
                result_list = sorted(chain(tocatas, tocatasabiertas,), key=attrgetter(orden), reverse=True)

        else:

            result_list = chain(tocatas, tocatasabiertas)

        return result_list
