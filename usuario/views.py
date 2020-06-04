from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth


from django.contrib.auth.models import User
from lugar.models import Lugar
from artista.models import Artista
from usuario.models import UsuarioArtista

from .forms import AgregaCamposUsuarioForm, UsuarioForm, UsuarioArtistaForm

from home.views import getTocatasArtistasHeadIndex

from toca.parametros import parToca

# Create your views here.
def registrarArt(request):

    if request.method == 'POST':
        form = AgregaCamposUsuarioForm(request.POST)
        usuario_form = UsuarioForm(request.POST)
        usuario_art_form = UsuarioArtistaForm(request.POST)

        if form.is_valid() and usuario_form.is_valid() and usuario_art_form.is_valid():
            user = form.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.es_artista = True
            usuario.save()

            usuario_art = usuario_art_form.save(commit=False)
            usuario_art.user = user
            usuario_art.num_celular = parToca['prefijoCelChile']+str(usuario_art.num_celular)
            usuario_art.save()

            art = Artista.objects.get(id=usuario_art.artista.id)
            art.usuario = user
            art.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            messages.success(request, 'Usuario registrado exitosamente. Ahora puedes ingresar')
            return redirect('index')
        else:
            messages.error(request,form.errors)
            messages.error(request,usuario_form.errors)
            messages.error(request,usuario_art_form.errors)
            return redirect('registrarart')

    else:
        form = AgregaCamposUsuarioForm()
        usuario_form = UsuarioForm()
        usuario_art_form = UsuarioArtistaForm()

    context = {
        'form': form,
        'usuario_form': usuario_form,
        'usuario_art_form': usuario_art_form,
    }
    return render(request, 'usuario/registrarart.html', context)


def registrar(request):

    if request.method == 'POST':
        form = AgregaCamposUsuarioForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if form.is_valid() and usuario_form.is_valid():
            user = form.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            messages.success(request, 'Usuario registrado exitosamente. Ahora puedes ingresar')
            return redirect('index')
        else:
            messages.error(request,form.errors)
            return redirect('registrar')

    else:
        form = AgregaCamposUsuarioForm();
        usuario_form = UsuarioForm();

    context = {
        'form': form,
        'usuario_form': usuario_form,
    }
    return render(request, 'usuario/registrar.html', context)


def ingresar(request):

    if request.method == 'POST':
        nombreusuario = request.POST['nombreusuario']
        contra = request.POST['contra']
        next = request.POST.get('next', '/')

        usuario = auth.authenticate(username=nombreusuario, password=contra)
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request,'Ingreso Existos')

            if next:
                return HttpResponseRedirect(next)
            else:
                return redirect('index')

        else:
            messages.error(request,'Usuario no encontrado')
            return redirect('ingresar')
    else:
        return render(request, 'usuario/ingresar.html')

def salir(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Salida Existosa')
        return redirect('index')

def cuenta(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)
    context = {
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'usuario': usuario,
    }
    return render(request, 'usuario/cuenta.html', context)

def actualizar(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)

    context = {
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'usuario': usuario,
    }

    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']

        usuario = request.user

        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.save()
        messages.success(request,'Actualizacion Existosa')

    return render(request, 'usuario/cuenta.html', context)

def actualizarArt(request):

    if request.method == 'POST':

        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        rut = request.POST['rut']
        digitoVerificador = request.POST['digitoVerificador']
        num_celular = request.POST['num_celular']
        banco = request.POST['banco']
        num_cuenta = request.POST['num_cuenta']
        tipo_cuenta = request.POST['tipo_cuenta']

        usuario = request.user
        usuario_art = UsuarioArtista.objects.filter(user=request.user)[0]

        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario_art.rut = rut
        usuario_art.digitoVerificador = digitoVerificador
        usuario_art.num_celular = parToca['prefijoCelChile']+str(num_celular)
        usuario_art.banco = banco
        usuario_art.num_cuenta = num_cuenta
        usuario_art.tipo_cuenta = tipo_cuenta

        usuario.save()
        usuario_art.save()

        messages.success(request,'Actualizacion Existosa')

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)
    usuario_art = UsuarioArtista.objects.filter(user=request.user)[0]
    usuario_art_form = UsuarioArtistaForm(request)

    context = {
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'usuario': usuario,
        'usuario_art': usuario_art,
        'usuario_art_form': usuario_art_form,
    }

    return render(request, 'usuario/cuentaart.html', context)

def cuentaArt(request):

    toc_head, art_head, usuario = getTocatasArtistasHeadIndex(request)
    usuario_art = UsuarioArtista.objects.filter(user=request.user)[0]
    usuario_art_form = UsuarioArtistaForm()

    context = {
        'tocatas_h': toc_head[:3],
        'artistas_h': art_head[:3],
        'usuario': usuario,
        'usuario_art': usuario_art,
        'usuario_art_form': usuario_art_form,
    }
    return render(request, 'usuario/cuentaart.html', context)

def cambioContra(request):

    if request.method == 'POST':

        contraact = request.POST['contraact']
        contranueva = request.POST['contranueva']
        contranuevarep = request.POST['contranuevarep']

        usuario = auth.authenticate(username=request.user.username, password=contraact)

        if usuario is not None:
            if contranueva:
                if contranueva == contranuevarep:
                    usuario.set_password(contranueva)
                    usuario.save()
                    auth.login(request, usuario)
                    messages.success(request,'Actualizacion Existosa')
                    return redirect('index')
                else:
                    messages.error(request,'Contraseñas nuevas diferentes')
                    return render(request, 'usuario/cambiocontra.html')
            else:
                messages.error(request,'Complete Ambos Campos para nueva contraseña')
                return render(request, 'usuario/cambiocontra.html')
        else:
            messages.error(request,'Actual Contraseña Incorrecta')
            return render(request, 'usuario/cambiocontra.html')

    return render(request, 'usuario/cambiocontra.html')

def enviaform(request):

    artistas = Artista.objects.filter(usuario__isnull=True)

    context = {
        'artistas': artistas,
    }

    return render(request,'usuario/enviaformnuevoart.html', context)
