from django.db import models

from orden.models import EntradasCompradas

# Create your models here.

# Anulaciones Entradas
class AnulacionEntradaQuerySet(models.query.QuerySet):
    def pendientes(self):
        return self.filter(estado='pendiente')

class AnulacionEntradaManager(models.Manager):
    def get_queryset(self):
        return AnulacionEntradaQuerySet(self.model, self._db)

    def pendientes(self):
        return self.get_queryset().pendientes()

ANULACIONENTRADA_ESTADO_OPCIONES = (
    ('pendiente','Pendiente'),
    ('enviadatbk','Enviada a Transbank'),
    ('reembolsado','Reembolsado'),
)

class AnulacionEntrada(models.Model):

    entradas_compradas      = models.ForeignKey(EntradasCompradas, on_delete=models.CASCADE)

    estado                  = models.CharField(max_length=20, choices=ANULACIONENTRADA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)
