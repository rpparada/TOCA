from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from anulaciones.models import AnulacionEntrada, TocataCancelada
from tocata.models import Tocata

from .forms import (
                MarcarComoEnviadaTBKForm,
                MarcarComoReembolsadoForm,
                MarcarComoReembolsadoTBKForm
            )

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

class MarcarComoEnviadaTBKView(LoginRequiredMixin, View):

    form_class = MarcarComoEnviadaTBKForm

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            anulacion = form.cleaned_data['anulacion']
            anulacion.estado = 'enviadatbk'
            anulacion.save()

        return redirect('cancelaciones:anulacion', slug=slug)

class MarcarComoReembolsadoView(LoginRequiredMixin, View):

    form_class = MarcarComoReembolsadoForm

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            anulacion = form.cleaned_data['anulacion']
            anulacion.estado = 'reembolsado'
            anulacion.save()

            # Verificar si todas las entradas fueron
            # reembolsadas para marcar tocata como reembolsada

        return redirect('cancelaciones:anulacion', slug=slug)

class MarcarComoReembolsadoTBKView(LoginRequiredMixin, View):

    form_class = MarcarComoReembolsadoTBKForm

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            anulacion = form.cleaned_data['anulacion']
            anulacion.estado = 'reembolsadotbk'
            anulacion.save()

            # Verificar si todas las entradas fueron
            # reembolsadas para marcar tocata como reembolsada

        return redirect('cancelaciones:anulacion', slug=slug)
