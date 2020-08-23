from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic.edit import FormMixin

from .models import EmailActivation

from .forms import IngresarForm, RegistrarUserForm, ReactivateEmailForm, UserDetailChangeViewForm, CuentaPasswordChangeForm
from .signals import user_logged_in

from toca.mixins import NextUrlMixin, RequestFormAttachMixin

# Create your views here.
class CuentaHomeView(LoginRequiredMixin, DetailView):

    template_name = 'cuentas/home.html'

    def get_object(self):
        return self.request.user

class CuentaEmailActivacionView(FormMixin, View):
    success_url = 'cuenta/ingresar'
    form_class = ReactivateEmailForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request,'Email confirmado. Ya puedes ingresar')
                return redirect('cuenta:ingresar')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = '''Email ya ha sido confirmado
                    ¿Queres <a href="{link}">reiniciar tu contraseña</a>?
                    '''.format(link=reset_link)
                    messages.success(request,mark_safe(msg))
                    return redirect('cuenta:ingresar')
        context = {
            'form': self.get_form(),
            'key': key
        }
        return render(request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = '''Email de activacion ya fue enviado'''
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(CuentaEmailActivacionView, self).form_valid(form )

    def form_invalid(self, form):
        request = self.request
        context = {
            'form': form,
            'key': self.key
        }
        return render(request, 'registration/activation_error.html', context)

class IngresarView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = IngresarForm
    template_name = 'cuentas/ingresar.html'
    success_url = '/'
    default_next = '/'

    def form_valid(self, form):
        #if Usuario.objects.get(user=usuario).es_artista:
        #    request.session['es_artista'] = 'S'
        #else:
        #    request.session['es_artista'] = 'N'
        #messages.success(request,'Ingreso Existos')
        next_path = self.get_next_url()
        return redirect(next_path)

class RegistrarView(CreateView):
    form_class = RegistrarUserForm
    template_name = 'cuentas/registrar.html'
    success_url = 'email/confirm/done'

class RegistrarDoneView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/activacion_cuenta_done.html')

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserDetailChangeViewForm
    template_name = 'cuentas/cuenta.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('cuenta:home')

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['formContra'] = CuentaPasswordChangeForm(self.request.POST or None)
        return context
