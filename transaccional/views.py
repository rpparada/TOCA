from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.views.generic import (
                                DetailView,
                                ListView,
                                View,
                                CreateView,
                                UpdateView
                            )

from tocata.models import Tocata
from cuentas.models import EmailActivation
from anulaciones.models import TocataCancelada
from artista.models import Artista

from cuentas.tokens import account_activation_token, art_activation_token

# Create your views here.

class TocataCanceladaView(DetailView):

    template_name = 'transaccional/tocata_cancelada.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class TocataCanceladaArtistaView(DetailView):

    template_name = 'transaccional/tocata_cancelada_artista.html'

    def get_object(self, queryset=None):
        tocata = TocataCancelada.objects.all().first()
        return tocata

    def get_context_data(self, *args, **kwargs):
        context = super(TocataCanceladaArtistaView, self).get_context_data(*args, **kwargs)

        return context

class RecuperarPasswordView(DetailView):

    template_name = 'transaccional/password_reset_email.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

class ValidacionEmailView(DetailView):

    template_name = 'transaccional/validacion_email.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

    def get_context_data(self, *args, **kwargs):
        context = super(ValidacionEmailView, self).get_context_data(*args, **kwargs)

        base_url = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
        email_activacion = EmailActivation.objects.all().first()
        key_path = reverse('cuenta:email-activate', kwargs={'key':email_activacion.key})
        path = '{base}{path}'.format(base=base_url,path=key_path)

        context['email'] = self.request.user
        context['path'] = path

        return context

class FormularioNuevoArtistaView(DetailView):

    template_name = 'transaccional/invitacion_nuevo_artista.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

    def get_context_data(self, *args, **kwargs):
        context = super(FormularioNuevoArtistaView, self).get_context_data(*args, **kwargs)

        current_site = get_current_site(self.request)
        context['domain'] = current_site.domain

        artista = Artista.objects.all().first()
        context['uid'] = urlsafe_base64_encode(force_bytes(artista.pk))

        context['token'] = art_activation_token.make_token(artista)

        return context

class BienvenidoNuevoUsuarioView(DetailView):

    template_name = 'transaccional/bienvenido_nuevo_usuario.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

    def get_context_data(self, *args, **kwargs):
        context = super(BienvenidoNuevoUsuarioView, self).get_context_data(*args, **kwargs)

        context['email'] = self.request.user.email

        return context

class BienvenidoNuevoArtistaView(DetailView):

    template_name = 'transaccional/bienvenido_nuevo_artista.html'

    def get_object(self, queryset=None):
        tocata = Tocata.objects.all().first()
        return tocata

    def get_context_data(self, *args, **kwargs):
        context = super(BienvenidoNuevoArtistaView, self).get_context_data(*args, **kwargs)

        context['artista'] = Artista.objects.all().first

        return context
