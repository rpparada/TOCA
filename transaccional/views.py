from django.shortcuts import render
from django.views.generic import (
                                DetailView,
                                ListView,
                                View,
                                CreateView,
                                UpdateView
                            )

from tocata.models import Tocata

# Create your views here.

class TocataCanceladaView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class TocataCanceladaArtistaView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class TocataCanceladaUsuarioView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class RecuperarPasswordView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class ValidacionEmailView(DetailView):

    template_name = 'transaccional/validacion_email.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class FormularioNuevoArtistaView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class BienvenidoNuevoUsuarioView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class BienvenidoNuevoArtistaView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata
