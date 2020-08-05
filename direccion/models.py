from django.db import models

from lugar.models import Region, Comuna
from facturacion.models import FacturacionProfile

from toca.parametros import parToca, parDireccion

# Create your models here.
class Direccion(models.Model):

    facturacion_profile     = models.ForeignKey(FacturacionProfile, on_delete=models.DO_NOTHING)
    tipo_direccion          = models.CharField(max_length=100, choices=parDireccion['tipo_direccion'])
    nombre_calle            = models.CharField(max_length=200)
    numero                  = models.IntegerField()
    region                  = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    comuna                  = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING)
    ciudad                  = models.CharField(max_length=200, blank=True)
    pais                    = models.CharField(max_length=100, default=parToca['paisDefecto'])
    codigo_postal           = models.CharField(max_length=20, blank=True)
    departamento            = models.CharField(max_length=20, blank=True)
    otros                   = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.facturacion_profile)
