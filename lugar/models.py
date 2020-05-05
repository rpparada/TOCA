from django.db import models
from datetime import datetime
from artista.models import Artista
from django.contrib.auth.models import User

from .divpoladmchile import regiones, comunas, provincias

from django_resized import ResizedImageField

from toca.parametros import parLugares, parToca

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

    provincia = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):

    nombre = models.CharField(max_length=200)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    nombre_calle = models.CharField(max_length=200)
    numero = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    ciudad = models.CharField(max_length=200, default=parToca['cuidadDefecto'])
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20, blank=True)

    descripción = models.TextField(blank=True)
    capacidad = models.IntegerField(default=0)
    evaluacion = models.IntegerField(choices=parToca['valoresEvaluacion'],default=parToca['defaultEvaluacion'])

    estado = models.CharField(max_length=2, choices=parLugares['estado_tipos'],default=parToca['disponible'])

    fecha_crea = models.DateTimeField(default=datetime.now)
    fecha_actua = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.nombre
