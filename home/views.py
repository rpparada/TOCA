from django.shortcuts import render
from django.http import HttpResponse

from tocata.models import Tocata
from artista.models import Artista

from django.db.models import Q

# Create your views here.
def index(request):

    # tocatas = Tocata.objects.order_by('-fecha', '-hora').filter(estado='PU')[:3]
    tocatas = Tocata.objects.all()[:3]
    artistas = Artista.objects.all()[:3]
    context = {
        'tocatas': tocatas,
        'artistas': artistas,
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')

def busqueda(request):

    queryset_list_tocatas = Tocata.objects.all()
    queryset_list_artistas = Artista.objects.all()
    if 'q' in request.GET:
        busqueda = request.GET['q']
        if busqueda:
            queryset_list_tocatas = Tocata.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )

            queryset_list_artistas = Artista.objects.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripción__icontains=busqueda)
            )

    context = {
        'tocatas': queryset_list_tocatas,
        'artistas': queryset_list_artistas,
        'valores': request.GET,
    }

    return render(request, 'home/busqueda.html', context)
