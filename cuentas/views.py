from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.utils.http import is_safe_url

from usuario.models import Usuario

from .forms import IngresarForm, RegistrarUserForm


# Create your views here.
def ingresar(request):

    form = IngresarForm(request.POST or None)

    if form.is_valid():
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        nombreusuario = form.cleaned_data.get('nombreusuario')
        contra = form.cleaned_data.get('contra')

        usuario = auth.authenticate(username=nombreusuario, password=contra)

        if usuario is not None:
            auth.login(request, usuario)

            if Usuario.objects.get(user=usuario).es_artista:
                request.session['es_artista'] = 'S'
            else:
                request.session['es_artista'] = 'N'
            messages.success(request,'Ingreso Existos')

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('index')
        else:
            messages.error(request,'Error en Usuario y/o Contraseña')

    context = {
        'form': form
    }

    return render(request, 'cuentas/ingresar.html', context)

def registrar(request):

    form = UserForm(request.POST or None)

    context = {
        'form': form,
    }

    if form.is_valid():
        form.save()
        return redirect('ingresar')

    return render(request, 'cuentas/registrar.html', context)
