from django.db import models
from datetime import datetime

# Create your models here.
class Artista(models.Model):

    disponible = 'DI'
    noDisponible = 'ND'
    estado_tipos = [
        (disponible, 'Disponible'),
        (noDisponible, 'No Disponible'),
    ]

    nombre = models.CharField(max_length=200)
    foto1 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto2 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto3 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto4 = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    descripción = models.TextField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    telefono_contacto = models.CharField(max_length=200, blank=True)

    estado = models.CharField(max_length=2, choices=estado_tipos,default=disponible)
    fecha_crea = models.DateTimeField(default=datetime.now)
    fecha_actua = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.nombre
