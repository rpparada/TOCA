from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from lugar.models import Lugar
from artista.models import Artista
from usuario.models import UsuarioArtista, Usuario

from .forms import (
        UserForm,
        UsuarioArtistaForm,
        ArtistaUserForm,
        IngresarForm,
        EditarCuentaUserForm
        )

from home.utils import getDataHeadIndex

from .tokens import account_activation_token, art_activation_token

from toca.parametros import parToca

# Create your views here.
def activateArt(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        artista = Artista.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Artista.DoesNotExist):
        artista = None

    if artista is not None and art_activation_token.check_token(artista, token):
        artistaUserForm = ArtistaUserForm(initial={'email':artista.email,
                                                    'username':artista.email})
        usuarioArtistaForm = UsuarioArtistaForm(initial={'artista':artista})

        context = {
            'artistaUserForm': artistaUserForm,
            'usuarioArtistaForm': usuarioArtistaForm,
        }
        return render(request, 'usuario/registrarart.html', context)
    else:
        return render(request, 'usuario/link_invalido.html')

def registrarArt(request):

    artistaUserForm = ArtistaUserForm(request.POST or None)
    usuarioArtistaForm = UsuarioArtistaForm(request.POST or None)

    if artistaUserForm.is_valid() and usuarioArtistaForm.is_valid():

        # Crea nuevo user
        artistauser = artistaUserForm.save()

        # Define usuario como artista
        usuario = Usuario(
            user=artistauser,
            es_artista=True
        )
        usuario.save()

        # Crea datos artistas
        usuarioartista = usuarioArtistaForm.save(commit=False)
        usuarioartista.user = artistauser
        usuarioartista.save()

        # Actualizar y habilita artista
        artista = Artista.objects.get(email=artistauser.email)
        artista.usuario = artistauser
        artista.estado = parToca['disponible']
        artista.save()

        # Ingreso de Usuario Artista
        username = artistaUserForm.cleaned_data.get('username')
        password = artistaUserForm.cleaned_data.get('password1')
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        messages.success(request, 'Artista registrado exitosamente')
        return redirect('index')

    else:
        print(artistaUserForm.errors.as_data())
        print(usuarioArtistaForm.errors.as_data())
        messages.error(request,'Error en form')

    context = {
        'artistaUserForm': artistaUserForm,
        'usuarioArtistaForm': usuarioArtistaForm,
    }

    return render(request, 'usuario/registrarart.html', context)

def registrar(request):

    form = UserForm(request.POST or None)

    if form.is_valid():
        if User.objects.filter(username=form.cleaned_data.get('email')).exists():
            messages.error(request,"Email ya registrado")
        else:
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.save()

            usuario = Usuario(
                user = user,
                es_artista = False
            )
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

    context = {
        'form': form,
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
        return render(request, 'usuario/link_invalido.html')

def ingresar(request):

    form = IngresarForm(request.POST or None)

    if form.is_valid():
        next = request.POST.get('next', '/')

        nombreusuario = form.cleaned_data.get('nombreusuario')
        contra = form.cleaned_data.get('contra')

        usuario = auth.authenticate(username=nombreusuario, password=contra)

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request,'Ingreso Existos')

            if next:
                return HttpResponseRedirect(next)

            else:
                return redirect('index')

        else:
            messages.error(request,'Error en Usuario y/o Contraseña')

    context = {
        'form': form
    }

    return render(request, 'usuario/ingresar.html', context)


def salir(request):

    if request.method == 'POST':
        next = request.POST.get('next', '/')
        auth.logout(request)
        messages.success(request,'Salida Existosa')
        if next:
            return HttpResponseRedirect(next)
        else:
            return redirect('index')

@login_required(login_url='index')
def CuentaUserView(request):

    form = EditarCuentaUserForm(request.POST or None, instance=request.user)

    if form.is_valid():
        user = form.save(commit=False)
        user.save()

    usuario, numitemscarro = getDataHeadIndex(request)
    context = {
        'form': form,
        'numitemscarro': numitemscarro,
    }
    return render(request, 'usuario/cuenta.html', context)

@login_required(login_url='index')
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

    usuario, numitemscarro = getDataHeadIndex(request)
    usuario_art = UsuarioArtista.objects.filter(user=request.user)[0]
    usuario_art_form = UsuarioArtistaForm(request)

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'usuario_art': usuario_art,
        'usuario_art_form': usuario_art_form,
    }

    return render(request, 'usuario/cuentaart.html', context)

@login_required(login_url='index')
def cuentaArt(request):

    usuario, numitemscarro = getDataHeadIndex(request)
    usuario_art = UsuarioArtista.objects.filter(user=request.user)[0]
    usuario_art_form = UsuarioArtistaForm()

    context = {
        'usuario': usuario,
        'numitemscarro': numitemscarro,
        'usuario_art': usuario_art,
        'usuario_art_form': usuario_art_form,
    }
    return render(request, 'usuario/cuentaart.html', context)


@login_required(login_url='index')
def cambioContra(request):

    if request.method == 'POST':

        contraact = request.POST['contraact']
        #contranueva = request.POST['password1']
        contranueva = request.POST.get('password1')
        #contranuevarep = request.POST['password2']
        contranuevarep = request.POST.get('password2')

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

@login_required(login_url='index')
def enviaform(request):

    if request.method == 'POST':
        artista_id = request.POST['artista']
        artista = Artista.objects.get(id=artista_id)

        if artista:
            if artista.email:
                current_site = get_current_site(request)
                mail_subject = 'Formulario de Ingreso de Artistas a Tocatas Intimas.'
                message = render_to_string('usuario/email_nuevo_artista_cuenta.html', {
                    'user': artista,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(artista.pk)),
                    'token':art_activation_token.make_token(artista),
                })
                to_email = artista.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'usuario/nuevo_artista_done.html')

            else:
                messages.error(request,'Artista no tiene correo registrado')
        else:
            messages.error(request,'Artista no encontrado')

    artistas = Artista.objects.filter(usuario__isnull=True)

    context = {
        'artistas': artistas,
    }

    return render(request,'usuario/enviaformnuevoart.html', context)
