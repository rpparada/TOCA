from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                                DetailView,
                                ListView,
                                View,
                                CreateView
                            )

from .models import LugaresTocata

from .forms import (
                CancelarPropuestaForm,
                BorrarPropuestaForm,
                CancelarPropuestaElegidaForm,
                ProponerLugarForm
            )

# Create your views here.
class MisPropuestasListView(LoginRequiredMixin, ListView):
    template_name = 'propuestaslugar/mispropuestas.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        request = self.request
        mis_propuestas = LugaresTocata.objects.mis_propuestas_by_request(request)
        print(mis_propuestas)
        return mis_propuestas

class CancelarPropuestaView(LoginRequiredMixin, View):

    form_class = CancelarPropuestaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.cancelar()

        return redirect('propuestaslugar:mispropuestas')

class BorrarPropuestaView(LoginRequiredMixin, View):

    form_class = BorrarPropuestaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.borrar()

        return redirect('propuestaslugar:mispropuestas')

class CancelarPropuestaElegidaView(LoginRequiredMixin, View):

    form_class = CancelarPropuestaElegidaForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            propuesta = form.cleaned_data['propuesta']
            propuesta.cancelar_elegido()

            # Suspender Tocata Abierta
            # Este proceso tambien suspende Tocata Publicada
            propuesta.tocataabierta.suspender_tocata_confirmado()

        return redirect('propuestaslugar:mispropuestas')


class ProponerLugarView(LoginRequiredMixin, View):

    form_class = ProponerLugarForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST or None)
        if form.is_valid():
            tocataabierta = form.cleaned_data['tocataabierta']
            lugar = form.cleaned_data['lugar']

        return redirect('propuestaslugar:mispropuestas')

@login_required(login_url='index')
def proponerlugar(request, tocata_id):

    if request.method == 'POST':
        form = LugaresTocataForm(request.POST)

        if form.is_valid():

            lugartocata = form.save(commit=False)
            if LugaresTocata.objects.filter(tocataabierta=tocata_id).filter(lugar=lugartocata.lugar).exclude(estado__in=[parToca['cancelado'],parToca['borrado']]):
                messages.error(request,'Ya habias enviado este lugar para esta tocata')
            else:
                tocataabierta = TocataAbierta.objects.get(pk=tocata_id)
                if tocataabierta.comuna.nombre == 'Todas':
                    if tocataabierta.region.nombre == lugartocata.lugar.region.nombre:
                        lugartocata.save()
                        messages.success(request, 'Lugar enviado al artista')
                        return redirect('index')
                    else:
                        messages.error(request,'Lugar no esta en la Region')
                else:
                    if tocataabierta.region.nombre == lugartocata.lugar.region.nombre\
                     and tocataabierta.comuna.nombre == lugartocata.lugar.comuna.nombre:
                     lugartocata.save()
                     messages.success(request, 'Lugar enviado al artista')
                     return redirect('index')
                    else:
                        messages.error(request,'Lugar no esta en la Region y/o Comuna')

        else:
            print(form.errors.as_data())
            messages.error(request,'Error en form')

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    mislugares = Lugar.objects.filter(usuario=request.user).filter(estado=parToca['disponible'])

    context = {
        'mislugares': mislugares,
        'tocata': tocata,
    }

    return render(request, 'tocata/proponerlugar.html', context)

@login_required(login_url='index')
def verpropuestas(request, tocata_id):

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)

@login_required(login_url='index')
def seleccionarpropuestas(request, tocata_id, lugar_id):

    if request.method == 'POST':

        # Cambia estado de TocataAbierta a confirmado
        tocataabierta = get_object_or_404(TocataAbierta, pk=tocata_id)
        tocataabierta.estado = parToca['confirmado']

        # Cambia estado del lugar elegido a "Elegido"
        lugartocata = get_object_or_404(LugaresTocata, pk=lugar_id)
        lugartocata.estado = parToca['elegido']
        lugartocata.save()

        # Cambiar las otras propuestas a "no elegido"
        listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado=parToca['pendiente'])
        for lugar in listaLugares:
            lugar.estado = parToca['noelegido']
            lugar.save()

        # Define capacidades
        asis_min = tocataabierta.asistentes_min
        if lugartocata.lugar.capacidad < tocataabierta.asistentes_min:
            asis_min = lugartocata.lugar.capacidad
            asis_max = lugartocata.lugar.capacidad
        else:
            asis_max = lugartocata.lugar.capacidad

        # Costo
        costotocata = request.POST.get('costo')

        # Crear Tocata oficial (tabla Tocata)
        tocata = Tocata(
            artista=tocataabierta.artista,
            usuario=tocataabierta.usuario,
            nombre=tocataabierta.nombre,
            lugar=lugartocata.lugar,
            region=lugartocata.lugar.region,
            comuna=lugartocata.lugar.comuna,
            descripción=tocataabierta.descripción,
            costo=int(costotocata),
            fecha=tocataabierta.fecha,
            hora=tocataabierta.hora,
            asistentes_total=0,
            asistentes_min=asis_min,
            asistentes_max=asis_max,
            flayer_original=tocataabierta.flayer_original,
            flayer_1920_1280=tocataabierta.flayer_1920_1280,
            flayer_380_507=tocataabierta.flayer_380_507,
            evaluacion=0,
            estado=parToca['publicado'],
        )
        tocata.save()

        tocata.estilos.set(tocataabierta.artista.estilos.all())

        tocataabierta.tocata = tocata
        tocataabierta.save()

        messages.success(request, 'Lugar seleccionado con exito y Tocata publicada')
        return redirect('mistocatas')

    tocata = get_object_or_404(TocataAbierta, pk=tocata_id)
    listaLugares  = LugaresTocata.objects.filter(tocataabierta=tocata).filter(estado=parToca['pendiente'])

    context = {
        'tocata': tocata,
        'listaLugares': listaLugares,
    }

    return render(request, 'tocata/propuestas.html', context)
