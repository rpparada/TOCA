from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import OrdenCompra, EntradasCompradas
from facturacion.models import FacturacionProfile

# Create your views here.
class OrdenCompraListView(LoginRequiredMixin, ListView):

    template_name = 'orden/ordencompra_list.html'
    def get_queryset(self):
        return OrdenCompra.objects.by_request(self.request)

class OrdenCompraDetailView(LoginRequiredMixin, DetailView):

    template_name = 'orden/ordencompra_detail.html'

    def get_object(self):
        qs = OrdenCompra.objects.by_request(
                    self.request
                ).filter(
                    orden_id=self.kwargs.get('orden_id')
                )
        print('aqui1')
        if qs.count() == 1:
            return qs.first()
        print('aqui2')
        raise Http404

class LibreriaView(LoginRequiredMixin, ListView):
    template_name = 'orden/libreria.html'
    def get_queryset(self):
        return EntradasCompradas.objects.by_request(self.request).all()
