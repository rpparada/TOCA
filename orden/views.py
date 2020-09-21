from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.conf import settings

import os
from wsgiref.util import FileWrapper;
from mimetypes import guess_type

from .models import OrdenCompra, EntradasCompradas
from facturacion.models import FacturacionProfile

from toca.utils import render_to_pdf

# Create your views here.
class OrdenCompraListView(LoginRequiredMixin, ListView):
    template_name = 'orden/ordencompra_list.html'
    paginate_by = 10
    ordering = ['-fecha_pago']

    def get_queryset(self):
        return OrdenCompra.objects.by_request(self.request).order_by('-fecha_pago')

class OrdenCompraDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orden/ordencompra_detail.html'

    def get_object(self):
        qs = OrdenCompra.objects.by_request(
                    self.request
                ).filter(
                    orden_id=self.kwargs.get('orden_id')
                )
        if qs.count() == 1:
            return qs.first()
        raise Http404

class OrdenDownloadView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        orden_id = kwargs.get('orden_id')

        print(orden_id)

        qs = OrdenCompra.objects.by_request(
                    self.request
                ).filter(
                    orden_id=orden_id
                )

        if qs.count() == 1:
            orden = qs.first()
            context = {
                'object': orden
            }
            pdf = render_to_pdf('orden/emails/email_skeleton_test.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = 'IT_Orden_%s.pdf' %(orden.orden_id)
                content = 'inline; filename="%s"' %(filename)
                download = request.GET.get("download")
                if download:
                    content = 'attachment; filename="%s"' %(filename)
                response['Content-Disposition'] = content
                return response
        raise Http404

class EntradasComprasListView(LoginRequiredMixin, ListView):
    template_name = 'orden/entradascompradas_list.html'
    paginate_by = 10

    def get_queryset(self):
        return EntradasCompradas.objects.by_request(self.request).all().order_by('item__tocata__fecha')

class EntradasComprasDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orden/entradascompradas_detail.html'

    def get_object(self, queryset=None):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            entrada = EntradasCompradas.objects.get(slug=slug)
        except EntradasCompradas.DoesNotExist:
            raise Http404('Entrada No Encontrada')
        except EntradasCompradas.MultipleObjectsReturned:
            entradas = EntradasCompradas.objects.get(slug=slug)
            entrada = entradas.first()
        except:
            raise Http404('Error Desconocido')

        return entrada

class ITicketDownloadView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        download_qs = EntradasCompradas.objects.filter(pk=pk)
        if download_qs.count() != 1:
            raise Http404('Archivo no encontrado')
        download_obj = download_qs.first()

        can_download = False
        tocatas_compradas = EntradasCompradas.objects.by_request(request)
        # Permisos de descarga
        if request.user.is_authenticated and download_obj in tocatas_compradas:
            can_download = True

        if not can_download:
            messages.error(request,'No tienes accesso a estas entradas')
            return redirect('libreria')

        file_root = settings.PROTECTED_ROOT
        filepath = download_obj.file.path
        final_filepath = os.path.join(file_root, filepath)

        with open(final_filepath, 'rb') as f:
            wrapper = FileWrapper(f)
            mimetype = 'application/force-download'
            guess_mimetype =guess_type(filepath)[0]
            if guess_mimetype:
                mimetype = guess_mimetype
            response = HttpResponse(wrapper,content_type=mimetype)
            response['Content-Disposition'] = 'attachment;filename=%s' %(download_obj.nombrearchivo)
            response['X-SendFile'] = str(download_obj.nombrearchivo)
            return response

        #return redirect(download_obj.get_default_url())
