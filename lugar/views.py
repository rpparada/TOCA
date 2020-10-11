from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                            DetailView,
                            ListView,
                            View,
                            CreateView
                        )

from .models import Lugar, Region, Provincia, Comuna
from tocata.models import Tocata
from propuestaslugar.models import LugaresTocata

from .forms import (
                CrearLugarForm,
                RegionForm,
                ComunaForm,
                ActualizaLugarForm,
                BorrarLugarForm
            )

from toca.parametros import parToca

from toca.mixins import NextUrlMixin, RequestFormAttachMixin

# Create your views here.

class MisLugaresListView(LoginRequiredMixin, ListView):

    template_name = 'lugar/mislugares.html'
    paginate_by = 12
    ordering = ['-fecha_crea']

    def get_queryset(self, *args, **kwargs):
        request = self.request
        mislugares = Lugar.objects.by_request(request)

        return mislugares

class LugarCreateView(NextUrlMixin, RequestFormAttachMixin, LoginRequiredMixin, CreateView):
    form_class = CrearLugarForm
    template_name = 'lugar/agregarlugar.html'
    success_url = '/lugares/mislugares'

    def form_valid(self, form):
        request = self.request
        msg = 'Dirección creado exitosamente'
        messages.success(request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        request = self.request
        msg = 'Error al crear dirección'
        messages.error(request, msg)
        return super().form_invalid(form)

class ActualizaLugarView(LoginRequiredMixin, View):

    form_class = ActualizaLugarForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            lugar = form.cleaned_data['lugar']
            descripción = form.cleaned_data['descripción']
            lugar.update_descripción(descripción)

        return redirect('lugar:mislugares')

class BorrarLugarView(LoginRequiredMixin, View):

    form_class = BorrarLugarForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            lugar = form.cleaned_data['lugar']
            lugar.borrar()

        return redirect('lugar:mislugares')

@login_required(login_url='index')
def carga_comunas_agregar(request):

    region_id = request.GET.get('region')
    comunas = Comuna.objects.filter(region=region_id).exclude(nombre='Todas').order_by('nombre')
    context = {
        'comunas_reg': comunas,
    }
    return render(request, 'lugar/comuna_dropdown_list_options_agregar.html', context)

@login_required(login_url='index')
def carga_comunas_actualizar(request):

    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    comunas = Comuna.objects.filter(region=region_id).exclude(nombre='Todas').order_by('nombre')

    if comuna_id.isdigit():
        context = {
            'comunas_reg': comunas,
            'comuna_id': int(comuna_id),
        }
    else:
        context = {
            'comunas_reg': comunas,
            'comuna_id': comunas.first(),
        }

    return render(request, 'lugar/comuna_dropdown_list_options_actualizar.html', context)
