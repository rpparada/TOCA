from django.db import models
from datetime import datetime
from artista.models import Artista
from django.contrib.auth.models import User

from .divpoladmchile import regiones, comunas, provincias

from django_resized import ResizedImageField

# Create your models here.
class Region(models.Model):

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):

    disponible = 'DI'
    noDisponible = 'ND'
    estado_tipos = [
        (disponible, 'Disponible'),
        (noDisponible, 'No Disponible'),
    ]

    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    nombre_calle = models.CharField(max_length=200)
    numero = models.IntegerField(default=0)

    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING, null=True)
    ciudad = models.CharField(max_length=200, default='Santiago')

    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True)
    descripción = models.TextField(blank=True)

    capacidad = models.IntegerField(default=0)

    foto1 = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])
    foto2 = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])
    foto3 = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])
    foto4 = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])

    estado = models.CharField(max_length=2, choices=estado_tipos,default=disponible)
    fecha_crea = models.DateTimeField(default=datetime.now)
    fecha_actua = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.nombre
