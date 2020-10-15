from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from anulaciones.models import AnulacionEntrada
from tocata.models import Tocata

# Create your views here.
class TocatasCanceladasListView(LoginRequiredMixin, ListView):

    template_name = 'anulaciones/listatocatascanceladas.html'
    paginate_by = 10
    ordering = ['-fecha_crea']
    queryset = Tocata.objects.suspendidas()
