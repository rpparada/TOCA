from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Tocata, CompraTocata
from artista.models import Artista
from lugar.models import Lugar
from django.db.models import Q

from django.core.mail import send_mail

from django.contrib import messages

# Create your views here.
def tocatas(request):
    # tocatas = Tocata.objects.all()
    # tocatas = Tocata.objects.order_by('-fecha', '-hora').filter(estado='PU')
    tocatas = Tocata.objects.order_by('-fecha', '-hora')

    paginador = Paginator(tocatas, 6)
    pagina = request.GET.get('page')
    pagina_tocatas = paginador.get_page(pagina)

    context = {
        'tocatas': pagina_tocatas
    }
    return render(request, 'tocata/tocatas.html', context)

def tocata(request, tocata_id):
    tocata = get_object_or_404(Tocata, pk=tocata_id)
    context = {
        'tocata': tocata
    }
    return render(request, 'tocata/tocata.html', context)

def mediopago(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            usuario = request.user
            tocata_id = request.POST['tocata_id']
            tocata = Tocata.objects.get(id=tocata_id)

            ha_compradro = CompraTocata.objects.all().filter(usuario=usuario, tocata=tocata)
            if ha_compradro:
                messages.error(request,'Ya tienes tu entreda')
                return redirect('/tocatas/'+tocata_id)
            else:
                compra = CompraTocata(tocata=tocata, usuario=usuario, estado='AC')
                compra.save()

                # send_mail(
                #    'subject_Prueba',
                #    'body_Prueba',
                #    'rpparada@gmail.com',
                #    ['rpparada@gmail.com','rpparada@hotmail.com'],
                #    fail_silently=False
                #)

                messages.success(request, 'Compra exitosa')
                return render(request, 'tocata/mediopago.html')
    else:
        context = {
            'valores': request.POST
        }
        return render(request, 'usuario/ingresar.html', context)
