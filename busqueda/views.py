from django.shortcuts import render
from django.views.generic.list import ListView

from tocata.models import Tocata, TocataAbierta

# Create your views here.
class BusquedaTocataView(ListView):

    template_name = 'busqueda/busqueda_test.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Tocata.objects.all()
