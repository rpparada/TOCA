from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User

from lugar.models import Lugar
from artista.models import Artista
from usuario.models import UsuarioArtista

from .forms import AgregaCamposUsuarioForm, UsuarioForm, UsuarioArtistaForm

from home.views import getTocatasArtistasHeadIndex
from .tokens import account_activation_token

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
            art.estado = parToca['disponible']
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

            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.save()

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta en Tocatas Intimas.'

            message = render_to_string('usuario/email_activacion_cuenta.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'usuario/activacion_cuenta_done.html')
        else:

            context = {
                'form': form,
            }

            mensaje = ''
            for campo, errores in form.errors.as_data().items():
                for error in errores:
                    mensaje = mensaje+' '+str(error.message)[:-1]+' and'

            mensaje = mensaje.rsplit(' ', 1)[0]

            messages.error(request,mensaje)
            return render(request, 'usuario/registrar.html', context)

    else:
        form = AgregaCamposUsuarioForm();
        usuario_form = UsuarioForm();

    context = {
        'form': form,
        'usuario_form': usuario_form,
    }
    return render(request, 'usuario/registrar.html', context)

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        login(request, user)

        return render(request, 'usuario/activacion_cuenta_completa.html')
    else:

        return HttpResponse('Activation link is invalid!')

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
            context = {
                'nombreusuario': nombreusuario,
            }
            messages.error(request,'Error en Usuario y/o Contraseña')
            return render(request, 'usuario/ingresar.html', context)
    else:
        return render(request, 'usuario/ingresar.html')

def salir(request):
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        auth.logout(request)
        messages.success(request,'Salida Existosa')
        if next:
            return HttpResponseRedirect(next)
        else:
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
