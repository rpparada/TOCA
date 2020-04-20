from django.db import models
from datetime import datetime

from django_resized import ResizedImageField

from toca.parametros import parToca, parArtistas

# Create your models here.
class Artista(models.Model):

    nombre = models.CharField(max_length=200)
    foto1 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto2 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto3 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto4 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)

    foto_525_350 = ResizedImageField(size=[525, 350],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])

    descripción = models.TextField(blank=True)
    habilidades = models.TextField(blank=True)
    
    email = models.EmailField(max_length=254, blank=True)
    telefono_contacto = models.CharField(max_length=200, blank=True)

    link_facebook = models.URLField(max_length=200, blank=True)
    link_twitter = models.URLField(max_length=200, blank=True)
    link_instagram = models.URLField(max_length=200, blank=True)

    estado = models.CharField(max_length=2, choices=parArtistas['estado_tipos'],default=parToca['disponible'])
    fecha_crea = models.DateTimeField(default=datetime.now)
    fecha_actua = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.nombre
