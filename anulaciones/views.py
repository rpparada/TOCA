from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from anulaciones.models import AnulacionEntrada, TocataCancelada
from tocata.models import Tocata

# Create your views here.
class TocatasCanceladasListView(LoginRequiredMixin, ListView):

    template_name = 'anulaciones/listatocatascanceladas.html'
    paginate_by = 10
    ordering = ['-fecha_crea']
    queryset = TocataCancelada.objects.all()

class EntradasTocataCanceladaListView(LoginRequiredMixin, ListView):

    template_name = 'anulaciones/listaentradastocatacancelada.html'
    paginate_by = 20

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        tocata = Tocata.objects.get(slug=slug)
        anulaciones = AnulacionEntrada.objects.by_tocata(tocata).order_by('-fecha_crea')

        return anulaciones

    def get_context_data(self, *args, **kwargs):
        context = super(EntradasTocataCanceladaListView, self).get_context_data(*args, **kwargs)

        slug = self.kwargs.get('slug')
        tocata = Tocata.objects.get(slug=slug)

        context['tocata'] = tocata

        return context
