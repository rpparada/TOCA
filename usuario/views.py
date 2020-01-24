from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.contrib.auth.models import User
from lugar.models import Lugar

# Create your views here.
def registrar(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        nombreusuario = request.POST['nombreusuario']
        email = request.POST['email']
        contra = request.POST['contra']
        contra2 = request.POST['contra2']

        if contra == contra2:
            if User.objects.filter(username=nombreusuario).exists():
                messages.error(request,'Nombre de Usuario existente')
                return redirect('registrar')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email existente')
                    return redirect('registrar')
                else:
                    usuario = User.objects.create_user(username=nombreusuario, email=email, password=contra, first_name=nombre, last_name=apellido)
                    usuario.save()
                    messages.success(request, 'Usuario registrado exitosamente. Ahora puedes ingresar')
                    return redirect('ingresar')
        else:
            messages.error(request,'Contraseñas diferentes')
            return redirect('registrar')
    else:
        return render(request, 'usuario/registrar.html')

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
