from django.shortcuts import render, redirect
from django.contrib import messages, auth


from django.contrib.auth.models import User
from lugar.models import Lugar

from .forms import AgregaCamposUsuarioForm, UsuarioForm

# Create your views here.
def registrarArt(request):

    if request.method == 'POST':
        form = AgregaCamposUsuarioForm(request.POST)
        usuario_form = UsuarioForm(request.POST)

        if form.is_valid() and usuario_form.is_valid():
            user = form.save()

            usuario = usuario_form.save(commit=False)
            usuario.user = user
            usuario.es_artista = True
            usuario.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            messages.success(request, 'Usuario registrado exitosamente. Ahora puedes ingresar')
            return redirect('index')
        else:
            messages.error(request,form.errors)
            return redirect('registrarart')

    else:
        form = AgregaCamposUsuarioForm();
        usuario_form = UsuarioForm();

    context = {
        'form': form,
        'usuario_form': usuario_form,
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

        usuario = auth.authenticate(username=nombreusuario, password=contra)
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request,'Ingreso Existos')

            tocata_id = request.POST['tocata_id']

            if tocata_id:
                # return redirect('tocata', tocata_id=tocata_id)
                return redirect('/tocatas/'+tocata_id)
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
    usuario = request.user
    lugares = Lugar.objects.filter(usuario=usuario).filter(estado='DI').order_by('-fecha_actua')
    context = {
        'lugares': lugares,
    }
    return render(request, 'usuario/cuenta.html', context)

def actualizar(request):

    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contra = request.POST['contra']
        contra2 = request.POST['contra2']

        usuario = request.user
        lugares = Lugar.objects.filter(usuario=usuario)
        context = {
            'lugares': lugares,
        }

        if contra:
            if contra == contra2:
                usuario.set_password(contra)
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.email = email
            else:
                messages.error(request,'Contraseñas diferentes')
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.email = email
        else:
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = email

        usuario.save()
        messages.success(request,'Actualizacion Existosa')
        return render(request, 'usuario/cuenta.html', context)

def cambioContra(request):
    return render(request, 'usuario/cambiocontra.html')


def cuentaArt(request):
    usuario = request.user
    lugares = Lugar.objects.filter(usuario=usuario).filter(estado='DI').order_by('-fecha_actua')
    context = {
        'lugares': lugares,
    }
    return render(request, 'usuario/cuentaart.html', context)

def emailNuevaContra(request):
    return render(request, 'usuario/emailnuevacontra.html')

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
