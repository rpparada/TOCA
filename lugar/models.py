from django.db import models
from django.contrib.auth.models import User

from toca.parametros import parLugares, parToca

# Create your models here.
class Region(models.Model):

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):

    region          = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):

    provincia       = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)
    region          = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):

    nombre          = models.CharField(max_length=200, blank=True)
    usuario         = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre_calle    = models.CharField(max_length=200)
    numero          = models.IntegerField()
    region          = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    provincia       = models.ForeignKey(Provincia, null=True, blank=True, on_delete=models.DO_NOTHING)
    comuna          = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING)
    ciudad          = models.CharField(max_length=200, blank=True)
    pais            = models.CharField(max_length=100, default=parToca['paisDefecto'])
    codigo_postal   = models.CharField(max_length=20, blank=True)
    departamento    = models.CharField(max_length=20, blank=True)
    otros           = models.CharField(max_length=20, blank=True)

    descripción     = models.TextField(blank=True)
    capacidad       = models.IntegerField()
    evaluacion      = models.IntegerField(choices=parToca['valoresEvaluacion'],default=parToca['defaultEvaluacion'])

    estado          = models.CharField(max_length=2, choices=parLugares['estado_tipos'],default=parToca['disponible'])
    fecha_crea      = models.DateTimeField(auto_now_add=True)
    fecha_actu      = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.nombre:
            return self.nombre+', '+self.nombre_calle+' '+str(self.numero)+', '+str(self.comuna)
        else:
            return self.nombre_calle+' '+str(self.numero)+', '+str(self.comuna)
