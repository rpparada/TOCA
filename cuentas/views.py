from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation

from .forms import IngresarForm, RegistrarUserForm
from .signals import user_logged_in

# Create your views here.
class CuentaHomeView(LoginRequiredMixin, DetailView):

    template_name = 'cuentas/cuenta.html'

    def get_object(self):
        return self.request.user

class CuentaEmailActivacionView(View):

    def get(self, request, key, *args, **kwargs):
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
        return render(request, 'registration/activation_error.html')

    def post(self, request, *args, **kwargs):
        pass

class IngresarView(FormView):
    form_class = IngresarForm
    template_name = 'cuentas/ingresar.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get('email')
        contra = form.cleaned_data.get('contra')
        usuario = auth.authenticate(username=email, password=contra)
        if usuario is not None:
            if not usuario.is_active:
                messages.error(request,'Usuario Inactivo')
                return super(IngresarView, self).form_invalid(form)

            auth.login(request, usuario)
            user_logged_in.send(usuario.__class__, instance=usuario, request=request)
            #if Usuario.objects.get(user=usuario).es_artista:
            #    request.session['es_artista'] = 'S'
            #else:
            #    request.session['es_artista'] = 'N'
            messages.success(request,'Ingreso Existos')
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(IngresarView, self).form_invalid(form)

class RegistrarView(CreateView):
    form_class = RegistrarUserForm
    template_name = 'cuentas/registrar.html'
    success_url = 'email/confirm/done'

class RegistrarDoneView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/activacion_cuenta_done.html')
