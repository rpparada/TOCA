from django.shortcuts import render, redirect, get_object_or_404
from .models import Lugar
from .forms import AgregarForm, EditarForm
from django.contrib import messages

from django.utils import timezone

# Create your views here.
def agregar(request):

    form = AgregarForm()

    if request.method == 'POST':
        form = AgregarForm(request.POST)
        if form.is_valid():
            nuevoLugar = form.save(commit=False)
            if 'foto1' in request.FILES:
                nuevoLugar.foto1 = request.FILES['foto1']
            if 'foto2' in request.FILES:
                nuevoLugar.foto2 = request.FILES['foto2']
            if 'foto3' in request.FILES:
                nuevoLugar.foto3 = request.FILES['foto3']
            if 'foto4' in request.FILES:
                nuevoLugar.foto4 = request.FILES['foto4']
            nuevoLugar.usuario = request.user
            nuevoLugar.fecha_crea = timezone.now()
            nuevoLugar.save()
            messages.success(request, 'Lugar agregado exitosamente')
            return redirect('cuenta')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')
            return redirect('agregar')

    return render(request, 'lugar/agregar.html', {'form':form})

def borrarlugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    lugar.estado = lugar.noDisponible
    lugar.save()
    return redirect('cuenta')

def editarlugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    form = EditarForm(instance=lugar)
    if request.method == 'POST':
        form = EditarForm(request.POST, instance=lugar)
        if form.is_valid():
            editarLugar = form.save(commit=False)
            if 'foto1' in request.FILES:
                editarLugar.foto1 = request.FILES['foto1']
            if 'foto2' in request.FILES:
                editarlugar.foto2 = request.FILES['foto2']
            if 'foto3' in request.FILES:
                editarLugar.foto3 = request.FILES['foto3']
            if 'foto4' in request.FILES:
                editarlugar.foto4 = request.FILES['foto4']
            editarlugar.fecha_actua = timezone.now()
            editarLugar.save()
            messages.success(request, 'Lugar editado exitosamente')
            return redirect('cuenta')
        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')
            return redirect('cuenta')

    return render(request,'lugar/editar.html', {'form':form})

def detalleslugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    context = {
        'lugar': lugar,
    }
    return render(request,'lugar/lugar.html', context)
