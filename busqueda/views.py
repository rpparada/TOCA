from django.shortcuts import render
from django.views.generic.list import ListView

from datetime import datetime
from itertools import chain

from tocata.models import Tocata, TocataAbierta

from toca.parametros import parToca

# Create your views here.
class BusquedaTocataView(ListView):

    template_name = 'busqueda/busqueda_test.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BusquedaTocataView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:

            tocatas = Tocata.objects.busqueda(query)
            for tocata in tocatas:
                diff = datetime.today() - tocata.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoTocata']:
                    tocata.nuevo = 'SI'
                else:
                    tocata.nuevo = 'NO'
                tocata.asistentes_diff = tocata.asistentes_max - tocata.asistentes_total
                tocata.tipo = 'cerrada'

            tocatasabiertas = TocataAbierta.objects.busqueda(query)
            for tocataabierta in tocatasabiertas:
                diff = datetime.today() - tocataabierta.fecha_crea.replace(tzinfo=None)
                if diff.days <= parToca['diasNuevoTocata']:
                    tocataabierta.nuevo = 'SI'
                else:
                    tocataabierta.nuevo = 'NO'
                tocataabierta.tipo = 'abierta'

            result_list = chain(tocatas, tocatasabiertas)

            return result_list

        return Tocata.objects.none()
