from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from usuario.models import Usuario

from .forms import IngresarForm, RegistrarUserForm

# Create your views here.

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
            auth.login(request, usuario)
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
    success_url = '/cuentas/ingresar'
