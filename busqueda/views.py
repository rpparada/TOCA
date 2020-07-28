from django.shortcuts import render
from django.views.generic.list import ListView

from tocata.models import Tocata, TocataAbierta

# Create your views here.
class BusquedaTocataView(ListView):

    template_name = 'busqueda/busqueda_test.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BusquedaTocataView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        #query = request.GET.get('q')
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Tocata.objects.filter(nombre__icontains=query)
        return Tocata.objects.none()
