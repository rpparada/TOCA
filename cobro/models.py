from django.db import models

from django.contrib.auth.models import User

from tocata.models import Tocata

from toca.parametros import parToca, parCarro, parOrden, mediodepago
# Create your models here.
class Carro(models.Model):

    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    estado = models.CharField(max_length=2, choices=parCarro['estado_carro'],default=parToca['pendiente'])
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.email+' '+self.tocata.nombre+' '+str(self.cantidad)+' '+str(self.cantidad*self.tocata.costo)

class Orden(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    numerodeitems = models.IntegerField(default=0)
    totalapagar = models.IntegerField(default=0)
    mediodepago = models.CharField(max_length=2, choices=mediodepago['medio_de_pago'],default=parToca['webpay'])

    #session id
    #numero tarjeta

    # Campos TBK
    #sharesAmount
    #sharesNumber
    #amount
    #commerceCode
    #buyOrder
    #authorizationCode
    #paymentTypeCode
    #responseCode

    estado = models.CharField(max_length=2, choices=parOrden['estado_orden'],default=parToca['pendiente'])
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)

class OrdenTocata(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.DO_NOTHING)
    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)

    #estado = models.CharField(max_length=2, choices=parCarro['estado_carro'],default=parToca['pendiente'])
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)
