from django.shortcuts import render, get_object_or_404
from .models import Artista

# Create your views here.
def artistas(request):
    artistas = Artista.objects.all()
    context = {
        'artistas': artistas
    }
    return render(request, 'artista/artistas.html', context)

def artista(request, artista_id):
    artista = get_object_or_404(Artista, pk=artista_id)
    context = {
        'artista': artista
    }
    return render(request, 'artista/artista.html', context)
